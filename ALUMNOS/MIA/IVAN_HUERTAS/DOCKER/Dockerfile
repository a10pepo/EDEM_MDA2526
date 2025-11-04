FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]


#the difference between compose up and compose down is that up creates and starts containers, while down stops and removes them.
