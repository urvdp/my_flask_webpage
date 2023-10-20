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
COPY --chown=jef:jef src app

#COPY src/__init__.py /home/source/code/

# switch to jef user
USER 1000

# setup app
RUN python -m app.setup

#expose port
EXPOSE 3031

# set default startup command (disabled for first testing)
CMD ["uwsgi --ini uwsgi.ini"]

# define entrypoint for example/test
#ENTRYPOINT FLASK_APP=__init__.py flask run --host=0.0.0.0



# setup directory for ssl keys and get keys stored in ssl folder
#RUN mkdir -p /home/source/ssl
#RUN openssl req -newkey rsa:2048 -nodes -keyout /home/source/ssl/domain.key -x509 -days 365  \
#    -out /home/source/ssl/domain.crt -subj "/C=DE/ST=Baden-Wuerttemberg/L=Karlsruhe/O=jef/OU=KIT SPZ/CN=localhost"
