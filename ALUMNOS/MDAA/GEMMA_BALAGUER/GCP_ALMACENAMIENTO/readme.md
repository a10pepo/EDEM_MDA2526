1. Creamos el bucket desde gcp
![configuración_bucket](image.png)

2. Tópicos order-events y delivery-events en gcp.
![orders-events](image-3.png)
![delivery-events](image-4.png)

3. Instancias orders-app y delivery-app en gcp.
![instancias](image-5.png) 

4. Instancia de Postgresen gcp. 
![Instancia de postgres](image-6.png)

5. Base de datos ecommerce en gcp. 
![ecommerce](image-7.png)

7. Ejecutamos los siguientes comandos en las dos instancias: 

**Log in to the instance:**
   ```sh
   gcloud compute ssh <instance-name> --zone=europe-west1-b
   ```
![orders-app](image-9.png)

**Clone or pull latest changes from this repository**
```sh
git clone https://github.com/frkroe/gcp-storage.git
``` 
Pero antes de ejecutarlo debemos descargar el paquete necesario (en este caso, no es necesaria la confirmación):

```sh
sudo apt-get update
sudo apt-get install git -y
```
![orders-app](image-10.png)
![delivery-app](image-15.png)

**Move to the correct directory:**
   ```sh
   cd gcp-storage/gcp_datawarehouse/exercise_end2end
   ```
![orders-app](image-11.png)
![delivery-app](image-16.png)

**Create a virtual environment:**
   ```sh
   python3 -m venv .venv
   ```
Para ejecutar el anterior comando, primero debemos instalar el paquete necesario (python3-venv). Por eso antes debemos ejecutar:
```sh
sudo apt-get update
sudo apt-get install python3-venv -y
```
![orders-app](image-12.png)
![delivery-app](image-17.png)

**Activate the venv:**
   ```sh
   source .venv/bin/activate
   ```
![orders-app](image-13.png)
![delivery-app](image-18.png)

**Install the requirements:**
   ```sh
   pip install -r requirements.txt
   ```
![orders-app](image-14.png)
![delivery-app](image-19.png)

8. Creamos las tablas dentro de la base de datos de ecommerce (creadas desde Cloud SQL Studio )**
![tablas de ecommerce](image-8.png)

9. For the `orders-app` instance
Para ejecutar tu aplicación orders-app en segundo plano usando nohup (de modo que siga corriendo aunque cierres la terminal):
   
   ```sh
   nohup bash -c 'HOST_IP=35.205.184.23 GCS_BUCKET_NAME=e2e-gemma-balaguer PROJECT_ID=e2e_gemma_balaguer python -m orders-app.orders_to_db.main' > output.log 2>&1 &
   ```
![orders-app](image-21.png)

This will start creating orders, store them in the database and publish confirmation events to the `order-events` topic.

If you want to see the logs, run the following command:
```sh
tail -f output.log
```


### For the `delivery-app` instance

1. Run the following command to start the `delivery-app`:
   ```sh
   nohup bash -c 'PROJECT_ID=<your-project-id> python -m delivery_app.main' > output.log 2>&1 &
   ```

If you want to see the logs, run the following command:
```sh
tail -f output.log
```

This will start consuming the events from the `order-events` topic and publish delivery events to the `delivery-events` topic.

![bucket creado](image-1.png)
![terraform](image-2.png)

