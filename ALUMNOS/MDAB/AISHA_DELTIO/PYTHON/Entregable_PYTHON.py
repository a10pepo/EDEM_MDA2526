# # EJERCICIOS ENTREGABLES : PYTHON
# # AUTOR: AISHA DEL TIO DE PRADO
# terminal: py Entregable_PYTHON.py

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

