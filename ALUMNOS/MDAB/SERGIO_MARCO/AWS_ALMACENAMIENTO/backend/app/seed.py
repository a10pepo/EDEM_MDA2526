from datetime import date, timedelta
from sqlalchemy.orm import Session
from .models import Conductor, Vehiculo, Ruta, Pedido


def seed_if_empty(db: Session) -> None:
    if db.query(Conductor).count() > 0:
        return

    today = date.today()

    conductores = [
        Conductor(dni="12345678A", nombre="Juan García López",      telefono="600111222"),
        Conductor(dni="23456789B", nombre="María Martínez Ruiz",    telefono="600222333"),
        Conductor(dni="34567890C", nombre="Carlos Sánchez Pérez",   telefono="600333444"),
        Conductor(dni="45678901D", nombre="Ana López Fernández",    telefono="600444555"),
        Conductor(dni="56789012E", nombre="Pedro Gómez Torres",     telefono="600555666"),
    ]
    db.add_all(conductores)
    db.flush()

    vehiculos = [
        Vehiculo(matricula="1234ABC", modelo="Mercedes Sprinter",  capacidad_carga_kg=1000, fecha_itv=today + timedelta(days=20),  estado="en_ruta"),   # ITV alert (< 30 days)
        Vehiculo(matricula="5678DEF", modelo="Iveco Daily",        capacidad_carga_kg=1500, fecha_itv=today + timedelta(days=10),  estado="en_ruta"),   # ITV alert (< 30 days)
        Vehiculo(matricula="9012GHI", modelo="Renault Master",     capacidad_carga_kg=1200, fecha_itv=today + timedelta(days=90),  estado="en_ruta"),
        Vehiculo(matricula="3456JKL", modelo="Ford Transit",       capacidad_carga_kg=800,  fecha_itv=today + timedelta(days=120), estado="disponible"),
        Vehiculo(matricula="7890MNO", modelo="Volkswagen Crafter", capacidad_carga_kg=2000, fecha_itv=today + timedelta(days=200), estado="disponible"),
    ]
    db.add_all(vehiculos)
    db.flush()

    rutas = [
        Ruta(vehiculo_id=vehiculos[0].id, conductor_id=conductores[0].id,
             origen_lat=40.416775, origen_lng=-3.703790,
             destino_lat=41.385064, destino_lng=2.173404,
             actual_lat=40.416775, actual_lng=-3.703790, estado="en_ruta"),   # Madrid → Barcelona
        Ruta(vehiculo_id=vehiculos[1].id, conductor_id=conductores[1].id,
             origen_lat=39.469907, origen_lng=-0.376288,
             destino_lat=43.263012, destino_lng=-2.934985,
             actual_lat=39.469907, actual_lng=-0.376288, estado="en_ruta"),   # Valencia → Bilbao
        Ruta(vehiculo_id=vehiculos[2].id, conductor_id=conductores[2].id,
             origen_lat=37.389092, origen_lng=-5.984459,
             destino_lat=40.416775, destino_lng=-3.703790,
             actual_lat=37.389092, actual_lng=-5.984459, estado="en_ruta"),   # Sevilla → Madrid
        Ruta(vehiculo_id=vehiculos[3].id, conductor_id=conductores[3].id,
             origen_lat=41.385064, origen_lng=2.173404,
             destino_lat=37.389092, destino_lng=-5.984459,
             actual_lat=41.385064, actual_lng=2.173404,  estado="pendiente"), # Barcelona → Sevilla
        Ruta(vehiculo_id=vehiculos[4].id, conductor_id=conductores[4].id,
             origen_lat=43.263012, origen_lng=-2.934985,
             destino_lat=39.469907, destino_lng=-0.376288,
             actual_lat=43.263012, actual_lng=-2.934985, estado="pendiente"), # Bilbao → Valencia
    ]
    db.add_all(rutas)
    db.flush()

    pedidos = [
        Pedido(ruta_id=rutas[0].id, peso_kg=920,  descripcion="Electrodomésticos"),      # 92% of 1000kg → overload alert
        Pedido(ruta_id=rutas[1].id, peso_kg=1400, descripcion="Materiales construcción"), # 93% of 1500kg → overload alert
        Pedido(ruta_id=rutas[2].id, peso_kg=500,  descripcion="Paquetería estándar"),
    ]
    db.add_all(pedidos)
    db.commit()
