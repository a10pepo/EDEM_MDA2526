# Data Processing with Kafka end to end: Spanish National Team Selection

## 1. Introduction & Use Case

### Business Definition
In the modern era of football, decision-making based on data is crucial. National team coaches cannot manually monitor every single action of every player in the league in real-time.

This project implements a **Real-Time Data Processing Pipeline** designed for the **Spanish Football Federation (RFEF)**. The goal is to ingest live player statistics from LaLiga EA Sports 2025/26 and automatically filter, categorize, and select the final squad for the upcoming international call-up.

### Value Proposition
* **Automation:** Removes manual filtering of non-eligible players.
* **Real-Time Categorization:** Instantly labels players as "Wonderkids", "Prime", or "Veterans" based on age.
* **Load Balancing:** Distributes players into specific Kafka partitions based on their position on the field (Goalkeeper, Defender, Midfielder, Attacker).
* **Quality Control:** Uses KSQL to strictly filter the "Final Squad" based on a high-performance rating threshold.

---

## 2. Dataset Selected

We utilize a dataset of **100 professional players** from **LaLiga EA Sports 2024-2025**.
* **Source:** `laliga_players.json` (Simulated live feed).
* **Format:** NDJSON (Newline Delimited JSON).
* **Key Attributes:** Name, Age, Position, Nation, Team, Rating, Pace, Market Value.

---

## 3. Architecture

The solution follows a Lambda-like streaming architecture using **Apache Kafka** and **KSQL**.

```mermaid
graph LR
    A [Data Source (JSON)] -->|Producer| B(Topic: laliga_players)
    B -->|Consumer Python| C{Python ETL Logic}
    C -->|Filter: Nation=Spain| D[Enrichment & Partitioning]
    D -->|Topic: spanish_players| E(KSQL Processing)
    E -->|Filter: Rating >= 81| F(Topic: FINAL_SQUAD)
    F -->|Consumer Python| G[Terminal Visualization]
```

Ingestion: A Python Producer simulates live match data sent to the topic laliga_players.

Processing (Python): A Consumer reads the raw data, filters out non-Spanish players, calculates the age_stage, and sends them to the topic spanish_players.

Key Feature: Data is sent to 4 specific partitions based on field position.

Analytics (KSQL): KSQL reads the partitioned stream and applies a high-performance filter to create the FINAL_SQUAD table.

Reporting: A final Python Consumer displays the eligible squad in the terminal in a readable format.

---

## 4. Data Models (JSON Evolution)

The pipeline transforms raw player data through three distinct stages, evolving from initial ingestion to the final scouting report.

### A. Input Data (Raw Message)
* **From Topic:** `laliga_players`
* **Description:** The initial raw data as ingested from the source dataset.

```json
{
  "name": "Nico Williams",
  "age": 23,
  "position": "Attacker",
  "nation": "Spain",
  "team": "Athletic Club",
  "rating": 84,
  "pace": 94,
  "market_value_E": 70000000
}
```

### B. Intermediate Data (Processed & Enriched)
* **From Topic:** `spanish_players`
* **Description:** The initial raw data as ingested from the source dataset.

```json
{
  "name": "Nico Williams",
  "age": 23,
  "position": "Attacker",
  "nation": "Spain",
  "team": "Athletic Club",
  "rating": 84,
  "pace": 94,
  "market_value_E": 70000000,
  "age_stage": "Wonderkid"  // <-- New Field Added by Python Consumer
}
```

## 5. Technical Implementation Details

### Components

1.  **producer.py**:
    
    *   Reads the dataset line-by-line and pushes to Kafka with a delay to simulate real-time events.
        
2.  **consumer1.py (The Router)**:
    
    *   **Logic:** IF nation == 'Spain'.
        
    *   **Enrichment:** Calculates age\_stage (Wonderkid/Prime/Veteran).
        
    *   **Partitioning Strategy:**
        
        *   Partition 0: Goalkeepers
            
        *   Partition 1: Defenders
            
        *   Partition 2: Midfielders
            
        *   Partition 3: Attackers
            
3.  **KSQL Queries**:
    
    *   Stream creation over spanish\_players.
        
    *   Persistent Query (CSAS) to create FINAL\_SQUAD filtering by rating.
        
4.  **consumer\_final.py**:
    
    *   Formats the JSON output into a readable table for the scouting department.
        

### Execution Steps

To run the application end-to-end:

1.  **Start Environment:** Ensure Zookeeper & Kafka are running.
    
2.  Bashkafka-topics --create --topic spanish\_players --partitions 4 --bootstrap-server localhost:9092
    
3.  **Run Final Consumer:**python consumer\_final.py (Starts waiting for final results).
    
4.  **Run KSQL Queries:** Execute the CREATE STREAM and CREATE TABLE commands.
    
5.  **Run Processing Consumer:**python consumer1.py (Starts listening to raw data).
    
6.  **Run Producer:**python producer.py (Starts injecting data).
    

## 6. Deliverables & Evidence

Screenshots provided in the attached document demonstrate the successful execution of the pipeline:

The screenshots (evidence_screenshots/) document the successful end-to-end execution of the pipeline, ordered chronologically according to the architecture:

1.  **01_producer_logs:** Execution of the Python Producer, demonstrating the ingestion of raw player data into the `laliga_players` topic.
2.  **02_consumer_logs:** The Router Consumer (`consumer1.py`) in action, filtering for Spanish players and routing them to specific partitions based on their position.
3.  **03_topic_creation:** Manual creation of the `spanishPlayers` topic with **4 partitions**, ensuring the load balancing architecture is correctly established.
4.  **04_ksql_show_topics:** KSQLDB verification command (`SHOW TOPICS;`) confirming the existence of the topics and the correct partition count (4) for the processed topic.
5.  **05_ksql_streamSNT_creation:** Creation of the initial KSQL Stream (`spanish_national_team`) mapping the JSON data to a schema.
6.  **06_ksql_query:** Verification query in KSQLDB to ensure data is flowing correctly into the stream.
7.  **07_ksql_streamSFS_creation:** Creation of the filtered stream/table (`FINAL_SQUAD`) using logic to select only players with a rating >= 81.
8.  **08_consumer_final_logs:** The Final Consumer (`consumer_final.py`) displaying the "Final Squad" list, formatted and filtered, completing the pipeline.

