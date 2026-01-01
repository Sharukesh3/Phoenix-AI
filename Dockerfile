FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for psycopg2 and git for some python packages)
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Set Python path to ensure imports work correctly
ENV PYTHONPATH=/app

# Copy source code
COPY . .

# Command to run the application (placeholder, will likely be overridden by docker-compose)
CMD ["python", "src/main.py"]
