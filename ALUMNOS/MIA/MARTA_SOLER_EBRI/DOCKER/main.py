import sys 

def suma(a,b):
    try:
        a=int(a)
        b=int(b)
        print(f"Suma: {a+b}")
    except ValueError:
        print("Debes introducir números.")
    
if __name__=="__main__":
    if len(sys.argv)!=3:
        print("Solo puedes pasar dos argumentos.")
    else:
        suma(sys.argv[1], sys.argv[2])