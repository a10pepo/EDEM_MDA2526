### EJERCICIO 1

var = 'Marina de Empresas 2025'

print(len(var))

print(var[0])

### EJERCICIO 2

festivo = False

if festivo==True:
    print('Hoy es fiesta voy a echarme una siesta!!')
else:
    print('No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)')

### EJERCICIO 4

def ultimoCaracter(var:str):
    if type(var)== str:
        res =var[-1]
    else:
        res = 'Debo ser ejecutada con un string'
    return res

### EJERCICIO 5

def norm(s:str):
    minus = s.lower().strip()
    return minus

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

word= input('Introduce una sola palabra: ')
word = norm(word)

if not word.strip() or ' ' in word:
    print('Introduce una sola palabra (sin espacios).')
elif word in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")






