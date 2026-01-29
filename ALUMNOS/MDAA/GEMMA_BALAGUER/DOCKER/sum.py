import sys

if len(sys.argv) != 3:
    print("Uso: python sum.py <num1> <num2>")
    sys.exit(1)

num1 = float(sys.argv[1])
num2 = float(sys.argv[2])

print(f"Sum: {num1 + num2}")
