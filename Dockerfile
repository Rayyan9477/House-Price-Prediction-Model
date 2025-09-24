# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update \
    && apt-get install -y --no-install-recommends \

        curl \

        ca-certificates \
        gcc \
        g++ \

    && rm -rf /var/lib/apt/lists/* \

    && update-ca-certificates \
    && curl --version


# Copy requirements file
COPY requirements.txt .


RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \

    && python -m pip install --no-cache-dir -r requirements.txt \

    && python -m pip list


# Copy application code
COPY . .

# Reconstruct model if parts exist and verify artifact
RUN set -e; \
    echo "Attempting model reconstruction..."; \
    python split_model.py reconstruct || true; \
    if [ -s house_price_model.pkl ]; then \
        echo "Model reconstruction successful"; \
    else \
        echo "Model reconstruction not available. App will train on first run."; \
    fi

# Create a non-root user and set proper permissions
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app \
    && chmod +x app.py split_model.py

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]
