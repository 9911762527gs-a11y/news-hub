# News Hub - Dockerfile for Railway Deployment
# Multi-stage build for smaller image size

FROM python:3.12-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir --user -e .

# --- Runtime stage ---
FROM python:3.12-slim

# Install runtime dependencies for Edge TTS (Microsoft Edge)
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
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft Edge for Edge TTS
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - && \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" | tee /etc/apt/sources.list.d/microsoft-edge.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends microsoft-edge-stable && \
    rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy built dependencies from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Add local bin to PATH
ENV PATH=/root/.local/bin:$PATH

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/root/.local/bin:$PATH"

# Create output directory
RUN mkdir -p /app/output /app/logs

# Expose ports
EXPOSE 8000
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default command (runs scheduler)
CMD ["python", "-m", "news_hub.scheduler"]
