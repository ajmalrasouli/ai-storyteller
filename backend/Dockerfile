# Use Python 3.11 slim image
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libssl1.1 \
        libasound2 \
        libffi6 \
        libstdc++6 \
        libgcc1 \
        libgomp1 \
        ca-certificates \
        curl \
        libcurl4 \
        libuuid1 \
        libtinfo6 \
        libzstd1 \
        libgssapi-krb5-2 \
        libxcb1 \
        libx11-6 \
        libopus0 \
        libpulse0 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]