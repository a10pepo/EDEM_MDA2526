# -----------
# Base image
# -----------
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------
# Set workdir
# -----------
WORKDIR /app

# -----------
# Install system dependencies (minimal)
# -----------
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# -----------
# Install Python dependencies
# -----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------
# Copy application code
# -----------
COPY twitter_bot.py .

# -----------
# Run the bot
# -----------
CMD ["python", "twitter_bot.py"]
