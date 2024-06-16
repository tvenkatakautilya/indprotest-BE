# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Copy the rest of the application code into the container
COPY . /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


COPY ./gunicorn_config.py /app/

COPY ./static /

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "entrypoint.sh" ]
