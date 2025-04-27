# Use Python 3.11 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y libssl1.1 libasound2 libffi7 || apt-get install -y libssl3 libffi8 || true
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]