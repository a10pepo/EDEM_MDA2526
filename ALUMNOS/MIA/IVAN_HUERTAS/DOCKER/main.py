import sys
def sumar(a,b):
    return a + b
try:
    a=int(input("Introduce dos numeros para sumar: "))
    b=int(input())
    print(sumar(a,b))
except:
    print("Introduce 2 numeros válidos")
