FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        curl \
        ffmpeg \
        aria2 \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        pyrogram==2.0.106 \
        tgcrypto \
        yt-dlp \
        py-tgcalls==0.9.7

# Make downloads folder
RUN mkdir -p /app/downloads

# Run bot
CMD ["python", "main.py"]