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
persona["profesion"] = "Ingeniera"

# 2. Cambia la edad a 30.
persona["edad"] = 30

# 3. Muestra la ciudad.
print("Ciudad:", persona["ciudad"])

# Mostramos el diccionario final para verificar los cambios
print("Diccionario actualizado:", persona)
