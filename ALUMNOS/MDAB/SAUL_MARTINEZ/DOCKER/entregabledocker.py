import sys

def suma (a,b):
    return a+b

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Inserta dos números para sumarlos")
        sys.exit(1)

a = int(sys.argv[1])
b = int(sys.argv[2])
print(suma(a, b))
