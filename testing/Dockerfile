FROM python:latest

WORKDIR /testing/

RUN apt-get update && \
    apt-get install -y git && \
    apt-get upgrade -y

RUN pip3 -q install pip --upgrade

