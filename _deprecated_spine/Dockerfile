# Gap 128: Pinning Base OS (Bookworm Slim)
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

# Gap 127: Multi-Stage - Export requirements to avoid poetry in runtime
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# --- Runner Stage ---
FROM python:3.11-slim-bookworm AS runner

WORKDIR /app

# Gap 126: Configure Non-Root User
RUN groupadd -r vte && useradd -r -g vte vte_user

# Runtime Dependencies & Playwright
# Gap 134: Caching - optimized apt and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && pip install playwright \
    && playwright install --with-deps chromium \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache/pip

# Install Python Deps from Builder
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Application Code
COPY . .

# Gap 131: Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Gap 129/130: Scanning/Signing should happen in CI before push
# Gap 133: Logging limits configured in runtime (docker-compose/k8s)

# Switch to constrained user
USER vte_user

# Expose port
EXPOSE 8000

# Command
CMD ["uvicorn", "spine.main:app", "--host", "0.0.0.0", "--port", "8000"]
