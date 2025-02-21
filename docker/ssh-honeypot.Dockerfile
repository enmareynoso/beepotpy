# Base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching
COPY ./app/ssh_honeypot/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app/ssh_honeypot /app/ssh_honeypot
COPY ./app/web_api/mongodb.py /app/web_api/

# Expose SSH port
EXPOSE 2222

# Entrypoint
CMD ["python", "-u", "/app/ssh_honeypot/ssh_server.py"]