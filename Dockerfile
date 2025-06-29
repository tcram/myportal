# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.12-slim-bookworm

# Add user that will be used in the container.
RUN useradd myportaluser

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=myportal.settings \
    PYTHONPATH=/app

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy the requirements first to leverage Docker cache
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install "gunicorn==20.1.0"

# Copy the source code of the project into the container.
COPY --chown=myportaluser:myportaluser . /app/

# Set directory ownership
RUN chown -R myportaluser:myportaluser /app

# Create the entrypoint script
COPY --chown=myportaluser:myportaluser <<'EOF' /app/docker-entrypoint.sh
#!/bin/bash
set -e

# Run the web server
echo "Starting web server..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn myportal.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --log-level debug \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance

EOF

RUN chmod +x /app/docker-entrypoint.sh

# Use user "myportaluser" to run the commands
USER myportaluser

# Set the entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]
