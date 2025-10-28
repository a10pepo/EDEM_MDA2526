import os, psycopg, string


# Conectar a la base de datos
try:
    #URL CONEXIÓN A BD 
    url = os.getenv("DATABASE_URL")
    #CONEXIÓN A BD
    connection = psycopg.connect(url)
    # Cursor
    cur = connection.cursor()
    print("BD conectada con éxito")
except Exception as e:
    print("Error conectando a la BD")
    print(e)

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






# # Inicializar la variable intento
# intentos = 0

# # Lista abecedario
# abecedario_es = list(string.ascii_uppercase) 
# indice_n = abecedario_es.index("N") 
# abecedario_es.insert(indice_n + 1, "Ñ")
# print(abecedario_es)


# # Leer las palabras del fichero e imprimirlas
# palabras = set()
# with open("palabras.txt", encoding="utf-8") as doc_palabras:
#     for line in doc_palabras:
#         palabra = line.strip()
#         n_letras = len(palabra)
#         for letra in abecedario_es:
#             intentos += 1
#             n_aparicion = palabra.count(letra)
#             n_letras = n_letras - n_aparicion
#             if n_letras == 0:
#                 break

# # Imprimimos el número de intentos
# print(intentos)