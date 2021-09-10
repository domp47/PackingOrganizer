FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ="America/New York"

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools nginx python3-virtualenv

COPY requirements.txt /tmp/requirements.txt

RUN mkdir /app
COPY ./ /app
RUN rm -fr /app/env

RUN python3 -m virtualenv /app/env

RUN source /app/env/bin/activate && pip install -r /tmp/requirements.txt gunicorn

WORKDIR /app
ENV PATH=$PATH:/app/env/bin
ENTRYPOINT [ "/app/env/bin/gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "-m", "007", "wsgi:app" ]