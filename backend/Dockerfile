FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PyMuPDF or compiling FAISS
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create the vector store directory to ensure it can be mounted or written to
RUN mkdir -p /app/faiss_index

COPY . ./backend

# Expose FastAPI port
EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
