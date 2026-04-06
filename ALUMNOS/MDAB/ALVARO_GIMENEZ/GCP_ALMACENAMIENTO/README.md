# Entregable GCP Almacenamiento

# Creamos los tópicos de Pub/Sub: 

![Pub/Sub topics](images/pubsub.png)

# Creamos las máquinas virtuales a partir de la imagen base previamente creada

![Pub/Sub topics](images/compute_eng.png)

# Creamos la instancia de cloud sql y creamos las tablas

![Pub/Sub topics](images/cloud_sql1.png)

![Pub/Sub topics](images/cloud_sql2.png)

#  Creamos los datasets de Bigquery

![Pub/Sub topics](images/orders_BQ.png)
![Pub/Sub topics](images/delivery_BQ.png)

# Nos logeamos en las VM e instalamos los requirements
![alt text](images/vm_req.png)

# Ejecutamos orders app y delivery app
![alt text](images/vm_ejec.png)

# Comprobamos que se insertan los logs en CLOUD SQL y BIGQuery
![alt text](images/cloud_sql_logs.png)
![alt text](images/bigquery_logs.png)

# Ejecutamos la ETL de cloud SQL -> Bigquery
![alt text](images/ETL.png)