FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "generador.py"]

