FROM ubuntu:24.04

# Add metadata
LABEL maintainer="Developer"
LABEL description="Telegram YouTube Downloader Bot"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

# Install system dependencies and create virtual environment
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /venv

# Set working directory
WORKDIR /telegram_youtube_downloader

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Command to run the application
CMD ["python3", "telegram_youtube_downloader"]