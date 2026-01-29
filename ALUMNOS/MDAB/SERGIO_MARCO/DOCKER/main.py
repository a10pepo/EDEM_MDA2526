import sys

def main():
    if len(sys.argv) != 3:                                                              #sys.argv es una lista que contiene: [0] Nombre del script main.py [1] y [2] Los argumentos que le pases (En este caso 2 argumentos)
        print("Has introducido más de 2 argumentos, por favor vuelve a intentarlo.")
        sys.exit(1)

    try:
        num1 = int(sys.argv[1])
        num2 = int(sys.argv[2])
        print(f"La suma es: {num1 + num2}")
    except ValueError:
        print("Por favor, introduce dos números válidos.")
        sys.exit(1)

if __name__ == "__main__":                                                              # Al ejecutar main.py Python asigna el valor especial "__main__" a la variable interna __name__
    main()                                                                              # Se ejecuta solo si el archivo se está ejecutando directamente, no si se está importando la función main
