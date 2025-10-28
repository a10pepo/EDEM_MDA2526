import sys

def suma(num1,num2):
  resultado = num1+num2
  return print(f"El resultado es: {resultado}")

if len(sys.argv) == 3:
    numero1 = int(sys.argv[1])
    numero2 = int(sys.argv[2])
else:
    print("Sum: ")
    numero1=int(input("Numero uno: "))
    numero2=int(input("Numero dos: "))

suma(numero1,numero2)
