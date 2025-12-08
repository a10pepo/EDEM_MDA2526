import csv
import random
import os
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
NUM_CLIENTES = 300
NUM_PEDIDOS_PROV = 200
NUM_VENTAS = 6000  # Subimos volumen para asegurar variedad de especies

# --- 1. MAESTRO DE PRODUCTOS (Marcas reales y categorias) ---
catalog_definitions = [
    # (Categoria, Subcategoria, Marca, Modelo, [Variaciones], Precio, Gama, EsBarco, ProbExito)
    
    # --- EGING ---
    ("Eging", "Señuelo", "Yamashita", "Egi-OH Live", ["3.0 Naranja", "3.5 Rosa", "3.0 Natural"], 23.00, "Alta", False, 0.70),
    ("Eging", "Señuelo", "DTD", "Real Fish", ["Sargo", "Julia", "Pagel"], 14.50, "Media", False, 0.55),
    ("Eging", "Señuelo", "Generico", "Jibionera Tela", ["Pack 3u"], 9.00, "Baja", False, 0.20),
    ("Eging", "Caña", "Major Craft", "Crostage Eging", ["832E", "862E"], 155.00, "Media", False, 0.0),

    # --- SPINNING (Costa) ---
    ("Spinning", "Señuelo", "Fiiish", "Black Minnow 120", ["Kaki", "Blue", "Pink"], 13.50, "Alta", False, 0.80),
    ("Spinning", "Señuelo", "Xorus", "Patchinko 100", ["Sun Sprat", "Ghost Iwashi"], 32.00, "Alta", False, 0.85), 
    ("Spinning", "Señuelo", "Rapala", "MaxRap 13", ["Fayu", "Flake Silver"], 19.00, "Media", False, 0.60),
    ("Spinning", "Señuelo", "Savage Gear", "Sandeel", ["White", "Blue Lemon"], 9.50, "Media", False, 0.65),
    ("Spinning", "Carrete", "Shimano", "Stradic FL", ["4000 XG", "5000 XG"], 190.00, "Media", False, 0.0),
    
    # --- SURFCASTING (Playa) ---
    ("Surfcasting", "Cebo", "Cebos Norte", "Americana", ["Caja XL"], 6.50, "Media", False, 0.90),
    ("Surfcasting", "Cebo", "Cebos Sur", "Tita Biby", ["Caja"], 8.50, "Media", False, 0.95),
    ("Surfcasting", "Terminal", "Turkana", "Plomo Bala", ["120g", "130g"], 2.50, "Baja", False, 0.0),
    ("Surfcasting", "Caña", "Vercelli", "Enygma", ["4.20m Hybrid"], 140.00, "Media", False, 0.0),

    # --- CURRI / BARCO (Alta mar) ---
    ("Curri", "Señuelo", "Halco", "Sorcerer 150", ["Redhead", "Purple"], 26.00, "Alta", True, 0.80),
    ("Curri", "Señuelo", "Williamson", "Exciter Bird", ["130mm"], 22.00, "Media", True, 0.60),
    ("Curri", "Carrete", "Shimano", "Tiagra", ["50W LRS"], 850.00, "Alta", True, 0.0),
    
    # --- JIGGING / FONDO (Barco) ---
    ("Jigging", "Señuelo", "Major Craft", "Jigpara Vertical", ["100g Zebra", "150g Pink"], 12.00, "Media", True, 0.70),
    ("Vivo", "Terminal", "Mustad", "Anzuelo Kaiju", ["5/0", "7/0"], 9.00, "Alta", True, 0.50)
]

# --- 2. SISTEMA DE BIODIVERSIDAD Y RAREZA ---
# Formato: "Especie": PesoRelativo (Cuanto más alto, más común)
# Esto evita la plaga de pulpos y da variedad.

ecosistema = {
    "Eging": {
        "Calamar": 60,     # Muy común
        "Sepia": 30,       # Común
        "Pulpo": 10        # Raro (ahora saldrán menos)
    },
    "Spinning": {
        "Lubina": 35,
        "Anjova": 20,
        "Jurel": 15,
        "Espeton": 10,
        "Baila": 10,
        "Palometon": 5,    # Raro
        "Serviola": 5      # Raro
    },
    "Surfcasting": {
        "Herrera": 30,
        "Sargo": 25,
        "Mabra": 20,
        "Dorada": 15,
        "Lubina": 5,
        "Corvina": 3,      # Muy raro (Trofeo)
        "Rodaballo": 2     # Muy raro
    },
    "Curri": {
        "Bonito del Norte": 40,
        "Llampuga": 30,
        "Bacoreta": 15,
        "Melva": 10,
        "Marlin Blanco": 5 # El sueño
    },
    "Jigging": {
        "Sama": 20,
        "Denton": 15,
        "Pargo": 20,
        "Cabrilla": 25,    # Pez pasto común
        "San Pedro": 10,
        "Mero": 5,         # Raro
        "Gallineta": 5
    },
    "Vivo": { # Pesca específica de trofeos
        "Denton": 40,
        "Serviola": 40,
        "Mero": 20
    }
}

# Rangos de peso (kg) aproximados por especie para dar realismo
pesos_ref = {
    "Calamar": (0.2, 1.5), "Pulpo": (1.0, 5.0), "Sepia": (0.3, 2.0),
    "Lubina": (0.5, 5.0), "Anjova": (2.0, 7.0), "Palometon": (5.0, 15.0),
    "Dorada": (0.3, 3.0), "Sargo": (0.2, 1.2), "Herrera": (0.2, 0.8), "Corvina": (2.0, 15.0),
    "Bonito del Norte": (4.0, 15.0), "Llampuga": (2.0, 10.0), "Marlin Blanco": (15.0, 50.0),
    "Denton": (1.5, 8.0), "Sama": (2.0, 10.0), "Mero": (3.0, 15.0), "San Pedro": (0.5, 2.5)
}

# --- 3. GENERACIÓN DE ARTÍCULOS ---
articulos = []
sku_id = 1
for cat, subcat, marca, modelo, vars, precio, gama, barco, prob in catalog_definitions:
    for v in vars:
        articulos.append({
            "id_articulo": f"A{str(sku_id).zfill(4)}",
            "nombre": f"{modelo} {v}",
            "marca": marca, "categoria": cat, "subcategoria": subcat, "gama": gama,
            "precio": precio, "coste": round(precio*0.55, 2), "es_barco": barco, "prob_pesca": prob
        })
        sku_id += 1

# --- 4. CLIENTES ---
clientes = []
for i in range(1, NUM_CLIENTES + 1):
    clientes.append({
        "id_cliente": f"C{str(i).zfill(3)}",
        "nombre": f"Cliente {i}",
        "municipio": random.choice(["Valencia", "Alicante", "Castellon", "Gijon", "Santander", "Cadiz"]),
        "modalidad_pref": random.choice(list(ecosistema.keys())),
        "fecha_alta": (datetime(2023,1,1) + timedelta(days=random.randint(0,500))).strftime("%Y-%m-%d")
    })

# --- 5. VENTAS Y CAPTURAS (CORE LOGIC) ---
ventas = []
capturas = []
t_id = 1
c_id = 1

print("🎣 Simulando jornadas de pesca con biodiversidad ajustada...")

for _ in range(NUM_VENTAS):
    cli = random.choice(clientes)
    
    # Seleccionamos artículo (preferencia por su modalidad, pero compra otras cosas a veces)
    pool = [a for a in articulos if a["categoria"] == cli["modalidad_pref"]]
    if random.random() < 0.2: pool = articulos # 20% compra random
    if not pool: pool = articulos
    
    art = random.choice(pool)
    
    # Fecha Venta
    mes_venta = random.randint(1,12)
    # Ajuste estacional
    if art["categoria"] == "Eging": mes_venta = random.choice([10,11,12,1,2]) # Invierno
    elif art["categoria"] == "Curri": mes_venta = random.choice([6,7,8,9]) # Verano
    
    fecha_venta = datetime(2024, mes_venta, random.randint(1,28))
    
    ventas.append({
        "id_ticket": f"T-{str(t_id).zfill(5)}",
        "fecha": fecha_venta.strftime("%Y-%m-%d"),
        "id_cliente": cli["id_cliente"],
        "id_articulo": art["id_articulo"],
        "cantidad": random.randint(1,3),
        "total": round(art["precio"], 2)
    })
    t_id += 1

    # --- GENERACIÓN DE CAPTURAS PONDERADAS ---
    # Si el articulo sirve para pescar...
    if art["prob_pesca"] > 0:
        # Simulamos X salidas de pesca tras la compra
        num_salidas = random.choices([1, 2, 3, 4, 5], weights=[20, 30, 25, 15, 10])[0]
        
        for i_salida in range(num_salidas):
            # Tirada de éxito de la jornada
            if random.random() < art["prob_pesca"]:
                
                # ¿Qué modalidad es? (A veces usan un señuelo de spinning para curri, pero simplifiquemos)
                modalidad = art["categoria"]
                if modalidad not in ecosistema: modalidad = "Spinning"
                
                # SELECCIÓN PONDERADA DE ESPECIE
                # Aquí está la magia: Usamos los pesos definidos arriba para que no salgan siempre los mismos
                posibles_peces = list(ecosistema[modalidad].keys())
                pesos_peces = list(ecosistema[modalidad].values())
                
                # Elegimos 1 especie basada en probabilidad
                especie_elegida = random.choices(posibles_peces, weights=pesos_peces, k=1)[0]
                
                # Cantidad de capturas en ese día (Eging/Surfcasting a veces sacas varios, Curri suele ser 1)
                num_piezas = 1
                if modalidad in ["Eging", "Surfcasting"]:
                    # 70% de sacar 1, 20% de sacar 2, 10% de sacar 3. Ya no salen 8 pulpos.
                    num_piezas = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
                
                for _ in range(num_piezas):
                    # Calcular peso
                    rango = pesos_ref.get(especie_elegida, (0.5, 2.0))
                    peso_final = round(random.uniform(rango[0], rango[1]), 2)
                    
                    # Fecha captura (dias despues de compra)
                    fecha_cap = fecha_venta + timedelta(days=random.randint(1, 30) + (i_salida*7))
                    
                    capturas.append({
                        "id_captura": f"CAP-{c_id}",
                        "fecha": fecha_cap.strftime("%Y-%m-%d"),
                        "id_cliente": cli["id_cliente"],
                        "especie": especie_elegida,
                        "peso": peso_final,
                        "articulo_usado": art["id_articulo"],
                        "zona": random.choice(["Espigon", "Playa", "Ria", "Alta Mar"])
                    })
                    c_id += 1

# --- GUARDAR ---
os.makedirs("data", exist_ok=True)
def save(name, data):
    if not data: return
    with open(f"data/{name}", 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=data[0].keys())
        w.writeheader()
        w.writerows(data)

save("articulos.csv", articulos)
save("clientes.csv", clientes)
save("ventas.csv", ventas)
save("capturas.csv", capturas)

# Pedidos stock simples
pedidos = []
for i in range(1, NUM_PEDIDOS_PROV + 1):
    art = random.choice(articulos)
    pedidos.append({
        "id_pedido": f"PROV-{i}",
        "fecha": datetime(2024, random.randint(1,10), 1).strftime("%Y-%m-%d"),
        "proveedor": "Distribuidor Oficial",
        "id_articulo": art["id_articulo"],
        "cantidad": 50,
        "estado": "recibido"
    })
save("pedidos_stock.csv", pedidos)

print(f"✅ ¡Script V10 completado!")
print(f"-> Total Ventas: {len(ventas)}")
print(f"-> Total Capturas: {len(capturas)}")
print("-> Distribución de especies ajustada (Menos pulpos, más variedad).")