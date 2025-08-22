FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server/ .

# Set environment variables for development
ARG PYTHONPATH

ENV PYTHONPATH="/app:$PYTHONPATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Expose the port
EXPOSE 5143

# Default command - can be overridden in docker-compose
CMD ["python", "-m", "flask", "--app", "app.main", "run", "--host=0.0.0.0", "--port=5143", "--debug", "--reload"]
