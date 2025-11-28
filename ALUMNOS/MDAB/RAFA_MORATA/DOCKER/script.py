
import sys

if len(sys.argv) != 3:
    print("Uso: python main.py <num1> <num2>")
else:
    n1 = float(sys.argv[1])
    n2 = float(sys.argv[2])
    print(f"La suma es: {n1 + n2}")
