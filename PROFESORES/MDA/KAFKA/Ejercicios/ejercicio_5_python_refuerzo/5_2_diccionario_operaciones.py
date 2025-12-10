# ============================================
# EJERCICIO 2: OPERACIONES CON DICCIONARIOS
# ============================================
# Vamos a practicar cómo añadir, modificar y eliminar elementos/atributos con código Python.

producto = {
    "nombre": "Portátil",
    "precio": 1200,
    "stock": 10
}

print("Producto inicial:", producto)
print("Tipo de producto:", type(producto))

# Añadir una nueva clave
producto["marca"] = "Lenovo"
print("Producto con marca:", producto)

# Modificar el precio
producto["precio"] = 1100
print("Producto con precio actualizado:", producto)

# Eliminar la clave "stock"
del producto["stock"]
print("Producto sin stock:", producto)

# ============================================
# EJERCICIOS:
# 1. Añade una clave "color" con el valor "gris".
# 2. Cambia la marca a "HP".
# 3. Elimina la clave "precio".

producto["color"]="gris"
producto["marca"]="HP"
del producto["precio"]
print("Producto final:", producto)
