import sys
def suma (a,b):
    return a + b
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python main.py <num1> <num2>")
    else:
        try:
            num1 = float(sys.argv[1])
            num2 = float(sys.argv[2])
            resultado = suma(num1, num2)
            print(f"Sum: {resultado}")
        except ValueError:
            print("Error: introduce solo números.")