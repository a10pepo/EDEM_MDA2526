# Configuración PostgreSQL

Siguiendo estos pasos podremos configurarnos desde Docker nuestra base de datos con PostgreSQL


# Extensión VSC de PostgreSQL

Nos instalamos la siguiente extensión: https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql

## Configuramos nuestro proyecto con PostgreSQL

Creamos una carpeta  **mi_proyecto** y abrimos el VSC en esa carpeta. Después creamos un archivo llamado **docker-compose.yml** con el siguiente código:
```yaml
services:
	db:
		image: postgres:17-alpine
		env_file:
			- .env
		volumes:
			- postgresDB:/var/lib/postgresql/data
		ports:
			- "5433:5432"
		restart: unless-stopped

volumes:
		postgresDB:
```
Nos creamos nuestro archivo **.env** con los datos para conectarnos a la base de datos:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=pruebadb
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/pruebadb
```
**OJO** En nuestro archivo **.env** hay información sensible entonces debemos tener cuidado con no subirlo a internet, en nuestro caso a nuestro repositorio de github. Para evitar que se suba crearemos un **.gitignore** en este archivo escribimos lo que queramos que git ignore, es decir, lo que no queramos subir:
```
.env
```
Abrimos nuestra terminal de VSC y arrancamos nuestro contenedor de docker-compose con el siguiente comando: 

```bash
docker compose up -d
```

La estructura del proyecto debe quedar finalmente de la siguiente forma:

![img](./images/Captura%20de%20pantalla%202025-10-17%20114451.png)

## Conexión a nuestro PostgreSQL

Vamos a nuestra extensión de PostgreSQL que habíamos instalado previamente y clicamos en **Add Contection**.

![img](./images/Captura%20de%20pantalla%202025-10-17%20112521.png)

Después clicamos en **Connection String** y pegamos donde pone Paste Connection String la siguiente url: > postgresql://postgres@127.0.0.1:5433/pruebadb

![img](./images/Captura%20de%20pantalla%202025-10-17%20113408.png)

Seguidamente en password ponemos la contraseña que pusimos en el arhivo .env **postgres**

![img](./images/Captura%20de%20pantalla%202025-10-17%20113435.png)

Clicamos en **Save & Connect** y ya lo tenemos.

![img](./images/Captura%20de%20pantalla%202025-10-17%20113446.png)

Resultado final:

![img](./images/Captura%20de%20pantalla%202025-10-17%20113500.png)