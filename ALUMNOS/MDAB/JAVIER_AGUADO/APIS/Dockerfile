FROM python:3.11-slim

WORKDIR /app2

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY last_pokemon_id.txt .
COPY mis_tweets.json .
COPY XPokemonAPI.py .

ENV APP_MODE=production

CMD ["python", "XPokemonAPI.py"]