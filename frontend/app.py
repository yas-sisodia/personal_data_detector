
# =============================================================================


from xml.etree.ElementTree import tostring

import streamlit as st
import websocket
import json
import requests
import traceback
import base64
from PIL import Image
import time
import io
import threading
import queue

# ==============================================================================
# Backend endpoints
# BACKEND_UPLOAD = "localhost:8000/upload"
# WS_URL = "ws://localhost:8000/ws/analyze"
BACKEND_UPLOAD = "http://localhost:8000/upload"
WS_URL = "ws://localhost:8000/ws/analyze"
# BACKEND_UPLOAD = "http://backend:8000/upload"
# WS_URL = "ws://backend:8000/ws/analyze"
# BACKEND_UPLOAD = "http://pii_backend:8000/upload"
# WS_URL = "ws://pii_backend:8000/ws/analyze"

# ==============================================================================
# Page config
st.set_page_config(page_title="Live PII Detection", layout="wide")
st.title("🔴 Live Personal Data Detection Framework (Image & Video)")



# ==============================================================================
# Session state defaults
defaults = {
    "uploaded_file": None,
    "file_type": None,
    "result": None,
    "show_results": False,
    "last_file_name": None,
    "is_analyzing": False,
    "trigger_analysis": False,
    "analysis_started": False,
    "ws_queue": None,
    "ws_thread": None,
    "progress_percent": 0,
    "progress_step": "",
    "enable_caption": True,
    "start_time": None, 
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v



# Ensure key exists
if "enable_caption" not in st.session_state:
    st.session_state.enable_caption = True

# Use the toggle widget and link to session state
st.toggle(
    "📝 Enable Image Captioning",
    value=st.session_state.enable_caption,
    key="enable_caption"  # <-- use the same key as session state
)

# You can now safely use st.session_state.enable_caption anywhere
st.write("Captioning enabled:", st.session_state.enable_caption)

print(f"Image caption Toggle: {st.session_state.enable_caption}")
# enable_caption = st.toggle("📝 Enable Image Captioning", value=True)
# st.session_state.enable_caption = enable_caption




# ==============================================================================
# WebSocket listener (runs in background thread)

def websocket_listener(file_id, file_type, message_queue, enable_caption):
    try:
        ws = websocket.WebSocket()
        ws.connect(WS_URL, timeout=3000)

        ws.send(json.dumps({
            "file_id": file_id,
            "file_type": file_type,
            "enable_caption": enable_caption
        }))

        while True:
            msg = ws.recv()
            if not msg:
                break

            data = json.loads(msg)
            message_queue.put(data)

            if data["type"] in ["result", "error"]:
                break

        ws.close()

    except Exception as e:
        message_queue.put({"type": "error", "message": str(e)})

# ==============================================================================


def reset_for_new_upload():
    st.session_state.result = None
    st.session_state.show_results = False

    st.session_state.progress_percent = 0
    st.session_state.progress_step = ""

    st.session_state.analysis_started = False
    st.session_state.trigger_analysis = False
    st.session_state.is_analyzing = False

    st.session_state.ws_queue = None
    st.session_state.ws_thread = None

# ==============================================================================


def highlight_text(text, segments):
    if not text or not segments:
        return text

    COLOR = "#e53935"

    # Filter out invalid segments
    valid_segments = [
        seg for seg in segments
        if seg.get("start") is not None
        and seg.get("end") is not None
        and isinstance(seg.get("start"), int)
        and isinstance(seg.get("end"), int)
    ]

    if not valid_segments:
        return text

    valid_segments = sorted(valid_segments, key=lambda x: x["start"])

    result = []
    last = 0

    for seg in valid_segments:
        print(f"Processing segment: {seg}")
        start, end = seg["start"], seg["end"]
        label = seg.get("type") or "SENSITIVE"
        score = seg.get("score") or 0

        if start < last:
            continue

        result.append(text[last:start])
        result.append(
            f'<span style="background-color:{COLOR};'
            f'padding:2px 4px;border-radius:4px;font-weight:600;" '
            f'title="{label} ({score:.2f})">'
            f'{text[start:end]}</span>'
        )
        last = end

    result.append(text[last:])
    return "".join(result)

# ==============================================================================
# File upload

uploaded = st.file_uploader(
    "Upload image or video",
    type=["jpg", "jpeg", "png", "mp4", "mov", "avi"],
    disabled=st.session_state.is_analyzing
)

# ==============================================================================


if uploaded and uploaded.name != st.session_state.last_file_name:
    reset_for_new_upload()

    st.session_state.uploaded_file = uploaded
    st.session_state.last_file_name = uploaded.name
    st.session_state.file_type = (
        "video" if uploaded.type.startswith("video") else "image"
    )

    st.session_state.is_analyzing = True
    st.session_state.trigger_analysis = True

    st.rerun()


# ==============================================================================
# Layout

left_col, right_col = st.columns([1, 3], gap="large")

            

with left_col:
    if st.session_state.uploaded_file:

        if st.session_state.file_type == "image":
            st.image(st.session_state.uploaded_file, use_container_width=True)
        else:
            st.video(st.session_state.uploaded_file)


    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    if st.session_state.is_analyzing:
        progress_placeholder.progress(
            st.session_state.progress_percent / 100
        )
        status_placeholder.markdown(
            f"**{st.session_state.progress_step}**"
        )
    elif "start_time" in st.session_state and st.session_state.start_time is not None and st.session_state.is_analyzing is not True and st.session_state.is_analyzing is not 1:
            elapsed_time = time.time() - st.session_state.start_time
            elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))  # Format as HH:MM:SS
            st.markdown(f" ⏱️ Total Processing Time: {elapsed_time_str}")
    else:
        st.info("Select an image or video to begin")
    

# ==============================================================================
# Start analysis (only once)

if st.session_state.trigger_analysis and not st.session_state.analysis_started:
     # Start time for the analysis
    st.session_state.start_time = time.time()

    st.session_state.analysis_started = True
    st.session_state.trigger_analysis = False
    progress_bar = progress_placeholder.progress(0.0)
    status_text = status_placeholder.empty()





    try:
        files = {"file": st.session_state.uploaded_file}
        response = requests.post(BACKEND_UPLOAD, files=files)

        if response.status_code == 200:

            file_id = response.json()["file_name"]

            msg_queue = queue.Queue()
            st.session_state.ws_queue = msg_queue

            thread = threading.Thread(
           target=websocket_listener,
             args=(
              file_id,
              st.session_state.file_type,
              msg_queue,
              st.session_state.enable_caption   # ✅ pass value
    ),
    daemon=True
)
            thread.start()

            st.session_state.ws_thread = thread

        else:
            st.error(f"Upload failed ({response.status_code})")
            st.session_state.is_analyzing = False

    except Exception:
        traceback.print_exc()
        st.error("Connection failed")
        st.session_state.is_analyzing = False

# ==============================================================================
# Process queue (runs every rerun)

if st.session_state.ws_queue:

    while not st.session_state.ws_queue.empty():
        data = st.session_state.ws_queue.get()
        
        if data["type"] == "progress":

            st.session_state.show_results = True
            st.session_state.progress_percent = data["percent"]
            st.session_state.progress_step = data.get("step", "")

            # progress_bar.progress(data["percent"] / 100)
            # status_text.markdown(f"**{data.get('step','')}**")



            if st.session_state.result is None:
                st.session_state.result = {}

            incoming = data.get("other_data", {})

            for k, v in incoming.items():
                if v is not None:
                    st.session_state.result[k] = v

        # elif data["type"] == "result":

        #     st.session_state.result = data["data"]
        #     st.session_state.progress_percent = 100
        #     st.session_state.progress_step = "Completed"            
        #     st.session_state.is_analyzing = False
        #     st.session_state.show_results = True
        elif data["type"] == "result":

            st.session_state.result = data["data"]
            st.session_state.progress_percent = 100
            st.session_state.progress_step = "Completed"
            st.session_state.show_results = True

            st.session_state.is_analyzing = False
            st.session_state.analysis_started = False
            st.session_state.trigger_analysis = False
            st.session_state.ws_thread = None
            st.session_state.ws_queue = None

            # ====
                # Calculate and display the total time spent on processing



            st.rerun()   # 🔥 force UI refresh


        elif data["type"] == "error":

            st.error(data["message"])
            st.session_state.is_analyzing = False

# ==============================================================================
# Results UI

with right_col:
    if st.session_state.show_results and st.session_state.result:

        st.subheader("📊 Sensitivity Analysis Results")




# ========

        st.markdown("### 📄 Extracted Text")
        st.text_area(
            "Detected Content",
            value=st.session_state.result.get("sequence", ""),
            height=200
        )

        if "objects" in st.session_state.result:
            st.markdown("### 🧠 Detected Objects")
            st.write(", ".join(set(st.session_state.result["objects"])))

        if "caption" in st.session_state.result:
            st.markdown("### 📝 Scene / Context Caption")
            st.write(st.session_state.result["caption"])

        st.divider()
        st.markdown("### 🔐 Sensitivity Classification")

        for label, score in sorted(
            zip(
                st.session_state.result.get("labels", []),
                st.session_state.result.get("scores", [])
            ),
            key=lambda x: x[1],
            reverse=True
        ):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"**{label}**")
                st.progress(score)
            with c2:
                st.write(f"**{round(score * 100, 2)}%**")

        if "caption_image" in st.session_state.result:
            img_bytes = base64.b64decode(
                st.session_state.result["caption_image"]
            )
            img = Image.open(io.BytesIO(img_bytes))
            st.markdown("### 🖼️ Video Context Image")
            st.image(img, use_container_width=True)

        if "textSeg" in st.session_state.result:
            st.markdown("### 🖍️ Highlighted Sensitive Text")

            highlighted_html = highlight_text(
                st.session_state.result.get("text", ""),
                st.session_state.result.get("textSeg", [])
            )

            st.markdown(
f"""<div style="
line-height:1.8;
font-size:18px;
padding:14px;
border:1px solid #333;
border-radius:8px;
background-color:#000000;
color:#ffffff;
white-space:pre-wrap;
word-wrap:break-word;
">
{highlighted_html}
</div>""",
                unsafe_allow_html=True
            )



# ==============================================================================
# Controlled polling loop

if st.session_state.is_analyzing:
    time.sleep(0.1)
    st.rerun()