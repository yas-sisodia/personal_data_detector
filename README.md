 
# System Requirements 
RAM : 16 GB ( recommended )
ROM : 30 GB


# Make sure python version should be 3.11.x(stable and wide support) 

download link : https://www.python.org/downloads/release/python-3119/

# ✅ STEP  Install Tesseract OCR ( version 5.5.0 )

Tesseract is required for OCR (extracting text from images).

---

 🪟 Windows Users

1. Download Tesseract from:
   https://github.com/UB-Mannheim/tesseract/wiki

3. Install it (recommended location):
   C:\Program Files\Tesseract-OCR
   If installation path is different copy at time of installation

5. Add it to Environment Variables (PATH):

   - Press Windows Key
   - Search "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System Variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add:
     C:\Program Files\Tesseract-OCR
   - Click OK and restart terminal / VS Code
     
<img width="1200" height="900" alt="set env variables" src="https://github.com/user-attachments/assets/bb7c4b05-e32b-4e2a-85c5-f5d0e1d6e782" />

---

🍎 Mac Users

Run this in Terminal:

   <!-- `brew install tesseract` -->
    brew install tesseract

🍎 Linux Users

Run this in Terminal:

   <!-- `brew install tesseract` -->
    sudo apt install tesseract-ocr

---

## ✅ Verify Installation

After installation, restart your terminal and run:

    tesseract --version


If it prints version details → Installation successful.

Before moving to next step restarting your system is recommended or atleast powershell or terminal and code editor.
# ✅ STEP Create Virtual Environment 

Run this in terminal:

    python -m venv .venv

Activate Virtual Environment
  - windows:
  
      1.     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
      
      2.     .venv/Scripts/Activate

  - Mac/Linux
    -     source .venv/bin/activate

If activated correctly, you will see:

    (.venv)

# ✅ STEP  Set your hugging face token to setup.py file
It is variable named as "token" in this file 


# ✅ STEP run below command in .venv terminal

    pip install -r requirements.txt

# ✅ STEP run setup.py by pasting below command in .venv terminal


    python setup.py


# ✅ STEP — Start Backend (FastAPI) and Frontend (Streamlit)











<!-- 
## run python setup.py in terminal

# Project Setup and Run Instructions

## Step  — Start Backend (FastAPI) and Frontend (Streamlit) -->

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

## How It Works

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

## UI
<!-- 
![UI](https://github.com/user-attachments/assets/4f1163dc-5e08-4509-986b-4b717052686b) -->

<img src="https://github.com/user-attachments/assets/4f1163dc-5e08-4509-986b-4b717052686b" height="300" />


## Results

[An image showing chatting](https://github.com/user-attachments/files/25533659/chat.pdf)

[ A general food image](https://github.com/user-attachments/files/25533670/food.pdf)

<!-- 
docker build -t personal_data_app . 

 docker run -p 8501:8501 personal_data_app


http://localhost:8501/ -->
