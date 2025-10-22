import sys
# print(sys.argv), len(sys.argv)      

def suma(numero1, numero2):
    return numero1 + numero2

try:
# 1. Obtenemos los argumentos de la línea de comandos
# sys.argv[1] es el primer número, sys.argv[2] es el segundo
    numero1 = int(sys.argv[1])
    numero2 = int(sys.argv[2])
# 2. Invocamos la función con los argumentos
    resultado = suma(numero1, numero2)
# 3. Imprimimos el resultado
    print(f"El resultado de la suma es: {resultado} ")

except:
    print("Ups, has cometido un error. Inténtalo de nuevo.")