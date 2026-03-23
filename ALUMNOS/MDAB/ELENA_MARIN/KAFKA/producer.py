#Step 1: importing libraries
from math import prod
import os
import json
from json import dumps
import time
import pandas as pd
from confluent_kafka import Producer

#Step 2: Producer configuration
config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'productor-python'
}

#Step 3: Producer creation
producer = Producer(config)

#Step 4: Topic definition
topic_kafka = 'sales'

#Step 5: Reading the CSV and sending messages to Kafka 
file_route = os.path.join(os.path.dirname(__file__), 'sales.csv')
print(f"Searching file in: {file_route}")
if not os.path.exists(file_route):
    raise FileNotFoundError(f"Can't find the file 'sales.csv'")

#Step 5.1: Reading the CSV with Pandas and convert it to a list of dictionaries (one per row)
df = pd.read_csv(file_route)
tickets = df.to_dict(orient='records') 

print(f"Success: {len(tickets)} loaded tickets.")

#Step 5.2: Sending every ticket to Kafka
for ticket in tickets:
    time.sleep(2) # Leaving 2 seconds to simulate a real data flow
    
    # Obtaining data to print
    ticket_id = ticket.get('ticket_id', 'N/A')
    garment = ticket.get('garment', 'N/A')
    price = ticket.get('price', 0)
    
    print(f"Sending to kafka: {ticket_id} - {garment} - ${price}")

    # Sending the data as a JSON
    # Using the ticket ID as the 'key' so Kafka organizes it well
    producer.produce(
        topic=topic_kafka, 
        value=json.dumps(ticket).encode('utf-8'), 
        key=str(ticket_id)
    )
    print(f"Sending data: {ticket} to topic '{topic_kafka}'...")
    time.sleep(1)
    
    # Flush makes sure the message is sent before moving on to the next one. It's a good practice to call it after producing messages, especially if you want to ensure all messages are sent before the program ends.
    pending = producer.flush()
    if pending != 0:
        print(f"Warning: Still {pending} messages pending to be sent.")
    
print("All data has been sent")