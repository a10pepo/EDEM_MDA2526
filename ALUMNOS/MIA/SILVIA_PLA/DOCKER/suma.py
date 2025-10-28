import sys  
def numeros(num1, num2):
    return num1 + num2  
if len(sys.argv) != 3:
    print("Por favor, escribe dos números. Ejemplo: python suma.py 3 4")
    sys.exit(1)  
try:
    num1=float(sys.argv[1])
    num2=float(sys.argv[2])
except ValueError:
    print("Ambos argumentos deben ser números válidos.")
    sys.exit(1)              
resultado = numeros(num1, num2)
print(f"Suma: {resultado}")