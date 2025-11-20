#Ejercicio 1
texto = "Marina de Empresas 2025"
print("------------------") 

print("Longitud del texto:", len(texto))

print("------------------") 

print("Primera letra:", texto[0])

print("------------------") 

#Ejercicio 2

festivo = False

if festivo == True:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

#Ejercicio 4

def ultimoCaracter(frase):

    if frase.isnumeric():
        return 'Debo ser ejecutada con un string'

    return frase[-1]
    
    

entrada = input("Introduce una frase y te devolverá el último carácter: ")
resultado = ultimoCaracter(entrada)
print("Resultado: ", resultado)

#Ejercicio 5

def norm(string: str) -> str:
    return string.strip().lower()


bad = set()
with open("bad_words.txt", encoding="utf-8") as file:
    for line in file:
        word = line.strip()
        if word and not word.startswith("#"):
            bad.add(norm(word))



palabra = input("Introduce una palabra: ")

if not palabra or " " in palabra.strip():
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_norm = norm(palabra)
    if palabra_norm in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")