# FROM python:3.11
# RUN pip install django==3.2
# COPY . . 
# RUN python manage.py migrate
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]


# FROM python:3.11-slim
# # Set work directory
# WORKDIR /app
# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# # Copy project files
# COPY . .
# # Set environment variables
# ENV PYTHONUNBUFFERED=1
# ENV PORT=8000
# # Expose the port Render will use (not strictly required)
# EXPOSE 8000
# # Start Django with Render's PORT
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT"]

FROM python:3.11-slim
# Set work directory
WORKDIR /app
# Install system dependencies (for psycopg2 and Pillow if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy project files
COPY . .
# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
# Collect static files at build time
RUN python manage.py collectstatic --noinput
# Expose port
EXPOSE 8000
# Run migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn todoApp.wsgi:application --bind 0.0.0.0:$PORT --workers 3"]
