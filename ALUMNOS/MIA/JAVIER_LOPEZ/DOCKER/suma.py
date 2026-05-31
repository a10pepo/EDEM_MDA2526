import sys

if len(sys.argv) != 3:
    print("Ejemplo de uso: docker run pysum <num1> <num2>")
    sys.exit(1)

try:
    num1 = float(sys.argv[1])
    num2 = float(sys.argv[2])
    print(f"La suma es: {num1 + num2}")
except ValueError:
    print("Error: Ambos argumentos deben ser números.")
