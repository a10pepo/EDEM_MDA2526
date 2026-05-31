import json
import logging
from google.cloud import pubsub_v1
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# --- CONFIGURACIÓN ---
PROJECT_ID = "astral-bit-481514-n1"
TOPIC_ALERT_NAME = "stock-alerts"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ALERT_NAME)

# --- INVENTARIO COMPLETO (IDs 1-20 de FakeStoreAPI) ---

INVENTORY_DB = {
    1: {"name": "Fjallraven - Foldsack No. 1 Backpack", "stock": 50},
    2: {"name": "Mens Casual Premium Slim Fit T-Shirts", "stock": 15},
    3: {"name": "Mens Cotton Jacket", "stock": 5},   # Stock crítico
    4: {"name": "Mens Slim Fit", "stock": 20},
    5: {"name": "John Hardy Women's Legends Naga Gold", "stock": 8},
    6: {"name": "Solid Gold Petite Micropave", "stock": 50},
    7: {"name": "White Gold Plated Princess", "stock": 12},
    8: {"name": "Pierced Owl Rose Gold Plated Stainless Steel", "stock": 30},
    9: {"name": "WD 2TB Elements Portable External Hard Drive", "stock": 40},
    10: {"name": "SanDisk SSD PLUS 1TB Internal SSD", "stock": 25},
    11: {"name": "Silicon Power 256GB SSD 3D NAND", "stock": 18},
    12: {"name": "WD 4TB Gaming Drive Works with Playstation", "stock": 10},
    13: {"name": "Acer SB220Q bi 21.5 inches Full HD", "stock": 7},
    14: {"name": "Samsung 49-Inch CHG90 144Hz Curved Gaming Monitor", "stock": 4}, # ¡Alerta inmediata!
    15: {"name": "BIYLACLESEN Women's 3-in-1 Snowboard Jacket", "stock": 22},
    16: {"name": "Lock and Love Women's Removable Hooded", "stock": 14},
    17: {"name": "Rain Jacket Women Windbreaker Striped Climbing", "stock": 35},
    18: {"name": "MBJ Women's Solid Short Sleeve Boat Neck V", "stock": 60},
    19: {"name": "Opna Women's Short Sleeve Moisture", "stock": 45},
    20: {"name": "DANVOUY Womens T Shirt Casual Cotton Short", "stock": 55}
}

def callback(message):
    global INVENTORY_DB
    
    try:
        # 1. Decodificar el mensaje JSON
        data = json.loads(message.data.decode("utf-8"))
        
        # Obtenemos el ID del pedido
        order_id = data.get("order_id")
        
        # Obtenemos la LISTA de productos
        products_list = data.get("products", [])
        
        logging.info(f" Procesando Pedido #{order_id} con {len(products_list)} productos.")

        # 2. Recorremos cada producto dentro del pedido
        for item in products_list:
            p_id = item.get("productId")  # ID que viene de la API
            p_name = item.get("name")
            qty = item.get("quantity", 1)
            
            # Si el producto existe en nuestro inventario simulado
            if p_id in INVENTORY_DB:
                # A) RESTAR STOCK
                INVENTORY_DB[p_id]["stock"] -= qty
                current_stock = INVENTORY_DB[p_id]["stock"]
                
                logging.info(f"   - 📦 {INVENTORY_DB[p_id]['name']} (ID: {p_id}): Vendidos {qty}. Quedan {current_stock}.")

                # B) CHEQUEAR ALERTA (< 5 unidades)
                if current_stock < 5:
                    logging.warning(f"   🚨 ALERTA: Stock crítico para {INVENTORY_DB[p_id]['name']}!")
                    
                    # Preparar mensaje para BigQuery
                    alert_payload = {
                        "message": "URGENTE: Reabastecer",
                        "product_id": p_id,
                        "product_name": INVENTORY_DB[p_id]['name'],
                        "current_stock": current_stock,
                        "timestamp": datetime.now().isoformat(),
                        "order_trigger": order_id
                    }
                    
                    # Enviar a Pub/Sub
                    data_str = json.dumps(alert_payload).encode("utf-8")
                    publisher.publish(topic_path, data_str)
                    
            else:
                # Si llega un ID raro (ej: 21, 22...), avisamos
                logging.info(f"   - Producto ID {p_id} desconocido en inventario local.")

        # 3. Confirmar mensaje procesado
        message.ack()
        
    except Exception as e:
        logging.error(f"🔥 Error procesando pedido: {e}")
        message.nack()