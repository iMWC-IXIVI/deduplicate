FROM python:3.12-slim

WORKDIR /usr/src/app

COPY req.txt ../req.txt

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r ../req.txt

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
