
1. Creación de los Topics

![Topics](images/1.png)

2. Creación de la instancia orders-app-semaiz y delivery-app-semaiz

![Compute engine instances](images/2.png)

3. Creación de la instancia de Cloud SQL

![Cloud SQL Instance](images/3.png)

4. Creamos la database ecommerce

![Ecommerce Database](images/4.png)

5. Nos conectamos ambas instancias, hacemos un pull del repositorio e instalamos los requirements en un entorno virtual

![Instances configuration](images/5.png)

6. Creamos los datasets en big query con sus respectivas tablas

![BigQuery datasets](images/6.1.png)

![Orders tables](images/6.2.png)

![Delivery table](images/6.3.png)

7. Creamos la suscripción de pub/sub para el topic delivery-events

![Delivery-events subscription](images/7.png)

8. Sincronizamos la bd postgres en cloud sql con el dataset en big query

![Cloud SQL - BigQuery synchronization](images/8.png)

9. Creamos la carpeta dbt e iniciamos el proyecto

![DBT](images/9.png)

10. Generamos las visualizaciones de los delivery events

![delivery-events view](images/10.png)

11. Generamos las tablas

![DBT Tables](images/11.png)

12. Generamos el dashboard con las visualizaciones

![Metabase dashboard](images/12.png)


