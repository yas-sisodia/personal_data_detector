import cv2
from PIL import Image
import pytesseract
from ultralytics import YOLO
from presidio_analyzer import AnalyzerEngine

from backend.core.model_manager import get_classifier, get_blip, load_yolo_models

classifier = get_classifier()
processor, blip_model = get_blip()
yolo_models = load_yolo_models()







analyzer = AnalyzerEngine()

CANDIDATE_LABELS = [
    "identity information such as a person's name, ID badge or face",
    "financial information such as bank details or payment cards",
    "medical or health information",
    "contact information such as phone number or email",
    "location or address information",
    "vehicle information such as license plate numbers",
    "digital screen content showing private messages",
    "non-sensitive public information"
]

# =========================================================
# Shared helpers
# =========================================================
def run_ocr(image_path):
    return pytesseract.image_to_string(Image.open(image_path))



def run_ocr_on_video(video_path):
    """
    Runs OCR on a video and returns extracted text.
    """

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file")

    final_text = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray)
        text = text.strip()

        if text:
            final_text.append(text)

    cap.release()

    return "\n".join(final_text)



def detect_objects(image):
    objects = []
    
    for model in yolo_models:
        results = model.predict(image, conf=0.5)
        for r in results:
            if r.boxes is not None:
                for c in r.boxes.cls:
                    objects.append(r.names[int(c)])
    return list(set(objects))

def predict(chosen_model, img, classes=[], conf=0.5):
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)

    return results


def predict_and_detect(chosen_model, img, classes=[], conf=0.5, rectangle_thickness=2, text_thickness=1):
    results = predict(chosen_model, img, classes, conf=conf)
    detected_objects = []
    for result in results:
        for box in result.boxes:
            cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
            object_name = result.names[int(box.cls[0])]
            detected_objects.append(object_name)
            cv2.putText(img, f"{object_name}",
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
    return img,detected_objects, results



def detect_objects_on_image(image):
    image = cv2.imread(image)
    result_img1, det_obj1, results1 = predict_and_detect(yolo_models[0], image, classes=[], conf=0.5)
    result_img2, det_obj2, results2 = predict_and_detect(yolo_models[1], image, classes=[], conf=0.5)
    result_img3, det_obj3, results3 = predict_and_detect(yolo_models[2], image, classes=[], conf=0.5)
    objects = list(set(det_obj1 + det_obj2 + det_obj3))
    return sorted({obj.strip().lower() for obj in objects})

import cv2


def detect_objects_in_video(video_path,
                       skip_frames=5,
                       conf=0.5,
                       display=False):
    return []

def detect_objects_in_video(video_path,
                       skip_frames=5,
                       conf=0.5,
                       display=False):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    frame_id = 0

    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()

        if not ret:
            break

        result_img1, det_obj1, results1 = predict_and_detect(
            yolo_models[2], frame, classes=[], conf=conf)

      
        

        if display:
            cv2.imshow("Detection", result_img1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        frame_id += skip_frames  # Skip frames for speed

    cap.release()
    cv2.destroyAllWindows()
    return sorted({obj.strip().lower() for obj in det_obj1})    





def generate_caption(image_path, max_tokens=50):
    image = Image.open(image_path).convert("RGB")
    # processor, blip_model = ensure_blip2_model()

    inputs = processor(images=image, return_tensors="pt")
    ids = blip_model.generate(**inputs, max_new_tokens=max_tokens)
    return processor.decode(ids[0], skip_special_tokens=True)
    # return "A caption describing the image."

def classify(text):
    # clf = get_classifier()
    # clf = ensure_bart_model()
    result = classifier(text, candidate_labels=CANDIDATE_LABELS)
    return result


def analyze_text(text, language="en"):
    return analyzer.analyze(text=text, language=language)


def convert_text_segments(text_segments):
    """
    Converts Presidio RecognizerResult objects into JSON-serializable dicts.
    """

    clean_segments = []

    for seg in text_segments:
        clean_segments.append({
            "type": getattr(seg, "entity_type", None),  # 🔥 FIX HERE
            "start": getattr(seg, "start", None),
            "end": getattr(seg, "end", None),
            "score": getattr(seg, "score", None)
        })

    return clean_segments

