FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

# Upgrade pip
RUN pip install --upgrade pip

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Install Playwright Browsers (Chromium only to save space)
RUN poetry run playwright install --with-deps chromium

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Command
CMD ["uvicorn", "vte.main:app", "--host", "0.0.0.0", "--port", "8000"]
