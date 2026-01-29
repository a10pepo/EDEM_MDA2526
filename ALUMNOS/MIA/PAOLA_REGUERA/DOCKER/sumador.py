import sys
def sumar_numeros(num1, num2):
    return num1 + num2
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python sumador.py <num1> <num2>")
        sys.exit(1)
    try:
        numero1 = float(sys.argv[1])
        numero2 = float(sys.argv[2])
    except ValueError:
        print("Por favor, ingrese dos números válidos.")
        sys.exit(1)
    resultado = sumar_numeros(numero1, numero2)
    print(f"La suma de {numero1} y {numero2} es {resultado}")