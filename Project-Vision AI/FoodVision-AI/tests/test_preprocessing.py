"""Verify FoodVision's serving pipeline against the supplied Colab notebook."""
import importlib.util
import json
from io import BytesIO
from pathlib import Path
import unittest

import numpy as np
from PIL import Image
from fastapi import UploadFile

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("foodvision_backend", root.parent / "VisionAI-Hub/backend/main.py")
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class FoodPreprocessingTests(unittest.TestCase):
    def setUp(self):
        self.names = json.loads((root / "model/class_names.json").read_text())

    def test_exported_metadata_and_sixty_percent_rule(self):
        config = json.loads((root / "model/preprocessing.json").read_text())
        api.validate_food_preprocessing(config, self.names)
        for changed in [{"unknown_threshold": 0.5}, {"interpolation": "nearest"}, {"class_names": self.names[::-1]}]:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                api.validate_food_preprocessing({**config, **changed}, self.names)

    def test_deployment_readiness_requires_both_models_and_face_gate(self):
        from unittest.mock import patch
        with patch.object(api.app.state, "model", object(), create=True), \
             patch.object(api.app.state, "mask_model", object(), create=True), \
             patch.object(api.app.state, "mask_preprocessing_ready", True, create=True), \
             patch.object(api.app.state, "mask_face_detector", object(), create=True):
            self.assertEqual(api.readiness_check().status_code, 200)
            api.app.state.mask_model = None
            self.assertEqual(api.readiness_check().status_code, 503)
            api.app.state.mask_model = object()
            api.app.state.mask_face_detector = None
            self.assertEqual(api.readiness_check().status_code, 503)

    def test_food_route_matches_notebook_on_jpeg_png_and_webp(self):
        import tensorflow as tf

        image = Image.fromarray(np.random.default_rng(13).integers(0, 256, (173, 239, 3), dtype=np.uint8))
        for format_name in ["PNG", "JPEG", "WEBP"]:
            with self.subTest(format=format_name):
                stream = BytesIO()
                image.save(stream, format=format_name)
                content = stream.getvalue()
                if format_name == "WEBP":
                    source = np.asarray(Image.open(BytesIO(content)).convert("RGB"))
                else:
                    source = tf.io.decode_image(content, channels=3, expand_animations=False)
                expected = tf.image.resize(source, (128, 128), method="bilinear", antialias=False).numpy()[None] / 255.0

                def model(batch, training):
                    self.assertFalse(training)
                    self.assertEqual(batch.dtype, np.float32)
                    np.testing.assert_allclose(batch, expected, atol=1e-7, rtol=0)
                    return [[0.9] + [0.01] * 10]

                api.app.state.model = model
                api.app.state.class_names = self.names
                result = api.predict(UploadFile(file=BytesIO(content), filename="food.png"))
                self.assertEqual(result["prediction"], self.names[0])
                self.assertEqual(len(result["probabilities"]), 11)

    def test_threshold_is_sixty_not_fifty(self):
        for best, unknown in [(0.5, True), (0.599, True), (0.6, False), (0.8, False)]:
            with self.subTest(confidence=best):
                stream = BytesIO()
                Image.new("RGB", (19, 23)).save(stream, format="PNG")
                scores = [[best] + [(1 - best) / 10] * 10]
                result = api.predict_image(UploadFile(file=BytesIO(stream.getvalue())), lambda *a, **k: scores, self.names)
                self.assertEqual(result["prediction"], "Unknown" if unknown else self.names[0])


if __name__ == "__main__":
    unittest.main()
