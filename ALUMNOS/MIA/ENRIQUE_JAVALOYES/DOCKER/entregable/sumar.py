import sys

n1 = sys.argv[1]
n2 = sys.argv[2]

def sumar(n1,n2):

    suma= int(n1) + int(n2)
    return suma

print(f'{n1}+{n2} = {sumar(n1,n2)}')

