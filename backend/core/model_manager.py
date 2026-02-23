



from pathlib import Path
from ultralytics import YOLO

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoProcessor,
    Blip2ForConditionalGeneration,
    pipeline,
)




# ==========================================================
# PATH SETUP - adjust as needed
# ==========================================================

BASE_PATH = Path(__file__).resolve().parents[2]
MODELS_DIR = BASE_PATH / "backend" / "models"
YOLO_DIR = MODELS_DIR / "yolo"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
YOLO_DIR.mkdir(parents=True, exist_ok=True)

BART_MODEL_PATH = MODELS_DIR / "bart-mnli"
BLIP2_MODEL_PATH = MODELS_DIR / "blip2-opt-2.7b"

# ==========================================================
# GLOBAL CACHE (VERY IMPORTANT)
# ==========================================================

_classifier = None
_blip_processor = None
_blip_model = None


# ==========================================================
# BART (Zero-shot classifier)
# ==========================================================

def ensure_bart_model():
    config_file = BART_MODEL_PATH / "config.json"
    if not BART_MODEL_PATH.exists() or not config_file.exists():
        print("Downloading BART model...")
        model_name = "facebook/bart-large-mnli"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, 
                                                                #    device_map="auto"
                                                                   )

        tokenizer.save_pretrained(BART_MODEL_PATH)
        model.save_pretrained(BART_MODEL_PATH)

        print("BART saved locally.")
    else:
        print("BART model already exists.")


def get_classifier():
    global _classifier

    if _classifier is None:
        print("Loading BART into memory...")

        model = AutoModelForSequenceClassification.from_pretrained(
            BART_MODEL_PATH,
            local_files_only=True,
            # device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(
            BART_MODEL_PATH,
            local_files_only=True
        )

        _classifier = pipeline(
            "zero-shot-classification",
            model=model,
            tokenizer=tokenizer
        )

    return _classifier


# ==========================================================
# BLIP2
# ==========================================================

def ensure_blip2_model():
    config_file = BLIP2_MODEL_PATH / "config.json"
    if not BLIP2_MODEL_PATH.exists() or not config_file.exists():
        print("Downloading BLIP2 model...")
        model_name = "Salesforce/blip2-opt-2.7b"

        processor = AutoProcessor.from_pretrained(model_name, use_fast=False)
        model = Blip2ForConditionalGeneration.from_pretrained(model_name, 
                                                            #   device_map="auto"
                                                              )

        processor.save_pretrained(BLIP2_MODEL_PATH)
        model.save_pretrained(BLIP2_MODEL_PATH)

        print("BLIP2 saved locally.")
    else:
        print("BLIP2 model already exists.")


def get_blip():
    global _blip_processor, _blip_model

    if _blip_model is None:
        print("Loading BLIP2 into memory...")

        _blip_processor = AutoProcessor.from_pretrained(
            BLIP2_MODEL_PATH,
            local_files_only=True,
            use_fast=False
        )

        _blip_model = Blip2ForConditionalGeneration.from_pretrained(
            BLIP2_MODEL_PATH,
            local_files_only=True
        )

        _blip_model.eval()

    return _blip_processor, _blip_model


# ==========================================================
# YOLO
# ==========================================================

def ensure_yolo_model(model_filename: str):
    model_path = YOLO_DIR / model_filename

    if not model_path.exists():
        print(f"Downloading {model_filename}...")
        model = YOLO(model_filename)
        model.save(str(model_path))
        print(f"Saved {model_filename}")
    else:
        print(f"{model_filename} already exists.")

    return YOLO(str(model_path))


def load_yolo_models():
    model_files = [
        "yolov9c.pt",
        "yolov8l-oiv7.pt",
        "yolov8x-oiv7.pt",
    ]

    return [ensure_yolo_model(name) for name in model_files]


# ==========================================================
# LOAD ALL (DOWNLOAD ONLY)
# ==========================================================

def load_all_models():
    """
    Ensures all models are downloaded.
    Does NOT load large models into RAM.
    """
    print("Ensuring all models exist...")

    ensure_bart_model()
    ensure_blip2_model()
    load_yolo_models()

    print("All models ready.")



