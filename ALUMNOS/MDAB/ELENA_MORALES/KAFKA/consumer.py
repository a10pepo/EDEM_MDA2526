import json
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer('music_raw_events', bootstrap_servers=['localhost:9092'],
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))

catalogo = {
    "SONG_01": {"titulo": "Espresso", "artista": "Sabrina Carpenter"},
    "SONG_02": {"titulo": "Houdini", "artista": "Eminem"},
    "SONG_03": {"titulo": "Gata Only", "artista": "FloyyMenor"},
    "SONG_04": {"titulo": "Luna", "artista": "Feid"},
    "SONG_05": {"titulo": "Starboy", "artista": "The Weeknd"}
}

for message in consumer:
    raw = message.value
    t_id = raw["track_id"]

    if t_id in catalogo:
        info = catalogo[t_id]
        
        # Marcar tráfico sospechoso si la IP es la del bot conocido
        es_sospechoso = True if raw["ip"] == "192.168.1.50" else False

        mensaje_completo = {
            "titulo": info["titulo"],
            "artista": info["artista"],
            "pais": raw["pais"],
            "ip": raw["ip"],
            "dispositivo": raw["dispositivo"].upper(),
            "es_bot": es_sospechoso,
            "duracion": raw["duracion_seg"],
            "ts": raw["timestamp"]
        }
        
        producer.send('music_enriched_data', value=mensaje_completo)
        print(f"[{'ALERTA' if es_sospechoso else 'OK'}] {info['titulo']} procesado.")