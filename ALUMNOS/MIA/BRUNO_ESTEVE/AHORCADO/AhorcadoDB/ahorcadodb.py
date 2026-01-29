import os, psycopg, string, time


# URL de conexión a la base de datos
url = os.getenv("DATABASE_URL")

# Intentar conectar hasta que funcione
while True:
    try:
        connection = psycopg.connect(url)
        cur = connection.cursor()
        print("BD conectada con éxito")
        break  # sale del bucle si se conecta correctamente

    except Exception as e:
        print("Error conectando a la BD, reintentando en 3 segundos...")
        print(e)
        time.sleep(3)

# Crear la tabla
try:
    def crear_tabla():
        query = """CREATE TABLE IF NOT EXISTS resultados_ahorcado (
            palabra TEXT,
            letras_acertadas TEXT,
            letras_falladas TEXT,
            intentos INTEGER PRIMARY KEY,
            tiempo TIMESTAMPTZ NOT NULL DEFAULT now()
            );"""
        cur.execute(query)
        connection.commit()
        print("Tabla de resultados creada con éxito")
except Exception as e:
    print('Error creando la tabla de resultados')
    print(e)
    
crear_tabla()



# Inicializar la variable intento
intentos = 0

# Lista abecedario
abecedario_es = list(string.ascii_uppercase) 
indice_n = abecedario_es.index("N") 
abecedario_es.insert(indice_n + 1, "Ñ")


# Leer las palabras del fichero e imprimirlas
palabras = set()
with open("palabras.txt", encoding="utf-8") as doc_palabras:
    for line in doc_palabras:
        
        palabra = line.strip()
        
        n_letras = len(palabra)
        
        letras_acertadas = ""
        
        letras_falladas = ""
        
        for letra in abecedario_es:
            
            intentos += 1
            
            n_aparicion = palabra.count(letra)
            
            if n_aparicion == 0:
                letras_falladas += letra
            else: 
                letras_acertadas += letra
                
            cur.execute("""INSERT INTO resultados_ahorcado (palabra, letras_acertadas, letras_falladas, intentos) 
                VALUES (%s, %s, %s, %s)""", (palabra, letras_acertadas, letras_falladas, intentos) )
            
            connection.commit()
            
            n_letras = n_letras - n_aparicion
            
            if n_letras == 0:
                break                                  

# Calcular tiempo 
try:
    # Consulta SQL para calcular la duración total de TODO el script
    query_total_time = """
    SELECT
        MAX(tiempo) - MIN(tiempo) AS duracion_total_global
    FROM
        resultados_ahorcado;
    """
    
    # Ejecutar la consulta
    cur.execute(query_total_time)
    
    # Obtener el resultado (solo hay una fila)
    duracion_total = cur.fetchone()[0]
    
    print("\n--- Tiempo Total Global ---")
    print(f"La duración total de todos los procesos de adivinanza fue: {duracion_total}")

except Exception as e:
    print('Error al calcular el tiempo total en la BD')
    print(e)
finally:
    # Aseguramos el cierre de la conexión al final de todo
    if connection:
        connection.close()
        print("Conexión a la BD cerrada.")
