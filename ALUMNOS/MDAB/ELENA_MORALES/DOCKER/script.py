import sys
print(sys.argv), len(sys.argv)      


def suma(numero1, numero2):
    return numero1 + numero2

try:
    numero1 = int(sys.argv[1])
    numero2 = int(sys.argv[2])
    print(f"El resultado de la suma es: " [suma])

except:
    print("Ups, has cometido un error. Inténtalo de nuevo.")