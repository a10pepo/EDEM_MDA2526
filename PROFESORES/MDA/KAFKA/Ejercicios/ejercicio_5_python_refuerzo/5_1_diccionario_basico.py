# ============================================
# EJERCICIO 1: CREAR Y MOSTRAR UN DICCIONARIO
# ============================================
# Un diccionario en Python guarda pares clave-valor.
# Ejemplo: {"nombre": "Ana", "edad": 25}

persona = {
    "nombre": "Ana",
    "edad": 25,
    "ciudad": "Valencia"
}

print("Diccionario completo:", persona)
print("Tipo de persona:", type(persona))  # Muestra el tipo del objeto
print("Nombre:", persona["nombre"])
print("Tipo del nombre:", type(persona["nombre"]))  # Tipo del valor



# ============================================
# EJERCICIOS:
# 1. Añade una nueva clave "profesion" con el valor "Ingeniera".
# 2. Cambia la edad a 30.
# 3. Muestra la ciudad.


persona = {
    "nombre": "Ana",
    "edad": 30,
    "ciudad": "Valencia",
    "profesion": "Ingeniera"
}
print("Ciudad:", persona["ciudad"])
