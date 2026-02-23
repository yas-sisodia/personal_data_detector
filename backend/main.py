

# ==========================================================


from fastapi import FastAPI, WebSocket, UploadFile
import shutil
import uuid
import os
import traceback
import sys
import asyncio
from typing import Any
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from backend.core.image_pipeline import run_image_pipeline  # next step
from backend.core.video_pipeline import run_video_pipeline  # next step
# from core.image_pipeline import run_image_pipeline  # next step
# from core.video_pipeline import run_video_pipeline  # next step


from contextlib import asynccontextmanager
from backend.core.model_manager import load_all_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up... Ensuring models exist.")
    
    load_all_models()  # download only
    
    print("✅ Models ready.")

    yield  # <-- App runs here

    print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan)



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # ==========================================================
# # Upload endpoint (image + video)
# # ==========================================================
# @app.post("/upload")
# async def upload_file(file: UploadFile):
#     file_id = str(uuid.uuid4())
#     file_name = f"{file_id}_{file.filename}"
#     file_path = os.path.join(UPLOAD_DIR, file_name)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     return {
#         "file_name": file_name,
#         "content_type": file.content_type
#     }


BASE_PATH = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_PATH / "backend" / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Upload endpoint (image + video)
# ==========================================================
@app.post("/upload")
async def upload_file(file: UploadFile):
    file_id = str(uuid.uuid4())
    file_name = f"{file_id}_{file.filename}"
    file_path = UPLOAD_DIR / file_name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_name": file_name,
        "content_type": file.content_type
    }

# ==========================================================
# WebSocket analysis endpoint
# ==========================================================
@app.websocket("/ws/analyze")
async def websocket_analyze(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket connected")

    try:
        data = await websocket.receive_json()
        file_id = data["file_id"]
        file_type = data.get("file_type", "image")  # default image
        enable_caption = data.get("enable_caption", False)

        file_path = os.path.join(UPLOAD_DIR, file_id)

        if not os.path.exists(file_path):
            await websocket.send_json({
                "type": "error",
                "message": "File not found"
            })
            await websocket.close()
            return

        async def progress_cb(step: str, percent: int, other_data: dict[str, Any] | None):
            data = {
                "type": "progress",
                "step": step,
                "percent": percent, 
                "other_data":other_data
            }
            print(f"Emitting progress: {data}")
            await websocket.send_json(data)
            await asyncio.sleep(0.05)

        # ---------------- ROUTING ----------------
        if file_type == "video":
            print("🎥 Running video pipeline")
            result = await run_video_pipeline(
                file_path,
                progress_cb=progress_cb,
                enable_caption=enable_caption
            )
        else:
            print("🖼️ Running image pipeline")
            result = await run_image_pipeline(
                file_path,
                progress_cb=progress_cb,
                enable_caption=enable_caption
            )

        await websocket.send_json({
            "type": "result",
            "data": result
        })

    except Exception as e:
        traceback.print_exc()
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })

    finally:
        await websocket.close()
        print("🔌 WebSocket closed")









    