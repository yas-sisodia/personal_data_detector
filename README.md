


## run python setup.py in terminal

# Project Setup and Run Instructions

# Setup Instructions

Follow these steps to set up the virtual environment for the project.

## ✅ STEP  — Create Virtual Environment

⚠️ **IMPORTANT:**  
Run this command in your **terminal** (NOT inside a Jupyter notebook):


```bash
python -m venv .venv

for windows

```bash
.venv\Scripts\Activate

```bash
source .venv/bin/activate

Once activated correctly, your terminal prompt will change to show something like this:
(.venv)

## Step  — Start Backend (FastAPI) and Frontend (Streamlit)

1. **Start the Backend (FastAPI):**

   - Open a new terminal and make sure your virtual environment is activated.
   - Run the following command to start the backend:

     ```bash
     uvicorn backend.main:app --reload
     ```

   - Wait until you see the following message:

     ```
     INFO:     Application startup complete.
     ```

   - The backend will be running at: [http://127.0.0.1:8000](http://127.0.0.1:8000).
   - **Do NOT close this terminal.**

2. **Start the Frontend (Streamlit):**

   - Open another new terminal and activate your virtual environment again.
   - Run the following command to start the frontend:

     ```bash
     streamlit run frontend/app.py
     ```

   - The frontend will be running at: [http://localhost:8501](http://localhost:8501).
  

# Image Processing Pipeline

This repository contains an image processing pipeline that performs **OCR**, **object detection**, **image captioning**, and **sensitivity classification**. The pipeline extracts relevant data from images and classifies the information into predefined categories such as **identity**, **financial**, **medical**, etc.

## Pipeline Overview

<!-- Link to your visual diagram -->
![Pipeline Flow] 
<img width="1408" height="768" alt="pipeline" src="https://github.com/user-attachments/assets/731c3971-933f-4e18-8121-7b247979d595" />


### The pipeline consists of the following steps:

1. **Loading the Image**
   - The image is loaded into the system for processing.

2. **OCR (Optical Character Recognition)**
   - Extracts text from the image using Tesseract OCR.

3. **Text Analysis**
   - Extracted text is analyzed using **Presidio Analyzer** to detect sensitive information (e.g., names, phone numbers).

4. **Object Detection**
   - Uses **YOLO** models to detect objects in the image (e.g., persons, vehicles, etc.).

5. **Image Captioning** *(Optional)*
   - Generates a natural language description of the image using a **BLIP model**.

6. **Sensitivity Classification**
   - The extracted text, objects, and caption are classified into predefined categories (e.g., **identity information**, **financial information**).

7. **Final Output**
   - A structured output containing extracted text, detected objects, captions (optional), and classification labels.

---

## How It Works for image

The pipeline processes images through a series of steps as shown in the diagram above. Below is an example of how the system processes an image:

1. **Input Image**: 
   A sample image is uploaded.

2. **Run OCR**:
   - The OCR extracts any text from the image.

3. **Detect Objects**:
   - YOLO models detect objects present in the image.

4. **Generate Caption** *(Optional)*:
   - A BLIP model generates a description of the image content.

5. **Classify Information**:
   - The extracted information is classified into categories like **Identity**, **Financial**, **Medical**, etc.

6. **Output**:
   The final output contains the image text, detected objects, optional caption, and classification labels.

 
## How It Works for video

Video pipeline works saame as image pipeline. Vidos is breaked into frames which are different . we take 2 frames from start and 2 from middle an 2 from end then we proceed according to image pipeline.




<!-- 
docker build -t personal_data_app . 

 docker run -p 8501:8501 personal_data_app


http://localhost:8501/ -->
