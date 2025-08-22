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

# Set Python path to include app directory
ENV PYTHONPATH="/app:$PYTHONPATH"

# Expose the port
EXPOSE 5143

# Command to run the application
CMD ["python", "-m", "app.main"]
