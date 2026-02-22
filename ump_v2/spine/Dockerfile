# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Prepend poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies (needed for Playwright and PostgreSQL building)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    libffi-dev \
    # Webkit dependencies for Playwright
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies (including Playwright, AsyncPG)
RUN poetry install --no-root --only main

# Install Playwright browser binaries (needed for the Headless Scraper Adapter)
RUN poetry run playwright install chromium --with-deps

# Copy the source code (Assuming Docker build context is `ump_v2/spine`)
COPY . .

# Expose the API Port
EXPOSE 8080

# Command to run the FastAPI Spine using Uvicorn async worker
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
