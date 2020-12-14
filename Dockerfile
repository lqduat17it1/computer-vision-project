# FROM ubuntu:16.04
FROM python:3.7-slim-stretch

MAINTAINER Your Name "Duat"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements-raspberry-pi.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt
# Install tflite_runtime
RUN pip install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp37-cp37m-linux_armv7l.whl

COPY . /app

# ENTRYPOINT [ "python" ]
ENV FLASK_APP app_lite
ENV FLASK_ENV development
ENV FLASK_DEBUG TRUE

CMD [ "flask", "run" ]
