import json
from confluent_kafka import Consumer

BOOTSTRAP = "localhost:9092"
TOPIC = "purchases_kpi"

def main():
    c = Consumer({
        "bootstrap.servers": BOOTSTRAP,
        "group.id": "printer_group",
        "auto.offset.reset": "earliest",
    })
    c.subscribe([TOPIC])
    print(f"🖥️ Printing KPIs from {TOPIC} ...")

    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("error", msg.error())
                continue

            data = json.loads(msg.value().decode("utf-8"))
            print("📊 KPI:", data)

    except KeyboardInterrupt:
        print("\nStopping printer...")
    finally:
        c.close()

if __name__ == "__main__":
    main()
