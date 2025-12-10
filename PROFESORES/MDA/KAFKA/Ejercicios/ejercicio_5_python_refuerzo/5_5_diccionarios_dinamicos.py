# =============================================
# EJEMPLO: Diccionarios dinámicos y f-strings
# =============================================
# Este script muestra cómo crear diccionarios dinámicos usando f-strings y condicionales.

# Ejemplo funcional:
for e in range(3):
    data = {
        'Proyecto': f'Innovación #{e+1}',
        'Presupuesto': f'{(e+1)*5000} EUR',
        'Estado': 'Aprobado' if e % 2 == 0 else 'En revisión'
    }
    print(data)

# =============================================
# EJERCICIOS:
# 1. Cambia el rango para generar 5 proyectos.
# 2. Añade una nueva clave al diccionario llamada 'Responsable' con el valor 'Equipo X'.
# 3. Haz que el presupuesto sea en dólares (USD) en lugar de EUR.

#1-2-3 Cambiar el rango para generar 5 proyectos
for e in range(5):
    data = {
        'Proyecto': f'Innovación #{e+1}',
        'Presupuesto': f'{(e+1)*5000} USD',  # Cambiado a USD
        'Estado': 'Aprobado' if e % 2 == 0 else 'En revisión',
        'Responsable': 'Equipo X'  # Nueva clave añadida
    }
    print(data)

