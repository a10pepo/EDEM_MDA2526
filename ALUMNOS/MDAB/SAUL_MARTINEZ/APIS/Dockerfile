FROM python:3.14-slim
WORKDIR /app

COPY botx.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "botx.py"]