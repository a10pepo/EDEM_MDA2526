from confluent_kafka import Consumer
import json
from threading import Thread
import dash
from dash import html, dcc
import plotly.graph_objs as go