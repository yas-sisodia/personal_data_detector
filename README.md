


## run python setup.py in terminal

# Project Setup and Run Instructions

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

<!-- 
docker build -t personal_data_app . 

 docker run -p 8501:8501 personal_data_app


http://localhost:8501/ -->
