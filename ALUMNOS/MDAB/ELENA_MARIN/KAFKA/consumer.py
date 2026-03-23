#Step 1: Importing libraries
from confluent_kafka import Consumer
import json

#Step 2: Consumer configuration
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-consumidor',
    'auto.offset.reset': 'earliest'
}

#Step 3: Consumer creation
consumer = Consumer(config)

#Step 4: Topic subscription
topic_kafka = "sales"
consumer.subscribe(["sales"])

print(f"Waiting for messages in topic '{topic_kafka}'...")

#Step 5: Messages consumption
try:
    while True:
        msg = consumer.poll(1.0) # tries to obtain 1 message every one second:
        if msg is None: #if no message is received, we just wait for the next one
            continue
        if msg.error(): #if there is an error in the message, we print it and wait for the next one
            print(f"Error: {msg.error()}")
            continue

        # Decoding the message
        message_value = msg.value().decode('utf-8')
        ticket = json.loads(message_value)
        
        # Business logic: we print the garment, size and store of the sale, and we create an alert for luxury sales, that is, sales with price higher than 100 dollars
        garment = ticket.get('garment')
        size = ticket.get('size')
        store = ticket.get('store')
        
        print(f"DETECTED SALE: {garment} (Size {size}) in {store}")
        
        # We create an alert for luxury sales, that is, sales with price higher than 100 dollars
        if ticket['price'] > 100:
            print(f"ALERT: Luxury sale detected (${ticket['price']})")

except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()