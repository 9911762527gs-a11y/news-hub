# News Hub - Dockerfile for Railway/Render Deployment
# Fixed for better compatibility with Render

FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Install system dependencies FIRST (critical for edge-tts and moviepy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft Edge for Edge TTS (required)
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - && \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" | tee /etc/apt/sources.list.d/microsoft-edge.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends microsoft-edge-stable && \
    rm -rf /var/lib/apt/lists/*

# Copy entire project first
COPY . .

# Install Python dependencies (install directly, not in editable mode)
RUN pip install --no-cache-dir \
    feedparser>=6.0 \
    requests>=2.32 \
    python-dotenv>=1.1 \
    edge-tts>=7.0 \
    moviepy>=2.0 \
    pillow>=11.0 \
    schedule>=1.2 \
    tweepy>=4.14 \
    google-api-python-client>=2.150 \
    google-auth-oauthlib>=1.2 \
    google-auth-httplib2>=0.2 \
    aiohttp>=3.11 \
    groq>=0.5.0 \
    instaloader>=4.10 \
    flask>=3.0

# Create necessary directories
RUN mkdir -p /app/output /app/logs /app/assets/backgrounds /app/assets/characters /app/assets/fonts

# Expose port for dashboard
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default command (runs scheduler)
CMD ["python", "-m", "news_hub.scheduler"]
