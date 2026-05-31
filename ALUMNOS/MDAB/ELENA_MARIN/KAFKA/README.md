# Kafka end-to-end. Retail sales pipeline
This project implements a data pipeline designed for the retail sector. It allows users and businesses to monitor, filter, and track purchase transactions as they happen, moving data from raw CSV files to actionable insights using Apache Kafka and ksqlDB.

## Dataset selected
The selected dataset contains tickets from different retail stores, enabling users to mantain a historical record of their transactions. 

The dataset contains the following information:
- id_ticket
- purchase_date
- store
- category
- garment
- size
- price
- channel
- latitude
- longitude

## Final architecture implemented
I have used Python to develop a producer that sends sales data in a CSV format to a Kafka cluster. 

##### Producer
The producer extracts the information from the CSV 'sales.csv'. It acts as the data ingestion layer. 
##### Broker
Kafka receives the data from the producer and keeps it in the topic 'sales'. 
##### Consumer
The consumer receives the information from the CSV 'sales.csv'.
##### kSQL
Allows to filter by price, category, store...
1. **High value stream**
This stream captures premium sales in real-time. It is designed to trigger alerts or specialized workflows whenever an item over $100 is purchased.
2. **Revenue by channel**
This persistent table maintains a live balance of total revenue, broken down by sales channel (Online vs. In-store). Unlike a traditional database, this total updates automatically with every new event.

## JSON examples of my data json model
{
    "id_ticket": "T-MODA-001"
    "purchase_data": "2026-02-08 10:15:20"
    "store": "Zara"
    "category": "Footwear"
    "garment": "Leather Ankle Boots"
    "garment_size": "38"
    "price": "79.95"
    "channel": "Instore"
    "latitude": "40.4168"
    "longitude": "-3.7038"
}

## Target of my application
- ###### General consumers
    People looking for a centralized way to track their purchase history across different retail brands.
- ###### Retail analysts
    Professionals who need to monitor store performance and sales trends in real time. 


