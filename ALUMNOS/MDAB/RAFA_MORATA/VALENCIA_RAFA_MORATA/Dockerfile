FROM python:3.9-slim
WORKDIR /app
RUN pip install requests psycopg2-binary
COPY valenbisi_collector.py .
CMD ["python", "-u", "valenbisi_collector.py"]