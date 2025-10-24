<!-- Ejercicio de comandos en la consola de linux.

1.Listar todos los archivos del directorio bin. -->

ls /bin

<!-- 2.Listar todos los archivos del directorio tmp. -->

ls /tmp

<!-- 3.Listar todos los archivos del directorio etc que empiecen por t -->

ls /etc/t*

<!-- 4.Listar todos los archivos del directorio dev que empiecen por tty. -->

ls /etc/tty*

<!-- 5.Listar todos los archivos del directorio dev que empiecenpwd -->
 <!-- por tty y acaben en 3. -->

ls /dev/tty*3

<!-- 6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1. -->

ls /dev/t*C1

<!-- 7.Listar todos los archivos, incluidos los ocultos, del directorio raíz. -->

ls -a /

<!-- 8.Listar todos los archivos del directorio etc que no empiecen por t. -->

ls /etc/[!t]*

<!-- 9.Listar todos los archivos del directorio usr y sus subdirectorios. -->

ls -R /usr

<!-- 10.Cambiarse al directorio tmp, crear directorio PRUEBA. -->

cd /tmp mkdir PRUEBA

<!-- 11.Verificar que el directorio actual ha cambiado. -->

pwd

<!-- 12.Mostrar el día y la hora actual. -->

date

<!-- 13.Con un solo comando posicionarse en el directorio $HOME. -->

cd ~

<!-- 14.Verificar que se está en él. -->

pwd

<!-- 15.Listar todos los ficheros del directorio HOME mostrando sus permisos. -->

ls -la ~  

<!-- 16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA. -->

rm -r/ tmp/PRUEBA/*

<!-- 17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA.  -->
<!-- Dentro de dir1 crear el directorio dir11. 
Dentro del directorio dir3 crear el directorio dir31. 
Dentro del directorio dir31, crear los directorios dir311 y dir312. -->

cd/tmp/PRUEBA
mkdir -p dir1/dir11 dir2 dir3/dir31/dir311 dir3/dir31/dir312


<!-- 18.Copiar el archivo /etc/mtab a vuestro directorio PRUEBA. -->

 <!-- En macOS el archivo /etc/mtab no existe, así que usamos /etc/hosts. -->
 <!-- Este comando copia el archivo /etc/hosts al directorio /tmp/PRUEBA. -->
cp /etc/hosts /tmp/PRUEBA/

<!-- 19.Copiar /etc/mtab en dir1, dir2 y dir3. -->

<!-- w En macOS el archivo /etc/mtab no existe, por eso usamos /etc/hosts. -->
<!--  Este comando copia el archivo /etc/hosts dentro de las carpetas dir1, dir2 y dir3 del directorio PRUEBA. -->
cp /etc/hosts /tmp/PRUEBA/dir1
cp /etc/hosts /tmp/PRUEBA/dir2
cp /etc/hosts /tmp/PRUEBA/dir3

cp /etc/hosts /tmp/PRUEBA/dir{1,2,3}/

<!-- 20.Comprobar el ejercicio anterior mediante un solo comando. -->

ls -l /tmp/PRUEBA/dir{1,2,3}/