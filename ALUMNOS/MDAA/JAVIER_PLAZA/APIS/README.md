# Entregable APIs (Javier Plaza Rosique).

La finalidad de esta tarea es realizar una publicación en X a partir de su API. En esta se deberán emplear otras APIs, para generar la publicación.

En este entregable, se realizarán varias aplicaciones con python, para poder llegar a comprender paso a paso como funcionan las herramientas. Siendo la última app la más completa.

## Aplicación 1. Publicación simple a partir de la API de X.

Para poder emplear dicha app, se necesitará estar dentro de la carpeta "app_inicial/". En la consola, una vez dentro de la carpeta y cumpliendo los requerimientos (expuestos posteriormente) se debe de ejecutar el siguiente comando: 

```
docker compose up --build
```
### Requerimientos.

Para poder emplear esta app, en la carpeta "app_inicial/" se debe de crear un archivo llamado ".env", con el siguiente formato: 

```
X_API_KEY=<aquí va tu API key suministrada por X>
X_API_SECRET=<aquí va tu API key secreta suministrada por X>
X_ACCESS_TOKEN=<aquí va tu token de acceso suministrado por X>
X_ACCESS_TOKEN_SECRET=<aquí va tu token de acceso secreto suministrado por X>
```

### Localizar la publicación. 

Para poder encontrar la publicación, se debe de ejecutar el siguiente comando:

```
docker logs app_inicial
```

En esto, si no ha ocurrido ningún error (principalmente por credenciales), aparecerá un id.
Dicho id se debe de poner en la siguiente url: 

```
https://twitter.com/user/status/<id>
```

En mi caso la url es:

````
https://twitter.com/user/status/2000620896147349959
````