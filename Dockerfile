FROM ubuntu:16.04

MAINTANER Your Name "Duat"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# ENTRYPOINT [ "python" ]
ENV FLASK_ENV development
ENV FLASK_DEBUG TRUE

CMD [ "flask", "run" ]