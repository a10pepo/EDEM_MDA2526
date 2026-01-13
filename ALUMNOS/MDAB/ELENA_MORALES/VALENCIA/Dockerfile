FROM python:3.11-slim
WORKDIR /app

COPY valenbisi.py .

RUN pip install --no-cache-dir requests psycopg2-binary
CMD ["python","valenbisi.py"]