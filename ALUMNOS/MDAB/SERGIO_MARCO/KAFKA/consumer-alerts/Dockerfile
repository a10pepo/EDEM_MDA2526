FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer_alerts.py .

CMD ["python", "-u", "consumer_alerts.py"]
