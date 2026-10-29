from pathlib import Path
from contextlib import asynccontextmanager
from io import BytesIO
import json
import logging
import warnings
from threading import Lock

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

WORKSPACE_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = WORKSPACE_DIR / "FoodVision-AI"
FRONTEND_DIR = PROJECT_DIR / "frontend"
MODEL_DIR = PROJECT_DIR / "model"
HUB_DIR = WORKSPACE_DIR / "VisionAI-Hub" / "frontend"
MASK_FRONTEND_DIR = WORKSPACE_DIR / "MaskVision-AI" / "frontend"
MASK_MODEL_DIR = WORKSPACE_DIR / "MaskVision-AI" / "model"
MAX_IMAGE_BYTES = 15 * 1024 * 1024
logger = logging.getLogger(__name__)


def validate_food_preprocessing(config, class_names):
    expected = {
        "image_size": [128, 128], "color_mode": "rgb",
        "resize_backend": "tensorflow", "interpolation": "bilinear",
        "antialias": False, "preserve_aspect_ratio": False,
        "normalization": "divide_by_255", "input_range": [0.0, 1.0],
        "unknown_threshold": 0.6, "class_names": class_names,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"Unsupported FoodVision preprocessing: {key}")


class FaceGate:
    """Reusable YuNet detector; lock protects OpenCV's mutable inference state."""

    def __init__(self, model_path):
        import cv2
        self.cv = cv2
        self.lock = Lock()
        self.detector = cv2.FaceDetectorYN.create(
            str(model_path), "", (640, 640), 0.8, 0.3, 5000
        )
        # Fail at startup if the ONNX file is invalid or incompatible.
        self.detector.detect(np.zeros((640, 640, 3), dtype=np.uint8))

    def __call__(self, image):
        width, height = image.size
        scale = min(640 / width, 640 / height)
        size = (max(1, round(width * scale)), max(1, round(height * scale)))
        bgr = self.cv.cvtColor(np.asarray(image), self.cv.COLOR_RGB2BGR)
        resized = self.cv.resize(bgr, size, interpolation=self.cv.INTER_AREA if scale < 1 else self.cv.INTER_LINEAR)
        canvas = np.zeros((640, 640, 3), dtype=np.uint8)
        canvas[:size[1], :size[0]] = resized
        with self.lock:
            _, faces = self.detector.detect(canvas)
        if faces is None:
            return 0
        # Ignore detections whose centers lie outside the actual image area.
        return sum(1 for face in faces if np.isfinite(face).all()
                   and face[2] > 0 and face[3] > 0
                   and 0 <= face[0] + face[2] / 2 < size[0]
                   and 0 <= face[1] + face[3] / 2 < size[1])


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = None
    app.state.class_names = []
    app.state.mask_model = None
    app.state.mask_class_names = []
    app.state.mask_preprocessing_ready = False
    app.state.mask_face_detector = None
    # כשל בטעינה משאיר את האתר זמין עם הודעת שגיאה ברורה.
    try:
        from tensorflow.keras.models import load_model
        names = json.loads((MODEL_DIR / "class_names.json").read_text(encoding="utf-8"))
        if not isinstance(names, list) or len(names) != 11 or not all(isinstance(n, str) and n for n in names) or len(set(names)) != 11:
            raise ValueError("Expected 11 unique class names")
        preprocessing = json.loads((MODEL_DIR / "preprocessing.json").read_text(encoding="utf-8"))
        validate_food_preprocessing(preprocessing, names)
        model = load_model(MODEL_DIR / "foodvision.keras", compile=False, safe_mode=True)
        if tuple(model.input_shape[1:]) != (128, 128, 3) or model.output_shape[-1] != len(names):
            raise ValueError("Model shape does not match Food-11")
        app.state.class_names = names
        app.state.model = model
    except Exception:
        logger.exception("FoodVision model could not be loaded")
    try:
        from tensorflow.keras.models import load_model
        names = json.loads((MASK_MODEL_DIR / "class_names.json").read_text(encoding="utf-8"))
        if names != ["with_mask", "without_mask"]:
            raise ValueError("Unexpected MaskVision class order")
        model = load_model(MASK_MODEL_DIR / "maskvision_baseline.keras", compile=False, safe_mode=True)
        if tuple(model.input_shape[1:]) != (128, 128, 3) or model.output_shape[-1] != len(names):
            raise ValueError("Model shape does not match MaskVision")
        app.state.mask_model = model
        app.state.mask_class_names = names
        preprocessing = json.loads((MASK_MODEL_DIR / "preprocessing.json").read_text(encoding="utf-8"))
        app.state.mask_preprocessing_ready = preprocessing.get("verified") is True and all(
            preprocessing.get(key) == expected for key, expected in {
                "color_mode": "RGB", "image_size": [128, 128],
                "resample": "tensorflow_bilinear", "scale_divisor": 255,
            }.items()
        )
    except Exception:
        logger.exception("MaskVision model could not be loaded")
    try:
        app.state.mask_face_detector = FaceGate(MASK_MODEL_DIR / "face_detection_yunet_2023mar.onnx")
    except Exception:
        logger.exception("MaskVision face detector could not be loaded")
    yield
    app.state.model = None
    app.state.mask_model = None
    app.state.mask_face_detector = None


app = FastAPI(title="Vision AI API", lifespan=lifespan)


@app.middleware("http")
async def prevent_stale_app_pages(request, call_next):
    response = await call_next(request)
    path = request.url.path
    if path in {"/", "/home", "/food", "/mask", "/results", "/ready", "/health", "/mask/health"} or path.endswith((".js", ".css", ".json")):
        response.headers["Cache-Control"] = "no-store, max-age=0"
    return response


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.mount("/hub-static", StaticFiles(directory=HUB_DIR), name="hub-static")
app.mount("/mask-static", StaticFiles(directory=MASK_FRONTEND_DIR), name="mask-static")


@app.api_route("/home", methods=["GET", "HEAD"], include_in_schema=False)
def vision_home():
    return FileResponse(HUB_DIR / "index.html")


@app.get("/results", include_in_schema=False)
def model_results():
    return FileResponse(HUB_DIR / "results.html")


@app.get("/project-brief.pdf", include_in_schema=False)
def project_brief():
    return FileResponse(WORKSPACE_DIR / "project03_cnn_dec25.pdf", media_type="application/pdf")


@app.get("/mask", include_in_schema=False)
def mask_home():
    return FileResponse(MASK_FRONTEND_DIR / "index.html")


@app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)
def read_root():
    return FileResponse(HUB_DIR / "index.html")


@app.get("/food", include_in_schema=False)
def food_home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health_check():
    return {"status": "ok", "model_ready": app.state.model is not None}


@app.get("/ready")
def readiness_check():
    checks = {
        "food_model": getattr(app.state, "model", None) is not None,
        "mask_model": getattr(app.state, "mask_model", None) is not None,
        "mask_preprocessing": getattr(app.state, "mask_preprocessing_ready", False),
        "face_detector": getattr(app.state, "mask_face_detector", None) is not None,
    }
    ready = all(checks.values())
    return JSONResponse({"status": "ready" if ready else "not_ready", **checks},
                        status_code=200 if ready else 503)


@app.get("/mask/health")
def mask_health_check():
    return {"status": "ok", "model_ready": app.state.mask_model is not None,
            "preprocessing_ready": app.state.mask_preprocessing_ready,
            "face_detector_ready": app.state.mask_face_detector is not None,
            "class_names": app.state.mask_class_names}


@app.post("/mask/predict")
def mask_predict(file: UploadFile = File(...)):
    if not app.state.mask_preprocessing_ready:
        file.file.close()
        raise HTTPException(503, detail="preprocessingPending")
    if app.state.mask_face_detector is None:
        file.file.close()
        raise HTTPException(503, detail="faceDetectorUnavailable")
    return predict_image(file, app.state.mask_model, app.state.mask_class_names,
                         resize_method="tensorflow_bilinear", face_check=app.state.mask_face_detector)


@app.post("/predict")
def predict(file: UploadFile = File(...)):
    return predict_image(file, app.state.model, app.state.class_names,
                         resize_method="tensorflow_bilinear", decode_backend="tensorflow")


def predict_image(file: UploadFile, model, class_names, *, resize_method="nearest", face_check=None,
                  decode_backend="pillow"):
    if model is None:
        file.file.close()
        raise HTTPException(503, detail="modelUnavailable")
    try:
        content = file.file.read(MAX_IMAGE_BYTES + 1)
        if len(content) > MAX_IMAGE_BYTES:
            raise HTTPException(413, detail="tooLarge")
        # Both supplied notebooks use TensorFlow bilinear resize and float32 /255.
        # Preserve the notebook's TensorFlow decoder for ordinary Food-11 files.
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(content)) as image:
                original_format = image.format
                orientation = image.getexif().get(274, 1)
                image = ImageOps.exif_transpose(image).convert("RGB")
                if face_check is not None:
                    try:
                        face_count = face_check(image)
                    except Exception:
                        logger.exception("Face detection failed")
                        raise HTTPException(503, detail="faceDetectorUnavailable")
                    if face_count == 0:
                        raise HTTPException(422, detail="noFace")
                    if face_count > 1:
                        raise HTTPException(422, detail="multipleFaces")
                if resize_method == "tensorflow_bilinear":
                    import tensorflow as tf
                    source = np.asarray(image)
                    if decode_backend == "tensorflow" and orientation == 1 and original_format in {"JPEG", "PNG", "BMP", "GIF"}:
                        try:
                            source = tf.io.decode_image(content, channels=3, expand_animations=False)
                        except tf.errors.InvalidArgumentError:
                            raise HTTPException(400, detail="invalidImage")
                    # WebP and EXIF-rotated phone photos use the oriented RGB pixels.
                    pixels = tf.image.resize(source, (128, 128), method="bilinear",
                                             antialias=False, preserve_aspect_ratio=False).numpy()
                else:
                    pixels = np.asarray(image.resize((128, 128), Image.Resampling.NEAREST), dtype=np.float32)
                batch = np.expand_dims(pixels / 255.0, axis=0)
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(400, detail="invalidImage")
    finally:
        file.file.close()
    try:
        probabilities = np.asarray(model(batch, training=False), dtype=np.float32)
        if probabilities.shape != (1, len(class_names)) or not np.isfinite(probabilities).all():
            raise ValueError("Invalid model output")
        scores = probabilities[0]
        if np.any(scores < 0) or np.any(scores > 1) or not np.isclose(scores.sum(), 1, atol=1e-3):
            raise ValueError("Expected softmax probabilities")
        index = int(np.argmax(scores))
        raw_class = class_names[index]
        confidence = float(scores[index]) * 100
        return {
            "prediction": raw_class if confidence >= 60 else "Unknown",
            "raw_prediction": raw_class,
            "confidence": confidence,
            "probabilities": [
                {"category": name, "probability": float(score), "confidence": float(score) * 100}
                for name, score in zip(class_names, scores)
            ],
        }
    except Exception:
        logger.exception("Vision inference failed")
        raise HTTPException(500, detail="inferenceError")
