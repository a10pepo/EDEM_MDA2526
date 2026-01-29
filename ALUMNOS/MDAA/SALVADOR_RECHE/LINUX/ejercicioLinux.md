# Linux_Comandos

Para entregar este ejercicio, debes copiar este archivo en tu carpeta de alumno y completar las respuestas a las preguntas que se formulan en el mismo. Una vez completado, debes subirlo a vuestro repositorio remoto de GitHub y realizar una Pull Request poniendo a Pedro Nieto como reviewer.

Ejercicio de comandos en la consola de linux.

1.Listar todos los archivos del directorio bin.

__ls bin__

2.Listar todos los archivos del directorio tmp.

__ls tmp__

3.Listar todos los archivos del directorio etc que empiecen por t

__ls etc/t*__

4.Listar todos los archivos del directorio dev que empiecen por tty.

__ls dev/tty*__

5.Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3.

__ls dev/tty*3__

6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1.

__ls dev/t*C1__

7.Listar todos los archivos, incluidos los ocultos, del directorio raíz.

__ls -a__

8.Listar todos los archivos del directorio etc que no empiecen por t.

__ls etc/[!t]*__

9.Listar todos los archivos del directorio usr y sus subdirectorios.

__ls usr usr/*__

10.Cambiarse al directorio tmp, crear directorio PRUEBA.

__cd tmp && mkdir PRUEBA__

11.Verificar que el directorio actual ha cambiado.

__pwd__

12.Mostrar el día y la hora actual.

__date__

13.Con un solo comando posicionarse en el directorio $HOME.

__cd ../home__

14.Verificar que se está en él.

__pwd__

15.Listar todos los ficheros del directorio HOME mostrando sus permisos.

__ls -l__

16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA.

__rm -r PRUEBA__

17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312.

__mkdir PRUEBA/dir1 PRUEBA/dir2 PRUEBA/dir3 PRUEBA/dir1/dir11 PRUEBA/dir3/dir31 PRUEBA/dir3/dir31/dir311 PRUEBA/dir3/dir31/dir312__

18.Copiar el archivo /etc/mtab a vuestro directorio PRUEBA.

__cp ../etc/mtab PRUEBA/__

19.Copiar /etc/mtab en dir1, dir2 y dir3.

__cp ../etc/mtab PRUEBA/dir1/ && cp ../etc/mtab PRUEBA/dir2/ && cp ../etc/mtab PRUEBA/dir3/__

20.Comprobar el ejercicio anterior mediante un solo comando.

__ls PRUEBA/dir1 PRUEBA/dir2 PRUEBA/dir3__