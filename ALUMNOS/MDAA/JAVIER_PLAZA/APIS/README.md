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

Y la publicación es la siguiente: 

![Imagen publicación X con la app_inicial](.img/image.png)

## Aplicación 2. Creación de una API.

Para poder emplear esta app, se debe de estar dentro del directorio "api_v2/". En la consola, una vez dentro de la carpeta y cumpliendo los requerimientos (expuestos posteriormente) se debe de ejecutar el siguiente comando: 

```
docker compose up --build
```

### Requerimientos.

Para poder emplear esta app, en el directorio "api_v2/" se debe de crear un archivo llamado ".env", con el siguiente formato: 

```
JWT_SECRET_KEY=<aquí va una contraseña, que le dará seguridad a los tokens que se crean en la app>
```

### Uso de la API con Postman. 

La API, está configurada para tener que usarse secuencialmente. Es decir, que para poder obtener la información de una fruta aleatoria, se tienen que seguir algunos pasos anteriormente. Dichos pasos son los siguientes: 

1. Crear un usuario en la URL: "http://127.0.0.1:5000/usuarios". El usuario y la contraseña se deben de poner en formato JSON. Tal y como se muestra en la imagen. 

![Creación de un usuario en Postman](.img/image2.png)

2. A partir del usuario y la contraseña, se debe de generar un token en la URL: "http://127.0.0.1:5000/login". **El token debe de guardarse**. Para generar el token, debe de realizarse tal y como se muestra en la siguiente imagen. 

![Creación de un usuario en Postman](.img/image3.png)

3. Con el token generado anteriormente, ya se puede obtener la información de la fruta aleatoriamente. Se sebe de realizar tal y como se muestra en la imagen.

![Obtención de la información nutricional de una fruta aleatoria en Postman](.img/image4.png)

### Uso de la API con un script de Python.

En el directorio "api_v2/" se encuentra el archivo "consumir_api.py". Dicho script, cuando se realiza el primer paso, muestra en los logs del contenedor la información de la fruta aleatoriamente.

Para ver los logs del contenedor, se debe de realizar lo siguiente:

```
docker logs consumir_api
```
