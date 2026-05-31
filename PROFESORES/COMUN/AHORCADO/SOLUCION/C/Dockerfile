FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
COPY ahorcado.py .

RUN pip install -r requirements.txt

CMD ["python", "ahorcado.py"]
