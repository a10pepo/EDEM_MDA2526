FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip \
	&& pip install plotly pandas dash

COPY juntos.py tickets.csv ./

CMD ["python", "juntos.py"]