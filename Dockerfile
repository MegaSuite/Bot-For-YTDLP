FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

# Install system dependencies and create virtual environment
RUN apk add --no-cache \
    ffmpeg \
    python3-dev \
    gcc \
    musl-dev \
    && python3 -m venv /venv

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./ytdlp-tgbot ./ytdlp-tgbot

# Create required directories
RUN mkdir -p /app/configs /app/downloads /app/logs \
    && adduser -D appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Command to run the application
CMD ["python3", "-m", "ytdlp-tgbot"]