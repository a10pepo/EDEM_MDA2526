FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

#ENV creates an environment variable inside the container called "archivoPalabras". the default variable is palabras.txt,
    # but it allows to use whatever .txt without changing the Docker image 
ENV archivoPalabras=palabras.txt 
CMD ["python", "ahorcado.py", "palabras.txt"]



