# Just used to run the tests
FROM python:3.8.5-slim

WORKDIR /app/atmosphere

COPY atmosphere/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY atmosphere /app/atmosphere/
RUN chmod +x ./scripts/*.sh

ENV PYTHONPATH=/app
