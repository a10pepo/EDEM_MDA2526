"""
EJERCICIOS BÁSICOS DE PYTHON.
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

print("Nivel 1 - Condiciones simples")
# 1) Mayoría de edad (uno)
p = gente[3] # Pepe, 14
if p["edad"] >= 18:
    print("1) mayor")
else:
    print("1) menor")
# 2) Empieza por J
p = gente[1] # Juan, 35
if p["nombre"][0] == "J":
    print("2) empieza por 'J'")
else:
    print("2) no empieza por 'J'")
# 3) Nombre de 4 letras
p = gente[2] # Paco, 34
if len(p["nombre"]) == 4:
    print("3) 4 letras")
else:
    print(f"3) otra longitud ({len(p["nombre"])} letras)")
# 4) Edad par/impar
p = gente[4] # Pilar, 24
if p["edad"] % 2 == 0:
    print("4) par")
else:
    print("4) impar")
# 5) Termina en “o”
p = gente[0] # Jamiro, 45
if p["nombre"].endswith("o"):
    print("5) termina en 'o'")
else:
    print("5) no termina en 'o'")

print(" ") # línea de separación
print("Nivel 2 - if/else + lógicos")
# 6) J y menor de 40
p = gente[1] # Juan, 35
if p["nombre"].startswith("J") and p["edad"] < 40:
    print("6) J y <40")
else:
    print("6) no cumple")
# 7) A o a (sin distinguir mayúsculas)
p = gente[5] # Laura, 24
if "a" in p["nombre"].lower() or "A" in p["nombre"].upper():
    print("7) contiene 'a' o 'A'")
else:
    print("7) no contiene 'a' ni 'A'")
# 8) Entre 20 y 35 (ambos inclusive)
p = gente[4] # Pilar, 24
if 20 <= p["edad"] <= 35:
    print("8) rango 20-35")
else:
    print("8) fuera de rango")
# 9) No J y mayor de 30
p = gente[2] # Paco, 34
if not p["nombre"].startswith("J") and p["edad"] > 30:
    print("9) no 'J' y > 30")
else:
    print("9) no cumple")
# 10) Dos condiciones alternativas
p = gente[0] # Jamiro, 45
if p["nombre"].startswith("J") or p["edad"] <= 24:
    print("10) o J o <= 24")
else:
    print("10) no cumple")

print(" ") # línea de separación
print("Nivel 3 - Comparaciones entre 2-3 personas")
# 11) Mayor entre dos
a = gente[1] # Juan, 35
b = gente[2] # Paco, 34
if a["edad"] > b["edad"]:
    print("11)", a["nombre"], "es mayor")
elif a["edad"] < b["edad"]:
    print("11)", b["nombre"], "es mayor")
else:
    print("11)", "empate")
# 12) Más largo/ corto (nombre)
a = gente[5] # Laura, 24
b = gente[4] # Pilar, 24
if len(a) > len(b):
    print("12) a más largo")
elif len(a) < len(b):
    print("12) b más largo")
else:
    print("12) igual longitud")
# 13) El mayor de tres (solo ifs)
a = gente[0] # Jamiro, 45
b = gente[1] # Juan, 35
c = gente[2] # Paco, 34
if a["edad"] > b["edad"] and a["edad"] > c["edad"]:
    print(f"13) {a["nombre"]} es el mayor")
elif b["edad"] > a["edad"] and b["edad"] > c["edad"]:
    print(f"13) {b["nombre"]} es el mayor")
else:
    print(f"13) {c["nombre"]} es el mayor")