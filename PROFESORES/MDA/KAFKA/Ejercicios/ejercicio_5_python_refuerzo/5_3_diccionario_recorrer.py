# ============================================
# EJERCICIO 3: RECORRER UN DICCIONARIO
# ============================================
# Vamos a recorrer un diccionario para mostrar sus claves y valores.

alumno = {
    "nombre": "Carlos",
    "edad": 22,
    "carrera": "ADE"
}

print("Recorriendo el diccionario alumno:")
for clave, valor in alumno.items():
    print(f"{clave}: {valor}")

print("Tipo de alumno:", type(alumno))
print("Tipo de items():", type(alumno.items()))

# ============================================
# EJERCICIOS:
# 1. Añade una clave "nota" con el valor 8.5 y vuelve a recorrer el diccionario.
# 2. Muestra solo las claves (usa alumno.keys()).
# 3. Muestra solo los valores (usa alumno.values()).

#1 Añadir clave "nota" y recorrer el diccionario
alumno["nota"] = 8.5
print("Recorriendo el diccionario alumno después de añadir 'nota':")
for clave, valor in alumno.items():
    print(f"{clave}: {valor}")

#2 Mostrar solo las claves
print("Claves del diccionario alumno:")
for clave in alumno.keys():
    print(clave)

#3 Mostrar solo los valores
print("Valores del diccionario alumno:")
for valor in alumno.values():
    print(valor)

