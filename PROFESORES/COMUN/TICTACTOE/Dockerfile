# Use an official Python runtime as a parent image
FROM python:3.14-alpine

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt ./

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run the Tic Tac Toe game
CMD ["python3", "game.py"]