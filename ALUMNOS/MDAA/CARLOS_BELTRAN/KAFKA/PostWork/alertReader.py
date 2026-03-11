from confluent_kafka import Consumer, Producer,KafkaException
import json
import time
import os

# Kafka Configuration

BASE_URL = os.getenv("SERVER_URL", "http://localhost:9092")

conf = {
    'bootstrap.servers': BASE_URL,
    'group.id': 'alert_reader', 
    'auto.offset.reset': 'earliest'
}

# Initialize Kafka Consumer
consumer = Consumer(conf)
consumer.subscribe(['inverter_alerts'])

# Dictionary to track the last known state for each device
device_states = {}

def main():
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            try:
                # Parse message
                value = json.loads(msg.value().decode('utf-8'))
                device_id = value["device_id"]
                previous_watts = value["previous_watts"]
                current_watts = value["current_watts"]
                increase_quantity=current_watts-previous_watts
                timestamp=value["timestamp"]

                print(f"⚠️ Alert. Device {device_id} has increased {increase_quantity} W at {time.ctime(timestamp)}")
                
            except Exception as e:
                print(f"Error processing message: {e}")

        # Commit offsets manually (optional)
        consumer.commit()

    except KafkaException as e:
        print(f"Kafka error: {e.args}")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
