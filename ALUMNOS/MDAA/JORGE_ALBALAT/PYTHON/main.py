# EJERCICIO 1
variable1 = 'Marina de Empresas 2025'
print(len(variable1))
print(variable1[0])

# EJERCICIO 2
festivo = True
if festivo:
    print('Hoy es fiesta voy a echarme una siesta!!')
else:
    print('No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)')

# EJERCICIO 4
cadena = 'hola'
def ultimoCaracter(cadena):
    if type(cadena) != str:
        return 'Debo ser ejecutada con un string'
    else:
        return cadena[-1]
print(ultimoCaracter(cadena))

# EJERCICIO 5
def norm(s):
    s = s.strip()
    s = s.lower()
    return s
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))
palabra = input('Introduce una palabra:')
if ' ' in palabra:
    print('Introduce una sola palabra (sin espacios).')
else:
    palabra = norm(palabra)
    if palabra in bad:
        print('NO CORRECTA')
    else:
        print('CORRECTA')