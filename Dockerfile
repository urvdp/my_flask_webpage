FROM python:3.12-slim
LABEL authors="Jan"

# Install build dependencies (gcc for uwsgi)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc git \
    && rm -rf /var/lib/apt/lists/*

# Install the latest version of pip
RUN pip install --upgrade pip

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user
RUN useradd -m myuser
USER myuser

# Set environment variables
ENV FLASK_APP=src/my_flask_webpage/__init__.py
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 3031

# Run the application with uWSGI
CMD ["uwsgi", "--ini", "uwsgi.ini"]