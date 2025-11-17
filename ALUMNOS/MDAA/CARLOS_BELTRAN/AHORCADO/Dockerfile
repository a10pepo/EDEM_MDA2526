FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "ahorcado.py", "palabras.txt"]