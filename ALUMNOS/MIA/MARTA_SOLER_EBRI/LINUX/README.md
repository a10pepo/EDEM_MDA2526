# ENTREGABLE LINUX

## Objetivo

Desarrollar un script en Bash que nos permite realizar una serie de tareas de forma automática. Bases del ejercicio:
1. Las carpetas deben crearse en la carpeta de Usuario de cada alumno 
   dentro de LINUX.
2. El script debe ser capaz de crear las carpetas y los archivos 
   necesarios para realizar las tareas sin intervención del usuario 
   más allá de su ejecución.
3. El script debe ser reejecutable sin necesidad de modificarlo, por lo 
   que debe borrar al inicio lo creado en la ejecución anterior.
4. El script debe mostrar una leyenda al inicio de cada tarea indicando 
   que tarea se va a realizar.

## Instrucciones 

Creamos un nuevo archivo llamado `script.sh`, debe tener siempre la siguiente primera línea:
````
#!/bin/bash
````

Luego a este script le añadimos los comandos del ejercicio junto con explicaciones, usando `echo`.

Para poder ejecutar comandos de Linux en la terminal de VSC se necesita usar una imagen de `ubuntu` y ejecutar el contenedor. Ejecutamos:
````
docker create -it --name unix ubuntu:latest
docker start unix
docker exec -it unix /bin/bash
apt update
apt install vim
````

Una vez ejecutado deberíamos ver algo como:
````
root@f0b3c2c3f0b3:/#
````

Ahora ejecutamos:
````
vi script.sh
````

Una vez dentro de vi pulsamos `a` para entrar en modo edición **--INSERT--**. Ahora copiamos el contenido del script con el botón derecho, una vez pegado pulsamos `Esc` y escribimos `:wq` para guardar y salir del editor.

Una vez guardado el script tenemos que darle permisos de ejecución:
````
chmod 777 script.sh
````

Finalmente ejecutamos:
````
./script.sh
````