FROM python:3.7-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apk add build-base
RUN apk add postgresql-dev
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
