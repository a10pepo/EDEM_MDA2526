FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip \
	&& pip install pandas plotly

COPY visualizacion.py tickets.csv ./

CMD ["python", "visualizacion.py"]