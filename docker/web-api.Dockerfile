# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY ./app/web_api/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app/web_api /app/web_api

# Expose API port
EXPOSE 8000

# Startup command
CMD ["uvicorn", "web_api.main:app", "--host", "0.0.0.0", "--port", "8000"]