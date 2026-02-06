FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip \
	&& pip install plotly.graph_objects pandas plotly.express plotly.subplots

COPY tabla_ticket.py tickets.csv ./

CMD ["python", "tabla_ticket.py"]