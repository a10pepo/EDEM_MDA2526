import sys #Es una lista que contiene los argumentos que se pasan al script cuando se ejecuta desde la línea de comandos.

# Convierto los argumentos a números enteros
num1 = int(sys.argv[1])
num2 = int(sys.argv[2])
# Hago la suma 
suma = num1 + num2 
# Muestro el resultado
print(f"Sum: {num1 + num2}")