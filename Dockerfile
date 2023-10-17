# base information
FROM python:3.11-slim
MAINTAINER Jan Fenker

# create user
RUN useradd --home-dir /home/source --create-home --shell /bin/bash --uid 1000 jef

# set workdir
WORKDIR /home/source/code

# upgrade system and install requirements (normal and build)
RUN apt-get update && \
    mkdir -p /usr/share/man/man1 && \
    mkdir -p /usr/share/man/man7 && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends fonts-dejavu gcc libc-dev git gpg libmagic1 libpq-dev postgresql-client xz-utils && \
    pip install -U pip setuptools --no-cache-dir && \
    rm -rf /root/.cache /var/cache/*

# install python requirements and do cleanup
COPY requirements.txt requirements.txt
RUN pip install -U -r requirements.txt --no-cache-dir && \
    rm -rf /root/.cache /var/cache/*

#create state directory
RUN mkdir /state && \
    chown -R jef:jef /state

# copy code & config
COPY --chown=jef:jef uwsgi.ini uwsgi.ini
COPY src/__init__.py /home/source/code/
COPY src/setup.py /home/source/code/
#--chown=jef:jef src code
#COPY ../my_docker_webserver/nginx.conf /home/source/

# switch to jef user
USER 1000

#TODO: check if assets are needed

#expose port
#EXPOSE 3031

# set default startup command (disabled for first testing)
#CMD ["uwsgi --ini uwsgi.ini"]

# define entrypoint for example/test
ENTRYPOINT FLASK_APP=__init__.py flask run --host=0.0.0.0
#python -m __init__



# setup directory for ssl keys and get keys stored in ssl folder
RUN mkdir -p /home/source/ssl
RUN openssl req -x509 -nodes -newkey rsa:2048 -keyout /home/source/ssl/key.pem -out /home/source/ssl/cert.pem -sha256 -days 365 \
    -subj "/C=GB/ST=London/L=London/O=Alros/OU=IT Department/CN=localhost"
