FROM python:3.12-slim AS python

# Build stage
FROM python AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -e .

# Runtime stage
FROM python AS runtime

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set PATH to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY ./ville_flexible /app/ville_flexible

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "ville_flexible.main:app", "--host", "0.0.0.0", "--port", "8000"]