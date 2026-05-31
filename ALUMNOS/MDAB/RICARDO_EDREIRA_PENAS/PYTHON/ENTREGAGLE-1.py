
# EJERCICIO 1: 
informacion = "Marina de Empresas 2025"
longitud = len(informacion)
print(f'La longitud de la variable es: {longitud}')

primera_letra = informacion[0]
print(f'La primera letra es: {primera_letra}')

# EJERCICIO 2:
festivo = True 
if festivo:
    print('Hoy es fiesta voy a echarme una siesta!!')
else:
    print('No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)')

# EJERCICIO 4:

def ultimoCaracter(palabra):
   
    if type(palabra) == str:
        return f"El último carácter es: {palabra[-1]}"
    else:
        return 'Debo ser ejecutada con un string'

# Prueba:
print(ultimoCaracter("Desarrollo"))
print(ultimoCaracter(12345))

# EJERCICIO 5: Bad Words

def norm(s: str) -> str:
    return s.lower().strip()

bad = set()
try:
    with open("bad_words.txt", encoding="utf-8") as f:
        for line in f:
            w = line.strip() 
            if w: 
                bad.add(norm(w))
except FileNotFoundError:
    print("Error: Asegúrate de que 'bad_words.txt' existe en el directorio.")

palabra = input('Escribe una única palabra para comprobar: ')

if not palabra or ' ' in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_normalizada = norm(palabra)
    if palabra_normalizada in bad:
        print('NO CORRECTA') # La palabra está prohibida
    else:
        print('ES CORRECTA') # La palabra esta aceptada