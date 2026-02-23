import cv2
from backend.core.shared import (
    analyze_text,
    convert_text_segments,
    run_ocr,
    detect_objects_on_image,
    generate_caption,
    classify,
)




async def run_image_pipeline(image_path, progress_cb=None, enable_caption=False):

    async def emit(step: str, percent: int, data=None):
        if progress_cb:
            await progress_cb(step, percent, data)

    data = {}

    await emit("Loading image", 5, data)

    # OCR
    await emit("Detecting text (OCR)", 20, data)
    text = run_ocr(image_path)
    textSeg = analyze_text(text)

    data["text"] = text
    data["textSeg"] = convert_text_segments(textSeg)

    await emit("Running object detection", 45, data)

    # Object detection
    objects = detect_objects_on_image(image_path)
    data["objects"] = objects

    await emit("Generating image caption", 70, data)

    # Caption
    caption = ""
    if enable_caption:
        caption = generate_caption(image_path)
    data["caption"] = caption

    await emit("Final sensitivity classification", 90, data)

    # Classification
    merged_text = f"{text}\n{objects}\n{caption}\n{textSeg}"
    classification = classify(merged_text)

    data["sequence"] = merged_text
    data["labels"] = classification["labels"]
    data["scores"] = classification["scores"]

    
    await emit("Completed", 100, data)

    return data

