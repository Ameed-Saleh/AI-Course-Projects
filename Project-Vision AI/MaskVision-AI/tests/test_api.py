"""Run with the FoodVision virtualenv: python -m unittest discover -s MaskVision-AI/tests."""
import importlib.util
import json
from io import BytesIO
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np
from PIL import Image
from fastapi import HTTPException, UploadFile

backend = Path(__file__).resolve().parents[2] / "VisionAI-Hub/backend/main.py"
spec = importlib.util.spec_from_file_location("vision_backend", backend)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


def upload(content=None):
    if content is None:
        stream = BytesIO()
        Image.new("L", (19, 23), 128).save(stream, format="PNG")
        content = stream.getvalue()
    return UploadFile(file=BytesIO(content), filename="phone.png")


class PredictionTests(unittest.TestCase):
    names = ["with_mask", "without_mask"]

    def test_exported_binary_classes_and_excluded_incorrect_masks(self):
        model_dir = Path(__file__).resolve().parents[1] / "model"
        names = json.loads((model_dir / "class_names.json").read_text())
        config = json.loads((model_dir / "preprocessing.json").read_text())
        self.assertEqual(names, self.names)
        self.assertEqual(config["label_policy"]["incorrect_mask"], "excluded")

    def test_rgb_size_normalization_and_class_order(self):
        def model(batch, training):
            self.assertFalse(training)
            self.assertEqual(batch.shape, (1, 128, 128, 3))
            self.assertEqual(batch.dtype, np.float32)
            np.testing.assert_allclose(batch, 128 / 255)
            return [[0.8, 0.2]]
        file = upload()
        result = api.predict_image(file, model, self.names)
        self.assertTrue(file.file.closed)
        self.assertEqual(result["prediction"], "with_mask")
        self.assertEqual([p["category"] for p in result["probabilities"]], self.names)
        self.assertAlmostEqual(result["confidence"], 80, places=4)

    def test_low_confidence_is_unknown_and_retains_best_match(self):
        result = api.predict_image(upload(), lambda *a, **k: [[0.59, 0.41]], self.names)
        self.assertEqual(result["prediction"], "Unknown")
        self.assertEqual(result["raw_prediction"], "with_mask")

    def test_phone_exif_orientation_is_applied(self):
        image = Image.new("RGB", (2, 1))
        image.putpixel((0, 0), (255, 0, 0))
        image.putpixel((1, 0), (0, 0, 255))
        exif = Image.Exif()
        exif[274] = 6  # Phone photo rotated 90 degrees clockwise for display.
        stream = BytesIO()
        image.save(stream, format="PNG", exif=exif)

        def model(batch, training):
            np.testing.assert_array_equal(batch[0, 0, 0], [1, 0, 0])
            np.testing.assert_array_equal(batch[0, -1, 0], [0, 0, 1])
            return [[0.8, 0.2]]
        api.predict_image(upload(stream.getvalue()), model, self.names)

    def test_food_eleven_class_contract_is_preserved(self):
        names = [f"food-{i}" for i in range(11)]
        scores = [[0.01] * 10 + [0.9]]
        result = api.predict_image(upload(), lambda *a, **k: scores, names)
        self.assertEqual(result["prediction"], "food-10")
        self.assertEqual(len(result["probabilities"]), 11)

    def test_mask_route_matches_notebook_dataset_preprocessing(self):
        import tensorflow as tf

        pixels = np.random.default_rng(42).integers(0, 256, (231, 137, 3), dtype=np.uint8)
        image = Image.fromarray(pixels)
        with TemporaryDirectory(prefix="maskvision-preprocessing-") as directory:
            source = Path(directory) / "face.png"
            image.save(source)
            dataset = tf.keras.utils.image_dataset_from_directory(
                directory, labels=None, image_size=(128, 128),
                batch_size=1, shuffle=False, verbose=False,
            )
            expected = next(iter(dataset)).numpy().astype(np.float32) / 255.0
            nearest = np.asarray(image.resize((128, 128), Image.Resampling.NEAREST), dtype=np.float32) / 255.0
            self.assertFalse(np.allclose(expected[0], nearest))

            def model(batch, training):
                np.testing.assert_allclose(batch, expected, atol=1e-7, rtol=0)
                return [[0.8, 0.2]]

            api.app.state.mask_preprocessing_ready = True
            api.app.state.mask_model = model
            api.app.state.mask_class_names = self.names
            api.app.state.mask_face_detector = lambda image: 1
            result = api.mask_predict(upload(source.read_bytes()))
            self.assertEqual(result["prediction"], "with_mask")

    def test_no_face_and_multiple_faces_do_not_run_classifier(self):
        for count, detail in [(0, "noFace"), (2, "multipleFaces")]:
            file = upload()
            with self.subTest(count=count):
                from unittest.mock import Mock
                model = Mock()
                with self.assertRaises(HTTPException) as raised:
                    api.predict_image(file, model, self.names, face_check=lambda image: count)
                self.assertEqual(raised.exception.status_code, 422)
                self.assertEqual(raised.exception.detail, detail)
                model.assert_not_called()
                self.assertTrue(file.file.closed)

    def test_face_gate_sees_oriented_full_resolution_image(self):
        image = Image.new("RGB", (50, 80))
        stream = BytesIO()
        image.save(stream, format="PNG")
        def gate(image):
            self.assertEqual(image.size, (50, 80))
            self.assertEqual(image.mode, "RGB")
            return 1
        result = api.predict_image(upload(stream.getvalue()), lambda *a, **k: [[0.8, 0.2]], self.names, face_check=gate)
        self.assertEqual(result["prediction"], "with_mask")

    def test_detector_failure_blocks_classification(self):
        from unittest.mock import Mock
        model = Mock()
        def broken_detector(image):
            raise RuntimeError("detector failed")
        with self.assertLogs(api.logger, level="ERROR"), self.assertRaises(HTTPException) as raised:
            api.predict_image(upload(), model, self.names, face_check=broken_detector)
        self.assertEqual(raised.exception.status_code, 503)
        model.assert_not_called()

    def test_invalid_image_and_oversized_upload_are_closed(self):
        for file, size, status in [(upload(b"not an image"), 100, 400), (upload(b"x" * 33), 32, 413)]:
            with self.subTest(status=status), patch.object(api, "MAX_IMAGE_BYTES", size):
                with self.assertRaises(HTTPException) as raised:
                    api.predict_image(file, object(), self.names)
                self.assertEqual(raised.exception.status_code, status)
                self.assertTrue(file.file.closed)

    def test_invalid_model_outputs_are_rejected(self):
        for scores in [[[0.1, 0.2]], [[0.1, 0.1, 0.1]], [[float("nan"), 0, 0]], [[-1, 1, 1]]]:
            with self.subTest(scores=scores), self.assertLogs(api.logger, level="ERROR"):
                with self.assertRaises(HTTPException) as raised:
                    api.predict_image(upload(), lambda *a, **k: scores, self.names)
                self.assertEqual(raised.exception.status_code, 500)

    def test_unavailable_model_and_pending_preprocessing(self):
        file = upload()
        with self.assertRaises(HTTPException) as raised:
            api.predict_image(file, None, self.names)
        self.assertEqual(raised.exception.status_code, 503)
        self.assertTrue(file.file.closed)
        api.app.state.mask_preprocessing_ready = False
        file = upload()
        with self.assertRaises(HTTPException) as raised:
            api.mask_predict(file)
        self.assertEqual(raised.exception.detail, "preprocessingPending")
        self.assertTrue(file.file.closed)


if __name__ == "__main__":
    unittest.main()
