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
COPY --chown=jef:jef src code

# switch to jef user
USER 1000

#TODO: check if assets are needed

#expose port
EXPOSE 3031

# set default startup command
CMD ["uwsgi --ini uwsgi.ini"]
