import sys

def suma(a,b):
    try:
        a=int(a)
        b=int(b)
        print(f"Suma: {a+b}")
    except ValueError:
        print("Error, introduce números.")
    
if __name__=="__main__":
    if len(sys.argv)!=3:
        print("Utiliza sólo dos argumentos.")
    else:
        suma(sys.argv[1], sys.argv[2])
    