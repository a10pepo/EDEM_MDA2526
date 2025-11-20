import sys

def sumar(a, b):
    "Devuelve la suma de dos números."
    return a + b

# Verificar que se pasen exactamente dos argumentos
if len(sys.argv) != 3:
    print("Uso: python pysum.py <numero1> <numero2>")
    sys.exit(1)

try:
    num1 = int(sys.argv[1])
    num2 = int(sys.argv[2])
except ValueError:
    print("Error: ambos argumentos deben ser números.")
    sys.exit(1)

resultado = sumar(num1, num2)
print(f"La suma de {num1} y {num2} es: {resultado}")