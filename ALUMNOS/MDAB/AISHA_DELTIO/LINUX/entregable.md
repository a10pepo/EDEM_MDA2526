NOMBRE: AISHA DEL TIO DE PRADO

Para entregar este ejercicio, debes copiar este archivo en tu carpeta de alumno y completar las respuestas a las preguntas que se formulan en el mismo. Una vez completado, debes subirlo a vuestro repositorio remoto de GitHub y realizar una Pull Request poniendo a Pedro Nieto como reviewer.
Ejercicio de comandos en la consola de linux.

1.Listar todos los archivos del directorio bin.
ls -l /bin

2.Listar todos los archivos del directorio tmp.
ls -l /tmp

3.Listar todos los archivos del directorio etc que empiecen por t
ls -l /etc/t*

4.Listar todos los archivos del directorio dev que empiecen por tty.
ls -l /dev/tty*

5.Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3.
ls -l /dev/tty*3

6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1.
ls -l /dev/t*C1

7.Listar todos los archivos, incluidos los ocultos, del directorio raíz.
ls -la /

8.Listar todos los archivos del directorio etc que no empiecen por t.
ls /etc/!(t*)

9.Listar todos los archivos del directorio usr y sus subdirectorios.
ls -lR /usr

10.Cambiarse al directorio tmp, crear directorio PRUEBA.
cd /tmp
mkdir PRUEBA
NOTA: mkdir /tmp/PRUEBA

11.Verificar que el directorio actual ha cambiado.
pwd

12.Mostrar el día y la hora actual.
date

13.Con un solo comando posicionarse en el directorio $HOME.
cd ~

14.Verificar que se está en él.
pwd

15.Listar todos los ficheros del directorio HOME mostrando sus permisos.
ls -l /home

16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA.
cd /tmp/PRUEBA
rm -r *
NOTA: Estamos borrando el contenido, no la carpeta. Si quisiesemos borrar la carpeta: rm -r /tmp/PRUEBA

17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312.
cd /tmp/PRUEBA
mkdir dir1 dir2 dir3
mkdir dir1/dir11
mkdir dir3/dir31
mkdir dir3/dir31/dir311
mkdir dir3/dir31/dir312
NOTA: mkdir -p dir1/dir11 dir2 dir3/dir31/dir311 dir3/dir31/dir312

18.Copiar el archivo /etc/mtab a vuestro directorio PRUEBA.
cp etc/mtab tmp/PRUEBA
19.Copiar /etc/mtab en dir1, dir2 y dir3.
cp /etc/mtab /tmp/PRUEBA/dir1
cp /etc/mtab /tmp/PRUEBA/dir2
cp /etc/mtab /tmp/PRUEBA/dir3

NOTA: for d in dir1 dir2 dir3; do cp /etc/mtab /tmp/PRUEBA/$d/; done

20.Comprobar el ejercicio anterior mediante un solo comando.
OPCION1: ls -l /tmp/PRUEBA/dir1 /tmp/PRUEBA/dir2 /tmp/PRUEBA/dir3
OPCION2: find /tmp/PRUEBA -name mtab

NOTA: for d in dir1 dir2 dir3; do ls -l /tmp/PRUEBA/$d; done
