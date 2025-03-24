FROM python:3.12-slim
LABEL authors="Jan"

# add user
RUN useradd --create-home --shell /bin/bash --uid 1000 ubuntu

# Set the working directory
WORKDIR /home/app

# Install build dependencies (gcc for uwsgi)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc git \
    && rm -rf /var/lib/apt/lists/*

# Install the latest version of pip
RUN pip install --upgrade pip

# Copy the pdm.lock file
COPY requirements.txt ./
COPY uwsgi.ini ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ ./src/

# Set environment variables
ENV FLASK_APP=src/app/__init__.py

# Expose the port the app runs on
EXPOSE 3031

RUN chown -R ubuntu:ubuntu /home/app
USER ubuntu

# Run the application with uWSGI (we need to run it with pdm here, because pdm creates an isolated environment)
# uwsgi is not installed systemwide
CMD ["uwsgi", "--ini", "uwsgi.ini"]