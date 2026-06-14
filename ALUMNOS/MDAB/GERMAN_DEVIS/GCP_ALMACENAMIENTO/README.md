En este ejercicio migramos el flujo de datos del data warehouse que usábamos en el módulo de Cloud Intro hacia un stack 100% gestionado en Google Cloud Platform.
(Disclaimer, mi cuenta gratuita de GCP caducó, por lo que estoy reciclando un proyecto compartido. Es incorrecto, pero suponía un retraso dar de alta una cuenta completamente nueva)

1. Crear los topics de Pub/Sub

![topics](image.png)

2. Creación de las instancias

![VMinstances](image-1.png)

3. Create the Cloud SQL instance

![cloudsqlinstance](image-2.png)

4. Instances

![instances](image-3.png)

5. For the orders-app instance

![orders](image-4.png)

6. For the delivery-app instance

![delivery](image-5.png)

7. Datasets BQ

![datasets](image-6.png)
![orders-tablas](image-7.png)


8. Suscripciones

![subscription](image-8.png)



9. Sincronizamos CloudSQL con BQ

![sincro](image-9.png)

10. DBT

![DBT](image-10.png)

11. Dashboard
    
![metamase](image-11.png)

