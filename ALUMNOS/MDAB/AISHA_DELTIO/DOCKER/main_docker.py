import sys

def suma(a,b):
    return a + b

try:
    num1 = int(sys.argv[1])
    num2 = int(sys.argv[2])
    print(suma(num1, num2))
except:
    print("Error")

