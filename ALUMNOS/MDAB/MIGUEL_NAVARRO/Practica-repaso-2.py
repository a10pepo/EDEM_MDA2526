"""
EJERCICIOS BÁSICOS DE PYTHON
CLASE 1
"""

gente = [
    {"nombre": "Jamiro", "edad": 45},
    {"nombre": "Juan",   "edad": 35},
    {"nombre": "Paco",   "edad": 34},
    {"nombre": "Pepe",   "edad": 14},
    {"nombre": "Pilar",  "edad": 24},
    {"nombre": "Laura",  "edad": 24},
    {"nombre": "Jenny",  "edad": 10},
]

print("\nNivel 1 - Bucles")
# 1) Crea una lista con la gente que su nombre tiene 4 letras.
nombre4letras = [] # Creo la lista vacía
for persona in gente:
    if len(persona["nombre"]) == 4:
        nombre4letras.append(persona)
print(f"1) Personas cuyo nombre tiene 4 letras: {nombre4letras}")

# 2) Crea una lista con la gente que su nombre empieza por J y sean menores de 40 años.
nombre_J_menor40 = []
for persona in gente:
    if persona["nombre"].startswith("J") and persona["edad"] < 40:
        nombre_J_menor40.append(persona)
print(f"2) Personas menores de 40 años, cuyo nombre empieza por J: {nombre_J_menor40}")

print("\nNivel 2 – Funciones")
# 3) Crea una función resta que espere dos parámetros a y b y que devuelva la resta de los mismos.
def resta (a, b): # defino la función
    """
    Devuelve la resta de a - b
    """
    return f"Resultado de resta {a} - {b} = {a - b}"
resultado = resta (10,4) # llamo a la función y guardo el resultado
print(f"3) {resultado}")

# 4) Crea la función duplicaNumero debe recibir un tipo number y devolver el doble del valor recibido.
# Si la función no recibe un dato tipo number debe devolver el string ‘Debo ser ejecutada con un número’
def duplicaNumero(a: int | float): # defino la función
    """
    Devuelve el doble del número introducido.
    Si no recibe un número, devuelve un mensaje de error
    """
    if isinstance(a, (int | float)):
        return f"Resultado de duplicar {a}: {a * 2}"
    else:
        return "Debo ser ejecutada con un número"
resultado = duplicaNumero(7) # llamo a la función y guardo el resultado
print(f"4) {resultado}")

# 5) Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
# Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.
# Si recibe un string vacío debe devolver 'Debo ser ejecutada con un string no vacío'
def ultimoCaracter (string: str): # defino la función
    """
    Devuelve el último carácter de la string introducida.
    Válida si recibe un string no vacío.
    """
    if not isinstance(string, str):
        return "Debo ser ejecutada con un string"
    if string == "":
        return "Debo ser ejecutada con un string no vacío"
    return f"'{string[-1]}' es el último carácter de la string '{string}'"
resultado = ultimoCaracter("pez") # llamo a la función y guardo el resultado
print(f"5) {resultado}")

# 6) Crea la función cuentaCaracteres debe recibir un tipo string y devolver un number con el número de carácteres
# Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'
def cuentaCaracteres(string: str):
    """
    Devuelve el valor numérico de la longitud de un string introducido.
    Si no recibe un dato tipo string, devuelve un mensaje de error
    """
    if not isinstance(string, str):
        return "Debo ser ejecutada con un string"
    return len(string)
resultado = f"La string 'Python' tiene {cuentaCaracteres("Python")} carácteres"
print(f"6) {resultado}")
