# Entregable End2End GCP Almacenamiento. Carlos Beltrán

Se parte de la siguiente imagen para la infraestructura. 

<p align="center">
<img src=".images/arquitectura.png" alt="drawing" width="500"/>
</p>


Se ha utilizado Terraform para el despliegue de los recursos y se han utilizado:

- Dos maquinas virtuales

<p align="center">
<img src=".imagenes_entrega/maquinas_virtuales.png" alt="drawing" width="500"/>
</p>

- Dos tópicos con sus suscripciones

<p align="center">
<img src=".imagenes_entrega/topicos.png" alt="drawing" width="500"/>
</p>

- Una instancia de Cloud SQL

<p align="center">
<img src=".imagenes_entrega/cloud_sql.png" alt="drawing" width="500"/>
</p>

- Dos datasets, delivery_bronze y orders_bronze

<p align="center">
<img src=".imagenes_entrega/dataset.png" alt="drawing" width="500"/>
</p>

- Un subtópico en el topico de delivery para publicar en BigQuery

<p align="center">
<img src=".imagenes_entrega/delivery_subtopic.png" alt="drawing" width="500"/>
</p>


