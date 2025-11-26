from confluent_kafka import Consumer, Producer,KafkaException
import json
import time
import os
# Kafka Configuration

BASE_URL = os.getenv("SERVER_URL", "http://localhost:9092")

conf = {
    'bootstrap.servers': BASE_URL,
    'group.id': 'grupo_agua',  # Grupo único por ejecución
    'auto.offset.reset': 'earliest'
}

# Initialize Kafka Consumer
consumer = Consumer(conf)
consumer.subscribe(['pataton'])

# Dictionary to track the last known state for each device
device_states = {}

# Threshold for anomaly detection (e.g., 10% increase in consumption)
THRESHOLD_PERCENT = 10

alert_producer = Producer({    
            'bootstrap.servers': BASE_URL,
            'client.id': 'python-producer'
            })
    
topic_kafka = "inverter_alerts"

def send_alert(alert_description):
    """Send alert to Kafka topic 'alertas_irregularidades_inversores'."""
    
    data_str = json.dumps(alert_description, ensure_ascii=False)

    data_bytes = data_str.encode('utf-8')
    
    alert_producer.produce(topic=topic_kafka, value=data_bytes)
    

def is_anomaly(current_watts, previous_watts):
    """Check if the current value is an anomaly compared to the previous."""
    if abs(current_watts - previous_watts) > 50:
        return True  # Avoid division by zero
    return False

def generate_alert(device_id, previous_watts, current_watts):
    # publish alert message to topic 'alertas_irregularidades_inversores'
    """Generate an alert message."""
    alert_message={
        "device_id": device_id,
        "previous_watts": previous_watts,
        "current_watts": current_watts,
        "increase": abs(current_watts - previous_watts),
        "timestamp": time.time()
    }

    send_alert(alert_message)
    
    print(f"⚠️ Alert for device {device_id}:")
    print(f"  Previous: {previous_watts} W")
    print(f"  Current: {current_watts} W")
    print(f"  Increase: {abs(current_watts - previous_watts)} W")


def main():
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            try:
                # Parse message
                value = json.loads(msg.value().decode('utf-8'))
                device_id = value['id']
                watts = value['totalConsumption']
                timestamp = value['timestamp']

                # Update device state
                if device_id not in device_states:
                    device_states[device_id] = {
                        'last_watts': watts,
                        'last_timestamp': timestamp
                    }
                    print(f"Initialized device {device_id} with {watts} W")
                else:
                    previous_state = device_states[device_id]
                    previous_watts = previous_state['last_watts']

                    if is_anomaly(watts, previous_watts):
                        generate_alert(device_id, previous_watts, watts)
                    else:
                        print(f"✅ Device {device_id} consumed {watts} W")

                    # Update state
                    device_states[device_id]['last_watts'] = watts
                    device_states[device_id]['last_timestamp'] = timestamp

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
