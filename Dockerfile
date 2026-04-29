# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set environment variables for performance and cleaner logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Install dependencies by copying requirements.txt first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 8000
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
