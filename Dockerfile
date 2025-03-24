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
RUN pip install --no-cache-dir --upgrade pip

# install pdm
RUN pip install --no-cache-dir pdm>=2.4.3

# Copy the pdm.lock file
COPY pyproject.toml pdm.lock ./
COPY uwsgi.ini ./
COPY README.md ./

# install the dependencies via pdm.lock file
RUN pdm install --frozen-lockfile

# Copy the application code
COPY src/* ./code/

# Set environment variables
ENV FLASK_APP=app.py
#ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 3031

RUN chown -R ubuntu:ubuntu /home/app
USER ubuntu

# Run the application with uWSGI (we need to run it with pdm here, because pdm creates an isolated environment)
# uwsgi is not installed systemwide
CMD ["pdm", "run", "uwsgi", "--ini", "uwsgi.ini"]