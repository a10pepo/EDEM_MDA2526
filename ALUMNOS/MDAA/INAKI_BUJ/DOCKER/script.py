import sys

def suma(num1, num2):
    return f" La suma de {num1} y {num2} es {num1 + num2}"

num1= int(sys.argv[1])
num2= int(sys.argv[2])

print(suma(num1,num2))

