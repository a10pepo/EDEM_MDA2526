

import sys

def Suma(numero_1, numero_2):
    return numero_1 + numero_2

try:
    numero_1 = int(sys.argv[1])
    numero_2 = int(sys.argv[2])
    resultado = Suma(numero_1, numero_2)
    print(f"La Suma da como resultado:", resultado)

except:
    print("Haga el favor, e ingrese dos números válidos como parámetros.")