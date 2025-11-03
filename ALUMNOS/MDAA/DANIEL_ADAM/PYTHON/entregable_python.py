# ENTREGABLE PYTHON
# Ejercicio 1 --------------------------

texto = 'Marina de Empresas 2025'

print(len(texto))

print(texto[0])

# Ejercicio 2 --------------------------

festivo: bool = False
if festivo == True:
    print('Hoy es fiesta voy a echarme una siesta!!')
else:
    print('No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)')

# Ejercicio 4 --------------------------

def ultimoCaracter():
    palabra = input('Introduce una palabra para devolver el último caracter: ')
    if type(palabra) == str:
        print(palabra[-1])
    else:
        print('Debo ser ejecutada con un string')

ultimoCaracter()

# Ejercicio 5 --------------------------

def norm(s: str) -> str:
    try:
        lower = s.lower()
        clean = lower.strip()
        if not clean or ' ' in clean:
            exit()
        else:
            return clean
    except:
        print('Introduce una sola palabra (sin espacios).')
        exit()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

word = input('Introduce una palabra: ')

norm_word = norm(word)

if norm_word in bad:
    print('NO CORRECTA')
else:
    print('CORRECTA')



