import sys
import os #needed to read environmental variables
import time
import psycopg2
import requests #we use requests to call the API

API_KEY = os.getenv("RAE_API_KEY")

archivoPalabras = os.getenv("archivoPalabras", "palabras.txt") #os.getenv obtains the value of the environmental variable

letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
palabras = []

# this checks that in the terminal i've used palabras.txt when executing it
if len(sys.argv) < 2:
    print("Uso: python3 ahorcado.py <archivo_de_palabras>")
    exit(1)

# sys.argv[0] is ahorcado.py and sys.argv[1] is palabras.txt
archivoPalabras = sys.argv[1]

# opens the .txt and "moves" the words from the .txt to the list "palabras"
with open(archivoPalabras, "r") as archivo: #r means only read mode;
    for linea in archivo:
        palabra = linea.strip() #read line by line 
        if palabra:
            palabras.append(palabra)

if len(palabras) > 0:
    print("Palabras cargadas:", palabras)
else:
    print("Error. No se han cargado las palabras. Saliendo...")
exit

print("Conectando a la base de datos")
intentos_conexion = 0
conectado = False
while intentos_conexion < 5 and not conectado:
    try:
        conexion = psycopg2.connect(os.getenv("DATABASE_URL"))
        if conexion:
            print("Conexión exitosa a la base de datos")
            conectado = True
        cursor = conexion.cursor()
    except Exception as e:
        print("Error al conectar a la base de datos, reintentando...")
        print(e)
        intentos_conexion += 1
        time.sleep(10)
        if intentos_conexion == 5:
            print("No se pudo conectar a la base de datos después de varios intentos.")
            exit(1)

#create the table *"conexion" is the connection to the PostgreSQL database
def crearTabla(conexion):
    try:
        cursor=conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultadosAhorcado(
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        palabra VARCHAR(100) NOT NULL,
        letras_acertadas VARCHAR(100),
        letras_falladas VARCHAR(100),
        intentos INT NOT NULL,
        tiempo TIMESTAMP NOT NULL DEFAULT NOW ());

        """)
        cursor.close()
        conexion.commit()
    except Exception as e:
        print("Error al crear tabla: ", e)

print("Creando tabla de resultados si no existe")
crearTabla(conexion)

#insert the attempts into the table
def insertarIntento(conexion, palabra, letras_acertadas, letras_falladas, intentos):
    try:
        cursor=conexion.cursor()
        cursor.execute("""
        INSERT INTO resultadosAhorcado (palabra, letras_acertadas, letras_falladas, intentos)
        VALUES (%s, %s, %s, %s); """, (palabra, letras_acertadas, letras_falladas, intentos))
        cursor.close()
        conexion.commit()
    except Exception as e:
        print("Error al insertar intento: ", e)

def compruebaResultados(conexion):
    try:
        cursor=conexion.cursor()
        cursor.execute("SELECT COUNT (*) FROM resultadosAhorcado;") #it counts how many rows are there in the table "resultadosAhorcado"
        resultado = cursor.fetchone() #obtains the first result and prints it as a tuple, AKA in parenthesis
        print(f"Total de registros en la tabla resultadosAhorcado: {resultado[0]}") #we put [0] because we only want the first result of cursor.fetchone
        
        cursor.execute("SELECT * FROM resultadosAhorcado LIMIT 5;") 
        resultado = cursor.fetchall()
        print("Muestra los primeros 5 registros:")
        if resultado:
            for fila in resultado:
                print(fila)
            cursor.close()
            return resultado[0]
        else:
            print("No hay registros para mostrar")
            return None
    
    except Exception as e:
        print("Error al comprobar resultados: ", e)
        return 0

#* we don't do conexion.commit in this one because this function is just reading data from the database (we are just using "SELECT")
    # we just do commits when modifying data ("INSERT" "DELETE" "UPDATE")

print("##################################################")
print("Iniciando Ahorcado con Base de Datos")
print("##################################################")

#API : asks RAE website for a random word, reads the answer, converts it into text and gives back the word
def ObtenerPalabraAPI():
    url="https://rae-api.com/random"
    try:
        respuesta=requests.get( #like asking the browser for a website 
            "https://rae-api.com/api/random",
            headers={"Authorization": f"Token {API_KEY}"}) #this is something like a vip pass for entering the website (it's mandatory for some websites)         
        print("Respuesta RAE:", respuesta.text) #this shows exactly what the API will give back
        respuesta.raise_for_status() #if the API returns a 404 (error), python goes to the except 
        data = respuesta.json() #converts the info from the API into a dictionary (json)
        palabra = data["data"]["word"]
    except Exception as e:
        print("Error al llamar la API:", e)
        return None


while True:
    palabra = ObtenerPalabraAPI()
    if palabra is None:
        time.sleep(10)
        continue

    print("Palabra obtenida:", palabra)

    letras = list("ABCDEFGHIJKLMNÑOPQRSTVWXYZ")
    intentos = 0

    for palabra in palabras: #starts a loop that goes through every word in the .txt 
        aciertos = 0
        letrasAcertadas = ""
        letrasIncorrectas = ""

        for letra in letras: #starts a loop that goes through the letters in the list "letras" (checking if the letter is in the word)
            intentos +=1
            if letra in palabra:
                aciertos += palabra.count(letra) #palabra.count shows how many times the letters are in the word
                letrasAcertadas += letra 
            else:
                letrasIncorrectas += letra
            if aciertos == len(palabra):
                break

        insertarIntento(conexion, palabra, letrasAcertadas, letrasIncorrectas, intentos)

    print(f"Número de intentos:{intentos}")

    compruebaResultados(conexion)
    conexion.close()    