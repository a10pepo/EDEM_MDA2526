FROM python:3.11-slim
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "ahorcado.py", "palabras.txt"]
