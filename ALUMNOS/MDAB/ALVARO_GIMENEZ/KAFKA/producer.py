#Creamos un script de python que simula la lógica de negocio
#Dado un sistema de gestión de almacén (SGA/WMS), las entregas de expedición pueden tener diferencias entre el pedido /n
#y lo realmente cargado. Como consecuencia necesitamos un sistema que nos alerte en tiempo real para poder avisar a los clientes /n
#y tomar decisiones. 

import time
import random
from kafka import KafkaProducer