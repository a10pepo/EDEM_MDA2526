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
