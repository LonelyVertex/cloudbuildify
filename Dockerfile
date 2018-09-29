FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY cloudbuildify /app/cloudbuildify

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "cloudbuildify.webhooks:app"]
