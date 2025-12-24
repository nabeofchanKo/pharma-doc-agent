# Base image: use a lightweight slim variant
FROM python:3.10-slim

# Production tip: disable output buffering to flush logs immediately (for debugging)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

# Production tip: install system-level dependencies
# (e.g., gcc is required to build some Python libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Production tip: caching strategy (layer caching)
# Copy and install requirements before copying source code (COPY . .)
# This allows skipping the dependency installation step when only code changes
COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# During development, the host volume is mounted, so only create the directory here
# (In production deployment, COPY . . will be added here)
RUN mkdir -p /app/src/backend

# Health check
# (Allows ECS or similar orchestrators to restart the container if it dies)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Startup command
CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]