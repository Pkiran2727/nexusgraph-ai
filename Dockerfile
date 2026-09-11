FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Set Hugging Face Spaces default environment variables
ENV PORT=7860
ENV HOST=0.0.0.0

EXPOSE 7860

# Run FastAPI server
CMD ["python", "backend/main.py"]
