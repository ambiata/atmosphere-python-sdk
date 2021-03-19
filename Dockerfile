# Just used to run the tests
FROM python:3.8.5-slim

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

RUN chmod +x ./scripts/*.sh

ENV PYTHONPATH=/app
