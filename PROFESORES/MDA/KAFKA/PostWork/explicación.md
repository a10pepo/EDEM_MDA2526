# ** PROCESAMIENTO DE DATOS METEOROLÓGICOS CON KAFKA DE EXTREMO A EXTREMO **

## 1. INTRODUCCIÓN
Este proyecto implementa un flujo de procesamiento de datos en tiempo real utilizando Apache Kafka.

El objetivo es:

Obtener datos de observación meteorológica en tiempo real de la AEMET.

Detectar alertas de ola de frío basadas en la temperatura máxima (tamax) y mínima (tamin).

Mostrar las alertas en formato JSON en un Consumer final.

Se implementa un flujo completo end-to-end, desde la ingesta de datos hasta la visualización de alertas, usando únicamente Python (Producer y Consumers).

## 2. CASO DE USO
**Monotorización meteorológica en tiempo real**:
- Detecta estaciones que registran temperaturas extremas (ola de frío).
- Genera alarmas automáticas para su posterior análisis o notificación. 

**Dataset**
- Fuente: https://opendata.aemet.es/opendata/api/observacion/convencional/todas/?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJnYmFsYWd1ZXJhZGVsbEBnbWFpbC5jb20iLCJqdGkiOiIwM2RhNGE3Mi05NGM3LTQyNDMtODUwMC00MjA1ZjdkZTI2MWEiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc2NDUyMzI3NywidXNlcklkIjoiMDNkYTRhNzItOTRjNy00MjQzLTg1MDAtNDIwNWY3ZGUyNjFhIiwicm9sZSI6IiJ9.taxd2E3Z42ljuYEi-U0tsBfHSuwl0cxiTLpMDg0vmso

- Campos clave:
ubi: nombre de la estación.
tamax: temperatura máxima.
tamin: temperatura mínima.
ta: temperatura actual.
hr: humedad relativa.
vmax, vv: velocidad máxima y media del viento.
idema, lat, lon, alt: identificador y coordenadas de la estación.

## 2.ARQUITECTURA IMPLEMENTADA.
      ┌────────────┐
      │  AEMET API │
      └──────┬─────┘
             │ Datos JSON
             ▼
    ┌─────────────────┐
    │ Producer (Python)│
    │ raw_weather      │
    └────────┬────────┘
             │
             ▼
  ┌─────────────────────┐
  │ Consumer Intermedio │
  │ Filtra ola de frío  │
  │ weather_alerts      │
  └────────┬────────────┘
             │
             ▼
    ┌────────────────┐
    │ Consumer Final │
    │ Muestra alertas│
    │ en JSON        │
    └────────────────┘

**Producer.py**: 
- Obtiene los datos de AEMET en formato JSON. 
- Publica cada registro en el tópico raw_weather. 

**Consumidor.py (consumidor intermedio)**:
- Lee raw_weather.
- Transforma los datos, filtra las estaciones con tmax<3 y tmin<0, añade un campo mensaje y envía al topic weather alerts.

**Consumidor_final.py**
- Publica en weather_alerts y únicamente muestra las alertas en terminal en formato JSON. 


## 3. EJEMPLOS DE JSON DE LOS MODELOS JSON REALIZADOS. 

**1. Producer.py**
Enviando mensaje a Kafka: {                             
  "idema": "3013",                                      
  "lon": -1.878928,                                     
  "fint": "2025-12-01T11:00:00+0000",                   
  "prec": 0.0,                                          
  "alt": 1061.72,                                       
  "vmax": 1.6,                                          
  "vv": 0.5,                                            
  "dv": 225.0,                                          
  "lat": 40.841653,                                     
  "dmax": 205.0,                                        
  "ubi": "MOLINA DE ARAG\u00d3N",                       
  "pres": 898.9,                                        
  "hr": 94.0,                                           
  "stdvv": 0.3,                                         
  "ts": 8.6,                                            
  "tamin": -1.3,                                        
  "ta": 1.7,                                            
  "tamax": 1.7,                                         
  "tpr": 0.9,                                           
  "vis": 20.0,                                          
  "stddv": 42.0,                                        
  "inso": 60.0,                                         
  "tss5cm": 3.8,                                        
  "pacutp": 0.0,                                        
  "tss20cm": 6.4,                                       
  "geo850": 1511.8                                      
}                                                       
Enviando mensaje a Kafka: {                             
  "idema": "3021Y",                                     
  "lon": -2.199722,                                     
  "fint": "2025-12-01T11:00:00+0000",                   
  "prec": 0.2,                                          
  "alt": 1250.46,                                       
  "vmax": 7.5,                                          
  "vv": 4.9,                                            
  "dv": 240.0,                                          
  "lat": 40.758333,                                     
  "dmax": 245.0,                                        
  "ubi": "ZAOREJAS",                                    
  "hr": 80.0,                                           
  "tamin": 4.3,                                         
  "ta": 5.4,                                            
  "tamax": 5.4                                          
}                 

**2. Consumer.py (consumer intermedio)**
Mensaje recibido: {'idema': 'C929I', 'lon': -17.88889, 'fint': '2025-12-01T21:00:00+0000', 'prec': 0.0, 'alt': 32.0, 'vmax': 12.4, 'vv': 9.9, 'dv': 30.0, 'lat': 27.818888, 'dmax': 30.0, 'ubi': 'EL HIERRO/AEROPUERTO', 'pres': 1017.7, 'hr': 62.0, 'stdvv': 0.6, 'pres_nmar': 1021.5, 'tamin': 20.6, 'ta': 20.7, 'tamax': 20.9, 'tpr': 13.2, 'stddv': 4.0, 'inso': 0.0}

**3. Consumer_final.py**
🚨 ALERTA DE TEMPERATURA 🚨
Estación: CERLER  COGULLA
Temperatura máxima: -0.6°C
Temperatura mínima: -0.9°C
Mensaje: ⚠️ Ola de frío: -0.6°C, min -0.9°C

## 4. EVIDENCIAS
![Después de ejecutar: python productor.py](image-1.png)
![Después de ejecutar: python productor.py](image.png)
![Después de ejecutar: python consumer.py](image-2.png)
![Despues de ejecutar: python consumer_final.py](image-3.png)
