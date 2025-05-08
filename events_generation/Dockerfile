FROM python:3.10-slim
COPY ./requirements.txt .
RUN apt-get update && apt-get upgrade
RUN apt-get install -y python3-dev gcc libc-dev librdkafka-dev
RUN pip install -r requirements.txt
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . .
