# Use an official Python runtime as a parent image
FROM python:3.14-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Run the Tic Tac Toe game
CMD ["python3", "game.py"]