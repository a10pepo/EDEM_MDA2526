import sys # Módulo que permite interactuar con el intérprete de Python

def suma():
    try:
        # Sys.argv --> argumentos pasados al script desde la línea de comandos
        # Float --> convertimos los argumentos a números
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])

        # Calculamos la suma
        resultado = num1 + num2

        # Imprimimos el resultado
        print(f"La suma de {num1} + {num2} es: {resultado}")

    except:
        print("Error")

# Llamada a la función 
suma()


