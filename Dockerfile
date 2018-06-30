FROM python:3.6.5-alpine

ARG database_url
ARG redis_host
ENV DATABASE_URL $database_url
ENV REDIS_HOST $redis_host

RUN apk add --no-cache build-base \
                       python-dev \
                       mariadb-dev

RUN mkdir /code/
WORKDIR /code/

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY api/ api/
COPY ctf_platform/ ctf_platform/
COPY manage.py manage.py