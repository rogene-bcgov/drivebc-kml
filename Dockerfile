# Dockerfile for DriveBC KML Service (Alternative hosting option)

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service script
COPY drivebc_service.py .

# Create output directory
RUN mkdir -p /app/public

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run service every 30 minutes using cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Create cron job
RUN echo "*/30 * * * * cd /app && python drivebc_service.py > /app/public/drivebc_events.kml" | crontab -

# Expose port for serving files (if using nginx or similar)
EXPOSE 80

# Start cron daemon
CMD ["cron", "-f"]
