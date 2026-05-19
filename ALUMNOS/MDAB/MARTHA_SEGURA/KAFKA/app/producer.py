import json
import random
import time
from datetime import datetime, timezone
from confluent_kafka import Producer

BOOTSTRAP = "localhost:9092"
TOPIC = "purchases_raw"

products = ["zapatillas", "camiseta", "mallas", "botella", "auriculares"]
payments = ["card", "paypal", "bizum"]

def build_purchase():
    qty = random.randint(1, 3)
    unit_price = round(random.uniform(5.0, 120.0), 2)
    return {
        "purchase_id": random.randint(10000, 99999),
        "ts": datetime.now(timezone.utc).isoformat(),
        "user_id": random.randint(1, 500),
        "product": random.choice(products),
        "qty": qty,
        "unit_price": unit_price,
        "currency": "EUR",
        "payment_method": random.choice(payments),
    }

def main():
    p = Producer({"bootstrap.servers": BOOTSTRAP})
    try:
        while True:
            data = build_purchase()
            p.produce(TOPIC, value=json.dumps(data).encode("utf-8"))
            p.poll(0)
            print("RAW sent:", data)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        p.flush()

if __name__ == "__main__":
    main()
