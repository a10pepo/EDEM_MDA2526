import sys

numero1 = sys.argv[1]
numero2 = sys.argv[2]

try:
	numero1 = float(numero1)
	numero2 = float(numero2)
except ValueError:
	print("Los dos argumentos deben ser numeros")
	sys.exit(1)

print(f"La suma de los parametros es: {numero1 + numero2}")