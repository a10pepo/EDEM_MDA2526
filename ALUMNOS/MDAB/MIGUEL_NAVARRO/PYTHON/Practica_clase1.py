"""
EJERCICIOS BÁSICOS DE PYTHON
CLASE 1 DE PYTHON
26/09/2025
"""


# print("EJERCICIO 1")

# calle: str = "Marina Baixa"
# numero: int = 3
# ciudad: str = "Valencia"
# codigo_postal: int = 46015
# direccion = f"{calle}, {numero}, {ciudad} {codigo_postal}" # concateno
# print(direccion)
# cadena = '"Esta es mi cadena"' # string con comillas internas
# print(cadena)
# print(f"La cadena {cadena} tiene una longitud de {len(cadena)} caracteres")


# print("EJERCICIO 2")

# mi_variable = "Economía" # CORRECTA
# otra_var = "Ejercicio" # le falta la comilla (") al final
# # True = "Ejercicio" # True es una palabra reservada, no se puede utilizar como nombre de variable
# mi_variab1e = "Alpha" # el nombre de una variable no puede contener espacios ( )
# # import = 40 # import es una palabra reservada, no se puede utilizar como nombre de variable
# mi_variable81 = "Agua" # el nombre de una variable no puede empezar por un número
# mi_variable10 = 6 # CORRECTA


# print("EJERCICIO 3")

# num1: int = 10
# num2: float = 5.5
# print(type(num1))
# print(type(num2))
# suma = num1 + num2
# print(suma)
# print(type(suma)) # la suma es de tipo string
# # si elimino las 2 primeras variables, no se pueden hacer las operaciones ni obtener la variable resultante


# print("EJERCICIO 4")

# print("4.1 OPERADORES ARITMÉTICOS (suma, resta, multiplicación, división, módulo, potencia):")
# # VARIABLES:
# a = 10
# b = 3
# suma = a + b
# resta = a - b
# multi = a * b
# div = a / b
# modulo = a % b
# B41 = (a + b) * 2 - 5
# C41 = a // b 
# D41 = a ** 0.5
# E41 = a ** b
# print("Ejercicio 4.1")
# print("A.", suma, resta, multi, div, modulo)
# print(f"B. Resultado = {B41}")
# print("C.",C41)
# print("D.", D41)
# print("E.", E41)

# 4.2 OPERADORES CON COMPARACIÓN (==, !=, >, <, >=, <=):
# VARIABLES:
# a = 10
# b = 3
# A42 = a == b
# B42 = a != b
# C42 = a > b
# D42 = b <= a
# E42 = a + 5 >= b * 2
# print("Ejercicio 4.2.")
# print(A42, B42, C42, D42, E42)

# 4.3 OPERADORES LÓGICOS (and, or, not):
# VARIABLES:
# a = 10
# b = 3
# A43 = a > 5 and b < 5
# B43 = a < 5 or b < 5
# C43 = not a == b
# D43 = a > 5 and a != 10
# print(A43,
#       B43,
#       C43,
#       D43)
# # VARIABLES NUEVAS:
# A = 4
# B = "Text"
# C = 4.1
# print(A == B,
#       not A == C,
#       A > C,
#       C <= A,
#       not B == C)

# 4.4 OPERADORES DE PERTENENCIA (in, not in)
# lista = [1, 2, 3, 4, 5, 6]
# print(3 in lista)
# print(6 not in lista)
# texto = "python"
# print("y" in texto)
# print("z" in texto)

# 4.5 OPERADORES DE ASIGNACIÓN (=, +=, -=, *=, /=, %=, **=, //=)
# x = 10
# print(x)
# x += 5
# print(x)
# x -= 3
# print(x)
# x *= 2
# print(x)
# x /= 4
# print(x)
# x %= 3
# print(x)
# x **= 3
# print(x)
# x // 2
# print(x)


# EJERCICIO 5

# base = "A quien madruga, Dios le ayuda"
# print(base.upper()) # TODAS MAYÚSCULAS
# print(base.lower()) # todas minúsculas
# print(base.title()) # Iniciales Mayúsculas
# lista_base = base.split(" ") # Crea una lista dividiendo por los espacios
# print(lista_base)
# print(base.replace(",", ";")) # Sustituye las comas (,) por puntos y comas (;)
# print(base.replace("a","")) # Elimina las "a" minúscula (las he sustituido por nada)


# EJERCICIO 6

# puntuación: int = 9
# nombre_equipo: str = "ValenciaCF fútbol"
# promedio_tiempo: float = 8.5
# es_habil: bool = True
# lista_compras: list [str] = ["pechuga", "hummus", "zanahoria", "plátano", "salmón"]
# tupla_mascotas: tuple = (("Tana", 8, "perro"), ("Lando", 5, "gato"))
# dict_contactos: dict = {
#     "amigos": ["Carlos Gil Cebrián", "Salvador Gisbert Tararí"],
#     "telefonos": [987654321, 123456789],
#     "emails": ["carlosgilva21@gmail.com", "salvagis@gmail.com"]
#     }
# lista_actividades: list = []
# lista_actividades.append([puntuación, nombre_equipo, promedio_tiempo, es_habil, lista_compras, tupla_mascotas, dict_contactos])
# print(lista_actividades)
# # 9. Con un if: X not in list --> .apend
# if "NUEVO ELEMENTO" not in lista_actividades:
#     lista_actividades.append("NUEVO ELEMENTO")
#     print(lista_actividades)
# else:
#     print("La variable ya está en la lista.")



# EJERCICIO 6 (7)

# agenda: dict = {
#     "Ana": "654123987",
#     "Luis": "678555111",
#     "Marta": "622444333"
# }
# print(agenda) # A
# print(agenda.get("Luis")) # B
# print(agenda.get("Pedro")) # Devuelve "None"
# agenda["Pedro"] = "654321234" # C
# print("Ana", agenda["Ana"]) # D
# print("Luis", agenda["Luis"])
# print("Marta", agenda["Marta"])
# print("Pedro", agenda["Pedro"])
# eliminar = "Marta" # E
# eliminados = [eliminar, agenda.pop(eliminar)]
# print(agenda)
# print(eliminados)
# agenda.clear() # F
# print(agenda)


# print("EJERCICIO 7")

# peliculas: list = ["Inception", "The Matrix", "Interstellar", "Gladiator"]
# print("a)", peliculas) # a
# peliculas.append("El Padrino") # b
# print("b)", peliculas)
# peliculas.insert(1, "Memento") # c
# print("c)", peliculas)
# peliculas.remove("Gladiator") # d
# print("d)", peliculas)
# P = -1
# elimina = peliculas.pop(-1) # e) Se puede hacer con cualquier elemento de la lista, cambiando la variable P
# print("e)", peliculas, elimina, "deleted")
# peliculas.sort() # f
# print("f)", peliculas, "por orden alfabético")
# peliculas.clear() # g
# print("g)", peliculas)


# print("EJERCICIO 8")

# nota = 93
# if nota >= 90:
#     print("Excelente")
# elif nota > 70 and nota <= 89:
#     print("Bueno")
# elif nota > 50 and nota <= 69:
#     print("Suficiente")
# else:
#     print("Insuficiente")
