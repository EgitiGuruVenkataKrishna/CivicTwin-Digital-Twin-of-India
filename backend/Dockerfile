# ==========================================================================
# CivicTwin Backend — Dockerfile
# Deployed on Render (free tier) / Railway
# Base: python:3.11-slim with GDAL + PostGIS system dependencies
# ==========================================================================

# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Create non-root user
RUN useradd --create-home appuser
WORKDIR /app

# Copy backend source code
COPY . .

# Switch to non-root user
USER appuser

# Render injects $PORT at runtime (default 8000 for local dev)
ENV PORT=8000
EXPOSE ${PORT}

# Health-check for container orchestrators
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import httpx; httpx.get(f'http://localhost:{__import__(\"os\").environ.get(\"PORT\",8000)}/health')" || exit 1

CMD uvicorn civictwin_backend.main:app --host 0.0.0.0 --port ${PORT}
