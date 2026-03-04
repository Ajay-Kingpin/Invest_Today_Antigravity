# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install .

# Copy project files
COPY . .

# Create directory for cache
RUN mkdir -p data/cache

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Default command (will be overridden by docker-compose)
CMD ["python", "run_local.py"]
