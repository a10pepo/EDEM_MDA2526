# Entregable End2End GCP Almacenamiento. Carlos Beltrán

Se parte de la siguiente imagen para la infraestructura.

<p align="center">
<img src=".images/arquitectura.png" alt="drawing" width="500"/>
</p>

## SETUP

Se ha utilizado Terraform para el despliegue de los recursos y se han utilizado:

- 1 service account creada desde la cong¡sola de GCP

- 2 maquinas virtuales

<p align="center">
<img src=".imagenes_entrega/maquinas_virtuales.png" alt="drawing" width="500"/>
</p>

- 3 tópicos con sus suscripciones

<p align="center">
<img src=".imagenes_entrega/pubsub.png" alt="drawing" width="500"/>
</p>

- 1 instancia de Cloud SQL

<p align="center">
<img src=".imagenes_entrega/cloud_sql.png" alt="drawing" width="500"/>
</p>

- 2 datasets, delivery_bronze y orders_bronze

<p align="center">
<img src=".imagenes_entrega/dataset.png" alt="drawing" width="500"/>
</p>

- 1 bucket de cloud storage par el data lake

<p align="center">
<img src=".imagenes_entrega/bucket_data_lake.png" alt="drawing" width="500"/>
</p>

- Las sentencias sql para crear las tablas de dbt se ejecutan en el archivo main.tf

<p align="center">
<img src=".imagenes_entrega/dbt.png" alt="drawing" width="500"/>
</p>

## Envio de datos

Se han enviado datos a través de la maquina virtual de orders-app

<p align="center">
<img src=".imagenes_entrega/orders_send_data.png" alt="drawing" width="500"/>
</p>

y delivery-app

<p align="center">
<img src=".imagenes_entrega/delivery_send_data.png" alt="drawing" width="500"/>
</p>

Los datos que se envian se guardan en la base de datos de Cloud SQL

<p align="center">
<img src=".imagenes_entrega/cloud_sql_inserts.png" alt="drawing" width="500"/>
</p>

Los datos que se envian se guardan tambien en el bucket del data lake

<p align="center">
<img src=".imagenes_entrega/bucket_parquet.png" alt="drawing" width="500"/>
</p>

Los datos que se envian se pueden ver como llegan a los topicos de pubsub

<p align="center">
<img src=".imagenes_entrega/pubsub_messages.png" alt="drawing" width="500"/>
</p>

De manera local, se transforman los registros para dbt y poder verlos en BigQuery

<p align="center">
<img src=".imagenes_entrega/big_query_transform.png" alt="drawing" width="500"/>
</p>

Si vamos a BigQuery, podemos ver los datos transformados

<p align="center">
<img src=".imagenes_entrega/big_query_inserted.png" alt="drawing" width="500"/>
</p>

## Metabase

Una vez tenemos el contenedor de metabase y creamos nuestra cuenta tenemos acceso a la pagina principal

<p align="center">
<img src=".imagenes_entrega/metabase_main.png" alt="drawing" width="500"/>
</p>

Tenemos que añadir la base de datos de BigQuery, para ello, primero es necesario ir al servicio de Service account de la consola de Google, elegir la service account que se ha creado en el terraform y crear una clave

<p align="center">
<img src=".imagenes_entrega/metabase_added_db.png" alt="drawing" width="500" >
</p>

En la pantalla principal podemos añadir nuevas "preguntas" a BigQuery, por ejemplo de la tabla orders_bronze podemos ver las ordenes

<p align="center">
<img src=".imagenes_entrega/metabase_orders.png" alt="drawing" width="500" >
</p>

Podemos hacer varias "preguntas" o consultas a BigQuery para crear un dashboard

<p align="center">
<img src=".imagenes_entrega/metabase_dashboard.png" alt="drawing" width="500" >
</p>
