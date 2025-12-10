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

#1 Añadir un nuevo alumno
alumnos.append({"nombre": "Pedro", "nota": 9})
print("Lista de alumnos después de añadir a Pedro:", alumnos)

#2 Calcular la nota media
suma_notas = 0
for alumno in alumnos:
    suma_notas += alumno["nota"]
nota_media = suma_notas / len(alumnos)
print(f"Nota media de los alumnos: {nota_media}")

#3 Mostrar solo los nombres de los alumnos
print("Nombres de los alumnos:")
for alumno in alumnos:
    print(alumno["nombre"])
