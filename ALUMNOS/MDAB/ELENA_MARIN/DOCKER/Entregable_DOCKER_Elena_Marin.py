# Construir un script en python que acepte dos números como parámetros e imprima el resultado de la suma

import sys

if len(sys.argv) <= 2:
    print("python3 Entregable_DOCKER_Elena_Marin.py <numero1> <numero2>")
else:
    numero1 = int(sys.argv[1])
    numero2 = int(sys.argv[2])

resultado = numero1 + numero2

print(f"Sum: {resultado}")
