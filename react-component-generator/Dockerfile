# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV GCP_PROJECT=${GCP_PROJECT}

# Expose port
EXPOSE 8080

# Command to run the application
CMD streamlit run src/app.py \
    --server.port=${PORT} \
    --server.address=0.0.0.0 \
    --browser.serverAddress="0.0.0.0" \
    --server.baseUrlPath="" \
    --browser.gatherUsageStats=false