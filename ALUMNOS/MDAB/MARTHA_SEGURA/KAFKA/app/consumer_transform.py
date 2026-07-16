import json
from confluent_kafka import Consumer, Producer

BOOTSTRAP = "localhost:9092"
TOPIC_IN = "purchases_raw"
TOPIC_OUT = "purchases_enriched"
VAT_RATE = 0.21

def is_valid(p):
    return p.get("qty", 0) > 0 and p.get("unit_price", 0) > 0

def transform(p):
    qty = int(p["qty"])
    unit_price = float(p["unit_price"])
    subtotal = round(qty * unit_price, 2)
    vat = round(subtotal * VAT_RATE, 2)
    total = round(subtotal + vat, 2)
    return {
        "purchase_id": p["purchase_id"],
        "ts": p["ts"],
        "product": p["product"],
        "qty": qty,
        "unit_price": unit_price,
        "subtotal": subtotal,
        "vat": vat,
        "total": total,
        "currency": p.get("currency", "EUR"),
        "is_valid": True,
    }

def main():
    c = Consumer({
        "bootstrap.servers": BOOTSTRAP,
        "group.id": "transformer_group",
        "auto.offset.reset": "earliest",
    })
    p_out = Producer({"bootstrap.servers": BOOTSTRAP})

    c.subscribe([TOPIC_IN])
    print(f"📥 {TOPIC_IN} -> 📤 {TOPIC_OUT}")

    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("error", msg.error())
                continue

            raw = json.loads(msg.value().decode("utf-8"))
            if not is_valid(raw):
                continue

            enriched = transform(raw)
            p_out.produce(TOPIC_OUT, value=json.dumps(enriched).encode("utf-8"))
            p_out.poll(0)

            print("🛠️ ENRICHED:", enriched)

    except KeyboardInterrupt:
        print("\nStopping transformer...")
    finally:
        c.close()
        p_out.flush()

if __name__ == "__main__":
    main()
