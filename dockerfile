# FROM python:3.10-slim
FROM python:3.11.14-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first
COPY requirements.txt .

# Install CPU torch separately (smaller)
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install remaining Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Create uploads folder
RUN mkdir -p backend/uploads

# Expose ONLY frontend port
EXPOSE 8501

# Run both backend + frontend
CMD bash -c "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0"