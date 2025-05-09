# backend/Dockerfile

# Use Python 3.10 slim image (as per your original file)
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements file first for layer caching
COPY backend/requirements.txt .

# Install system dependencies needed by Python packages (Keep this section!)
# Includes libraries for audio (libasound2, libopus0, libpulse0), SSL, etc.
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
    # Clean up apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create and configure the data directory for Azure Files mount
# Set proper permissions and declare volume
RUN mkdir -p /data && \
    chmod 777 /data
VOLUME /data

# Expose port 5000 (Informational, ACA uses its own port mapping)
EXPOSE 5000

# Run the application using Gunicorn (Keep your original CMD)
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "backend.wsgi:app"]