# =============================================
# EJEMPLO: Flujo completo (dict -> JSON -> bytes -> texto -> dict)
# =============================================
# Objetivo: Ver cómo los datos pasan por diferentes formatos:
# 1. dict (Python) -> 2. str (JSON) -> 3. bytes (binario) -> 4. str -> 5. dict
# =============================================

import json
from datetime import datetime

for e in range(3):
    # PASO 1: Creamos el diccionario con datos simulados
    data = {
        'Proyecto': f'Innovación #{e+1}',
        'Presupuesto': f'{(e+1)*5000} EUR',
        'Estado': 'Aprobado' if e % 2 == 0 else 'En revisión',
        'Fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha actual
    }
    print("\nDiccionario original:", data)
    print("Tipo:", type(data))  # dict

    # PASO 2: Convertimos el diccionario a JSON (texto)
    data_str = json.dumps(data)
    print("\nTexto JSON:", data_str)
    print("Tipo:", type(data_str))  # str

    # PASO 3: Convertimos el texto a bytes (para enviar por red)
    data_bytes = data_str.encode('utf-8')
    print("\nBytes (para Kafka/red):", data_bytes)
    print("Tipo:", type(data_bytes))  # bytes

    # PASO 4: Simulamos recepción y decodificación (bytes -> texto)
    recibido_str = data_bytes.decode('utf-8')
    print("\nTexto decodificado:", recibido_str)
    print("Tipo:", type(recibido_str))  # str

    # PASO 5: Convertimos el texto decodificado de nuevo a diccionario
    recibido_dict = json.loads(recibido_str)
    print("\nDiccionario reconstruido:", recibido_dict)
    print("Tipo:", type(recibido_dict))  # dict

# =============================================
# EJERCICIOS:
# 1. Cambia el rango a 5 en lugar de 3.
# 2. Añade una lista de sensores al diccionario (por ejemplo ['Temperatura', 'Presión']).
# 3. ¿Qué pasa si añades un emoji en el valor de 'Estado'? ¿Se mantiene con UTF-8?
# 4. Imprime los tipos en cada paso para confirmar la transformación.