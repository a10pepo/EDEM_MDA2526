import sys
import psycopg
import os

def main():
    # Conexión a la base de datos
    database_url = os.getenv("DATABASE_URL", "postgresql://usuario:password@localhost:5432/ahorcado_db")
    connection = psycopg.connect(database_url)
    cur = connection.cursor()
    
    archivo = sys.argv[1] # Leemos el archivos palabras.txt como segundo argumento
    with open(archivo, "r", encoding="utf-8") as f: # Abrimos el fichero en modo lectura
        palabras = f.readlines() # Guardamos en "palabras" las lineas del fichero
            
    total_intentos = 0 # Inicializamos el contador de intentos totales

    print("Resultados del juego del ahorcado:")

    for palabra in palabras: # Recorremos todas nuestras palabras para intentar adivinarlas
        palabra = palabra.strip() # A cada linea le aplicamos el .strip() que elimina saltos de línea, dejando solamente la palabra
        letras_palabra = set(palabra) # Creamos un set de la palabra para saber cuántas letras únicas tiene (por si se repiten letras en la misma palabra)
        letras_acertadas = set() # Inicializamos un set donde guardaremos las letras que acertemos
        letras_falladas = set() # Inicializamos un set para las letras falladas
        intentos = 0  # Inicializamos los intentos para esta palabra
        for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": # Recorremos todas las letras del abc
            intentos += 1 # Añadimos un intento por cada letras que probamos
            if letra in letras_palabra: # Si esa letra está en nuestra palabra
                letras_acertadas.add(letra) # La añadimos al set de letras acertadas
            else:
                letras_falladas.add(letra) # Si no está, la añadimos a las falladas
            
            # Insertar en la base de datos
            cur.execute(
                "INSERT INTO intento_ahorcado (palabra, letras_acertadas, letras_falladas, intentos) VALUES (%s, %s, %s, %s)",
                (palabra, ''.join(sorted(letras_acertadas)), ''.join(sorted(letras_falladas)), intentos)
            )
            connection.commit()

            if letras_acertadas == letras_palabra: # Si ya hemos acertado todas la letras, es decir, nuestros set de letras de la palabra es igual que el set de letras acertadas
                break # Terminamos el bucle de búsqueda de letras porque ya hemos acertado la palabra

        total_intentos += intentos # Sumamos los intentos de esta palabra al contador de intentos total


        print(f"Palabra: {palabra} - Intentos: {intentos}")

    print("Suma total de intentos:", total_intentos)
    
    # Consultar los últimos 100 intentos
    print("\n--- Top 100 intentos registrados ---")
    cur.execute("SELECT id, palabra, letras_acertadas, letras_falladas, intentos, tiempo FROM intento_ahorcado ORDER BY id ASC LIMIT 100")
    resultados = cur.fetchall()
    
    for row in resultados:
        print(f"Palabra: {row[1]} | Acertadas: {row[2]} | Falladas: {row[3]} | Intentos: {row[4]} | Tiempo: {row[5]}")
    
    # Cerrar conexión
    cur.close()
    connection.close()

if __name__ == "__main__":
    main()