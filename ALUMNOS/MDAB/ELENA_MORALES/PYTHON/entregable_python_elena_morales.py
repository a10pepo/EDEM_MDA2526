# ENTREGABLE 🐍

# EJERCICIO 1

texto = "Marina de Empresa 2025"                  # Creo variable
print(f"Longitud:", len(texto), "letras")         # Longitud con len
print(f"Primera letra:", texto[0])                # Primera letra, con 0



# EJERCICIO 2

festivo = False

if festivo == True:
    print(f"¡¡Hoy es fiesta voy a echarme una siesta!!")
else:
    print(f"No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")



# EJERCICIO 4

def ultimoCaracter(texto):                              # texto = str
    if type(texto) != str:                              # != distinto de un str que es lo que queremos           
        return(f"Debo ser ejecutada con un string")
    else:
        return(texto[-1])                               # -1 para conseguir la ultima letra 
    
print(ultimoCaracter("'Voy a pasarmelo bien' es la cancion que estoy escuchando ahora"))
print(ultimoCaracter(23))



# EJERCICIO 5 -- BAD WORDS

# PUNTOS CLAVE: 
#    1. ESCRIBIMOS LA PALABRA
#    2. IGNORAMOS ESPACIOS Y MAYUSC/MINUSC
#    3. COMPRUEBA SI ESTA DENTRO DEL ARCHIVO bad_words.txt
#    4. NOS DEVUELVE "CORRECTA" o "NO CORRECTA" (si está en el archivo) o "...sin espacios" para que no pongamos espacios o no insertemos palabra
# THEN...


def norm(s):
    return s.strip().lower()                                # ESPACIOS Y MINUSC                      

bad = set()                                                 # GUARDAMOS EN EL SET VACIO
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()                                    # QUITAMOS ESPACIOS
        if w:
            bad.add(norm(w))                                # FUNCION QUE NORMALIZA LA PALABRA INTRODUCIDA


entrada_de_palabra = input("Introduce solo una palabra: ")

if entrada_de_palabra == "" or " " in entrada_de_palabra:    # SI TIENE ESPACIO O NO INTRODUZCO PALABRA
    print("Introduce una sola palabra (sin espacios).")
elif norm(entrada_de_palabra) in bad:                        # SI ESCRIBO UNA DE LAS TRES PALABRA QUE HE METIDO EN EL ARCHIVO BAD
    print("NO CORRECTA")
else:
    print("CORRECTA")