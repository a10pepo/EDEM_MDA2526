import psycopg2
import random
from datetime import datetime, timedelta
import time
import os

DB_CONFIG = {
    'host': "34.14.31.92",
    'port': 5432,
    'database': "mi-base-de-datos",
    'user': "admin-user",
    'password': "password-super-secreto-123"
}

NOMBRES = [
    'Juan García', 'María López', 'Pedro Martínez', 'Ana Rodríguez', 'Carlos Sánchez',
    'Laura Fernández', 'Miguel Torres', 'Elena González', 'David Ramírez', 'Carmen Díaz',
    'José Moreno', 'Isabel Muñoz', 'Francisco Romero', 'Lucía Navarro', 'Antonio Ruiz',
    'Marta Jiménez', 'Manuel Hernández', 'Sara Pérez', 'Javier Álvarez', 'Paula Gómez',
    'Roberto Silva', 'Andrea Castro', 'Fernando Ortiz', 'Clara Rubio', 'Pablo Molina',
    'Sofía Delgado', 'Diego Morales', 'Natalia Santos', 'Álvaro Iglesias', 'Victoria Herrera'
]

def get_email(nombre):
    nombre_partes = nombre.lower().split()
    return f"{nombre_partes[0]}.{nombre_partes[1]}@universidad.edu"

def wait_for_db():
    max_retries = 30
    retry_count = 0

    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("✓ Conexión exitosa a la base de datos")
            return True
        except psycopg2.OperationalError:
            retry_count += 1
            print(f"Esperando a que la base de datos esté lista... ({retry_count}/{max_retries})")
            time.sleep(2)

    print("✗ No se pudo conectar a la base de datos")
    return False

def wait_for_productos():
    max_retries = 30
    retry_count = 0

    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM productos")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            if count > 0:
                print(f"✓ Se encontraron {count} productos en la base de datos")
                return True

            retry_count += 1
            print(f"Esperando a que se inicialicen los productos... ({retry_count}/{max_retries})")
            time.sleep(3)
        except Exception as e:
            retry_count += 1
            print(f"Error al verificar productos: {e}")
            time.sleep(3)

    print("✗ No se encontraron productos en la base de datos")
    return False

def generate_historical_data():
    if not wait_for_db():
        return

    if not wait_for_productos():
        return

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT id, precio, categoria FROM productos")
    productos = cursor.fetchall()

    if not productos:
        print("No hay productos disponibles. Saliendo...")
        cursor.close()
        conn.close()
        return

    print(f"\n{'='*60}")
    print("Generando datos históricos de pedidos...")
    print(f"{'='*60}\n")

    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos_existentes = cursor.fetchone()[0]

    if pedidos_existentes > 10:
        print(f"Ya existen {pedidos_existentes} pedidos en la base de datos.")
        print("No se generarán datos históricos adicionales.")
        cursor.close()
        conn.close()
        return

    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=90)

    num_pedidos = random.randint(150, 250)

    estados = ['completado', 'completado', 'completado', 'completado', 'pendiente', 'cancelado']

    pedidos_generados = 0

    for i in range(num_pedidos):
        cliente = random.choice(NOMBRES)
        email = get_email(cliente)

        fecha_pedido = fecha_inicio + timedelta(
            seconds=random.randint(0, int((fecha_fin - fecha_inicio).total_seconds()))
        )

        estado = random.choice(estados)

        num_items = random.randint(1, 5)
        productos_pedido = random.sample(productos, min(num_items, len(productos)))

        total = 0
        items_data = []

        for producto in productos_pedido:
            producto_id, precio, categoria = producto
            cantidad = random.randint(1, 3)
            subtotal = precio * cantidad
            total += subtotal
            items_data.append((producto_id, cantidad, precio))

        cursor.execute(
            """
            INSERT INTO pedidos (cliente_nombre, cliente_email, total, estado, fecha_pedido)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (cliente, email, total, estado, fecha_pedido)
        )

        pedido_id = cursor.fetchone()[0]

        for producto_id, cantidad, precio_unitario in items_data:
            cursor.execute(
                """
                INSERT INTO items_pedido (pedido_id, producto_id, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
                """,
                (pedido_id, producto_id, cantidad, precio_unitario)
            )

        pedidos_generados += 1

        if (pedidos_generados % 50) == 0:
            print(f"  → {pedidos_generados}/{num_pedidos} pedidos generados...")

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM items_pedido")
    total_items = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total) FROM pedidos WHERE estado = 'completado'")
    ingresos_totales = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    print(f"\n{'='*60}")
    print("✓ Datos históricos generados exitosamente")
    print(f"{'='*60}")
    print(f"  Pedidos totales:        {total_pedidos}")
    print(f"  Items vendidos:         {total_items}")
    print(f"  Ingresos completados:   {ingresos_totales:.2f} €")
    print(f"  Periodo:                {fecha_inicio.date()} a {fecha_fin.date()}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    generate_historical_data()
