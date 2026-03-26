# ============================================
# EJERCICIO 4: LISTA DE DICCIONARIOS
# ============================================
# Vamos a crear una lista que contiene varios diccionarios, con los simbolos python `[]`

alumnos = [
    {"nombre": "Ana", "nota": 9},
    {"nombre": "Luis", "nota": 7},
    {"nombre": "Marta", "nota": 8}
]

print("Lista de alumnos:", alumnos)
print("Tipo de alumnos:", type(alumnos))
print("Tipo del primer elemento:", type(alumnos[0]))

# Recorremos la lista mostrando nombre y nota
for alumno in alumnos:
    print(f"Alumno: {alumno['nombre']}, Nota: {alumno['nota']}")

# ============================================
# EJERCICIOS:
# 1. Añade un nuevo alumno con nombre "Pedro" y nota 9.
# 2. Calcula la nota media de todos los alumnos.
# 3. Muestra solo los nombres de los alumnos.
