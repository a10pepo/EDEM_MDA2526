En este fichero documento como se ha creado cada uno de los recursos usados en el ejercicio e2e de GCP Storage propuesto durante las clases de EDEM.
Todos los elementos se han creado dentro del proyecto "gcp-storage-e2e-terraform" en GCP. 


## Imagen de VM

Primero he creado una imagen de máquina llamada "e2e-vm-image" que nos servirá para generar las VM instances posteriores. 
Esta imagen la he creado a través de la consola, y es de una maquina e2-micro ubicada en europe-west1.

![snips/vm_image.jpg](snips/vm_image.jpg)

## VM Instance (Orders App)

Una vez creada la imagen de máquina, he pasado a crear las dos instancias de VM con Terraform:

![snips/orders_app_VM_tf.jpg](snips/orders_app_VM_tf.jpg)

Tanto el project id como el nombre de la imagen se han declarado como variables definidas en terraform.tfvars
![snips/terraform_vars.jpg](snips/terraform_vars.jpg)

## VM Instance (Delivery App)

Después pasamos a desplegar la Instancia de Delivery App desde terrafrom con la misma imagen:

![snips/delivery_app_VM_tf.jpg](snips/delivery_app_VM_tf.jpg)


## Base de datos transaccional (Cloud SQL instance)
Para simular la base de datos operativa de la empresa, desplegamos una instancia de Cloud SQL con postgres.

Con las VM ya activas, pasamos a crear la instancia de CloudSQL a través de terraform también. 

![alt text](snips/sql_instance_tf.jpg)

El nombre de la instrancia y la región también se ha definido como variable en terraform:
![alt text](snips/sql_instance_variables.jpg)

A continuación creamos el usuario y la base de datos "ecommerce" con terraform también:
![alt text](snips/sql_user_database_tf.jpg)


## Datalake (GCS bucket)
Hemos creado un datalake (Bucket de GCS) donde guardar la información adicional de los pedidos en formato parquet a partir del order generator script. Esto nos permite almacenar la información adicional de forma mas eficiente a menor coste.
El bucket lo creamos con terraform también, y para asegurarme que el nombre es único en GCS lo he creado concatenando un prefijo con el nombre de mi proyecto (que incluye mi nombre de usuario).

![alt text](snips/datalake_gcs_tf.jpg)
![alt text](snips/GCS_buckets_created.jpg)
![alt text](snips/GCS_parquet_file_data.jpg)

## PubSub 

Para el envio de mensajes entre el Orders app, Delivery app, y el Analytical DB (BigQuery), usamos dos topics de PubSub.
Esto lo hacemos también con terraform: 
![alt text](snips/pubsub_order_topic_subscription_creation_tf.jpg)
![alt text](pubsub_topics_created.jpg)
El topic "order-events" mandará información de los pedidos creados con el script en la Orders-app VM al topic de pubsub, y la Delivery-app los leerá con la suscripción creada. Después la Delivery App mandará los eventos de delivery al topic Deliver-events, que lo conectará con BQ a través de otra suscripción. 
Tabién se ha creado una suscripción "dead letter" para recoger los mensajes no entregados después de 5 intentos.
 ![alt text](snips/pubsub_delivery_subscription_to_BQ_tf.jpg)
 ![alt text](snips/pubsub_delivery_topic_with_bq_subscription.jpg)


## Data warehouse (BigQuery)

Aqui creamos nuestra base de datos analítica.

Primero aprovisiono los Datasets vacíos para recibir los datos, y después creamos las tablas con sus esquemas:
![alt text](snips/BQ_datasets_tables_tf.jpg)

Se puede ver todos los recursos en el código de terraform adjunto.

Para insertar los datos desde la base de datos transaccional (CloudSQL) a la analítica, ejecutamos un EL job ya proporcionado en el repo en local.
Una vez aplicamos los cambios de terraform y ejecutamos las apps en las VMs, podemos ver en la consola tanto los datasets (delivery_bronze & orders_bronze) como las tablas creadas y los datos insertandose:
![alt text](snips/bigquery_datasets_tables_populated.jpg)

## DBT

La transformación de los datos raw insetrados en BigQuery en los datasets "Bronze" se produce con DBT en local, con el modelo proporcionado en el repo. Una vez se ejecuta, podemos ver los datasets (dbt_dataset, dbt_dataset_analytics & dbt_dataset_delivery_gold) y las tablas creadas y pobladas con los datos:
![alt text](snips/bigquery_dbt_customers_data.jpg)

## Metabase

Para la visualización de los datos, usamos Metabase en local. El programa lo ejecutamos corriendo el docker compose proporcionado:
![alt text](snips/metabase_docker_compose_running.jpg)

Para identificarnos y que pueda conectarse a nuestro proyecto cloud, hemos creado una Srevice account con permisos de administrador de BQ: 
 ![alt text](snips/service_account_metabase_BQ.jpg)

 Posteriormente generamos las credenciales en formato JSON que subiremos a Metabase para acceder a los datos. 
 Una vez tengamos los datos, generamos gráficos relevantes para reportar las métricas de negocio. En este caso he creado un gráfico con los Top 5 productos más vendidos (por ingresos), una pie chart con el porcentaje de ingresos que representa cada cliente, y un gráfico de barras con el estado total de entrega de los pedidos:
 ![alt text](snips/metabase_customer_stake.jpg)
 Después he insetrado todos los gráficos en un cuadro de mando:
 ![alt text](snips/metabase_cuadro_de_mando.jpg)
 
 Y con esto estaria completo el proyecto.


