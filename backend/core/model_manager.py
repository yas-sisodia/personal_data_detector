



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
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

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
            local_files_only=True
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
        model = Blip2ForConditionalGeneration.from_pretrained(model_name)

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





# =========================

# from pathlib import Path
# from ultralytics import YOLO

# from transformers import AutoProcessor, Blip2ForConditionalGeneration

# from transformers import (
#     AutoModelForSequenceClassification,
#     AutoTokenizer,
#     pipeline
# )


# BASE_PATH = Path(__file__).resolve().parents[2]
# YOLO_DIR = BASE_PATH / "backend" / "models" / "yolo"

# YOLO_DIR.mkdir(parents=True, exist_ok=True)


# from pathlib import Path
# from transformers import (
#     AutoTokenizer,
#     AutoModelForSequenceClassification,
#     AutoProcessor,
#     AutoModelForVisualQuestionAnswering,
#     pipeline,
# )

# BASE_PATH = Path(__file__).resolve().parents[2]
# MODELS_DIR = BASE_PATH / "backend" / "models"

# MODELS_DIR.mkdir(parents=True, exist_ok=True)


# # =========================
# # BART MNLI
# # =========================
# def ensure_bart_model():
#     model_dir = MODELS_DIR / "bart-mnli"

#     if model_dir.exists():
#         print("BART model already exists.")
#         return get_classifier()
#     else:
#         print("Downloading BART model...")
#         model_name = "facebook/bart-large-mnli"

#         tokenizer = AutoTokenizer.from_pretrained(model_name)
#         model = AutoModelForSequenceClassification.from_pretrained(model_name)

#         tokenizer.save_pretrained(model_dir)
#         model.save_pretrained(model_dir)

#         print("BART saved locally.")

#     tokenizer = AutoTokenizer.from_pretrained(model_dir)
#     model = AutoModelForSequenceClassification.from_pretrained(model_dir)

#     # return tokenizer, model
#     return pipeline(
#             "zero-shot-classification",
#             model=model,
#             tokenizer=tokenizer
#         )



# BART_MODEL_PATH = BASE_PATH / "backend" / "models" / "bart-mnli"
# BART_MODEL_PATH = str(BART_MODEL_PATH)

# def get_classifier():
#     global classifier
#     if classifier is None:
#         model = AutoModelForSequenceClassification.from_pretrained(
#             BART_MODEL_PATH,
#             local_files_only=True
#         )
#         tokenizer = AutoTokenizer.from_pretrained(
#             BART_MODEL_PATH,
#             local_files_only=True
#         )
#         classifier = pipeline(
#             "zero-shot-classification",
#             model=model,
#             tokenizer=tokenizer
#         )
#     return classifier

# # =========================
# # BLIP2
# # =========================

# Blip2_MODEL_PATH = BASE_PATH / "backend" / "models" / "blip2-opt-2.7b"
# Blip2_MODEL_PATH = str(Blip2_MODEL_PATH)

# def ensure_blip2_model():
#     model_dir = MODELS_DIR / "blip2-opt-2.7b"
    
#     if model_dir.exists():    
        
#         processor, model =get_blip()
#         print("BLIP2 model already exists.")
#         return processor, model

#     else:
#         print("Downloading BLIP2 model...")
#         model_name = "Salesforce/blip2-opt-2.7b"

#         processor = AutoProcessor.from_pretrained(model_name, use_fast=False)
#         model = AutoModelForVisualQuestionAnswering.from_pretrained(model_name)

#         processor.save_pretrained(model_dir)
#         model.save_pretrained(model_dir)

#         print("BLIP2 saved locally.")

#     processor = AutoProcessor.from_pretrained(model_dir)
#     model = AutoModelForVisualQuestionAnswering.from_pretrained(model_dir)

#     return processor, model


# def get_blip():
#     global blip_model, processor
#     if blip_model is None:
#         processor = AutoProcessor.from_pretrained(
#             Blip2_MODEL_PATH,
#             local_files_only=True,
#             use_fast=False
#         )

#         blip_model = Blip2ForConditionalGeneration.from_pretrained(
#             Blip2_MODEL_PATH,
#             local_files_only=True
#         )

#         blip_model.eval()

#     return processor, blip_model




# def ensure_yolo_model(model_filename: str):
#     model_path = YOLO_DIR / model_filename

#     if model_path.exists():
#         print(f"{model_filename} already exists.")
#         return model_path

#     print(f"{model_filename} not found. Downloading...")

#     # This triggers Ultralytics auto-download
#     model = YOLO(model_filename)

#     # Save to your controlled directory
#     model.save(str(model_path))

#     print(f"Saved to {model_path}")

#     return model_path


# def load_yolo_models():
#     model_files = [
#         "yolov9c.pt",
#         "yolov8l-oiv7.pt",
#         "yolov8x-oiv7.pt",
#     ]

#     models = []

#     for filename in model_files:
#         model_path = ensure_yolo_model(filename)
#         models.append(YOLO(str(model_path)))

#     return models


# # =========================
# # LOAD ALL MODELS
# # =========================
# def load_all_models():
#     print("Loading all models...")

#     # YOLO
#     yolo_models = load_yolo_models()

#     # BART
#     bart_tokenizer, bart_model = ensure_bart_model()

#     # BLIP2
#     blip_processor, blip_model = ensure_blip2_model()

#     print("All models loaded successfully.")

#     return {
#         "yolo": yolo_models,
#         "bart_tokenizer": bart_tokenizer,
#         "bart_model": bart_model,
#         "blip_processor": blip_processor,
#         "blip_model": blip_model,
#     }





