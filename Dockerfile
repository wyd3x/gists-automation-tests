FROM python:3.7-stretch

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

COPY . /automation

WORKDIR /automation

RUN pip install -r requirements.txt
