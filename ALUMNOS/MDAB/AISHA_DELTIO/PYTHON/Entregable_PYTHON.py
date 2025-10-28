# # EJERCICIOS ENTREGABLES : PYTHON
# # AUTOR: AISHA DEL TIO DE PRADO


# # EJERCICIO 1:
# Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025”
# Muestra por consola la longitud de la variable
# Utilizando esa variable muestra por consola la primera letra.

edem = "Marina de Empresas 2025"

longitud_edem = len(edem)
print(f'El término "Marina de Empresas 2025" tiene una longitud de {longitud_edem} ')

primera_edem = edem[0]
print(f'La primera letra de "Marina de Empresas 2025" es {primera_edem} ')



# # EJERCICIO 2:
# Define una variable festivo que sea de tipo booleano.
# Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” 
# y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”

festivo = True

if festivo == True:
    print('Hoy es fiesta voy a echarme una siesta!!')
else:
    print('No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)')



# # EJERCICIO 3:
# Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
# Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.    

def ultimoCaracter(palabra):
    if type(palabra) == str:
        ultimo_crc = palabra[-1]
        return f'El ultimo caracter de la palabra {palabra} es : {ultimo_crc}'
    else:
        return f'Debo ser ejecutada con un string'
        
print(ultimoCaracter("Aisha"))
print(ultimoCaracter(7))    
    
    

# # EJERCICIO 4:
# Escribe un programa que pida una palabra por teclado y diga si está en la lista de palabras prohibidas (bad_words.txt). 
# La comparación debe ser insensible a mayúsculas .


# Normalizacion: convierte a minúsculas y quita espacios al inicio y al final
def norm(s: str):
    return s.lower().strip()

# Codigo profesora
bad = set()
with open("bad_words.txt", encoding="utf-8") as f: # abrimos el archivo
    for line in f: # recorremos el archivo linea por linea
        w = line.strip() # eliminamos espacios en blanco y saltos de línea al principio y al final
        if w:
            bad.add(norm(w))

# Entrada: pide al usuario una sola palabra 
palabra = input('Escribe una única palabra: ')

# Validacion: Si la entrada está vacía o contiene espacios termina el programa
if palabra == '' or ' ' in palabra:
    print(f'Introduce una sola palabra (sin espacios).')
else:
    if norm(palabra) in bad: # normalizacion + comrpobacion 
        print('NO CORRECTA') # si pertenece, la palabra no es correcta
    else:
        print('CORRECTA') # si no pertenece, la palabra es correcta

    


            
            
            
            