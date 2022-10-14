FROM python:3.8

WORKDIR /app


COPY requirements.txt requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN pip3 install "fastapi[all]" SQLAlchemy psycopg2-binary
RUN pip3 install -r requirements.txt

COPY . .

