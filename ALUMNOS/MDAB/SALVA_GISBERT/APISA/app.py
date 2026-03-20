import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
from flasgger import Swagger
from datetime import datetime

app = Flask(__name__)

# Configuración de Swagger
app.config['SWAGGER'] = {
    'title': 'Robot Temperature API',
    'uiversion': 3
}
swagger = Swagger(app)

def get_db_connection():
    """Establece conexión con la base de datos PostgreSQL en Docker"""
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'robot_db'),
        user=os.environ.get('DB_USER', 'user123'),
        password=os.environ.get('DB_PASS', 'password123')
    )
    return conn

@app.route('/getLastMeassureBySensor/<sensor>', methods=['GET'])
def get_last_measure(sensor):
    """
    Obtener la última medición de un sensor específico.
    ---
    parameters:
      - name: sensor
        in: path
        type: string
        required: true
        description: ID del sensor a consultar
    responses:
      200:
        description: Medición encontrada con éxito
      400:
        description: Sensor no encontrado
      404:
        description: ID de sensor inválido (muy corto)
    """
    # Validación 404: Supongamos que un ID válido debe tener al menos 3 caracteres
    if len(sensor) < 3:
        return jsonify({"message": "Invalid ID supplied"}), 404

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Buscamos la medición más reciente basada en la fecha
        query = """
            SELECT code, fechamuestreo, unidad, medicion 
            FROM sensor_data 
            WHERE code = %s 
            ORDER BY fechamuestreo DESC 
            LIMIT 1
        """
        cur.execute(query, (sensor,))
        result = cur.fetchone()
        
        cur.close()
        
        if result:
            # Formateamos la fecha para que sea un string legible en el JSON
            if isinstance(result['fechamuestreo'], datetime):
                result['fechamuestreo'] = result['fechamuestreo'].strftime("%Y-%m-%d %H:%M:%S")
            return jsonify(result), 200
        else:
            # Validación 400: El ID es válido pero no existe en la base de datos
            return jsonify({"message": "Sensor not found"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/addMeasure', methods=['POST'])
def add_measure():
    """
    Guardar una nueva medición de temperatura.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - code
            - fechamuestreo
            - unidad
            - medicion
          properties:
            code:
              type: string
              example: "sensor_01"
            fechamuestreo:
              type: string
              example: "2026-01-13 15:00:00"
            unidad:
              type: string
              example: "Celsius"
            medicion:
              type: number
              example: 36.5
    responses:
      201:
        description: Medición guardada correctamente
      400:
        description: Error en los datos enviados
    """
    data = request.get_json()
    
    # Verificación de campos requeridos
    required_fields = ['code', 'fechamuestreo', 'unidad', 'medicion']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"message": "Invalid input data"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            INSERT INTO sensor_data (code, fechamuestreo, unidad, medicion) 
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (
            data['code'], 
            data['fechamuestreo'], 
            data['unidad'], 
            data['medicion']
        ))
        
        conn.commit()
        cur.close()
        
        return jsonify({"message": "Medición guardada con éxito"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # host='0.0.0.0' es vital para que Docker pueda mapear el puerto
    app.run(host='0.0.0.0', port=5000, debug=True)
    