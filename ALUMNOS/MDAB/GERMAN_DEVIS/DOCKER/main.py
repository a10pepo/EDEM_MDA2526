import sys

def add(a: int, b: int) -> int:
    return a + b


if len(sys.argv) != 3:
    print("Uso: python main.py <num1> <num2>")
    sys.exit(1)

try:
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
except ValueError:
    print("Error: ambos parámetros deben ser enteros.")
    sys.exit(2)

print(f"Sum: {add(n1, n2)}")