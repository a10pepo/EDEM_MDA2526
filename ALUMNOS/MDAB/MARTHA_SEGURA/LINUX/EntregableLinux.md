1.Listar todos los archivos del directorio bin. 
 Ls /bin 
2.Listar todos los archivos del directorio tmp. 
Ls /tmp 
3.Listar todos los archivos del directorio etc que empiecen por t 
Ls /etc/t* 
4.Listar todos los archivos del directorio dev que empiecen por tty. 
Ls/dev/tty* 
5.Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3. 
Ls/dev/tty*3 
6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1. 
Ls/dev/t*c1 
7.Listar todos los archivos, incluidos los ocultos, del directorio raíz. 
Ls/-a 
8.Listar todos los archivos del directorio etc que no empiecen por t. 
Ls/etc/[!t]* 
9.Listar todos los archivos del directorio usr y sus subdirectorios. 
Ls – R /usr 
10.Cambiarse al directorio tmp, crear directorio PRUEBA. 
Cd tmp 
Mkdir Prueba 
11.Verificar que el directorio actual ha cambiado. 
pwd 
12.Mostrar el día y la hora actual. 
date 
13.Con un solo comando posicionarse en el directorio $HOME.  
Cd ~ 
14.Verificar que se está en él.  
pwd 
15.Listar todos los ficheros del directorio HOME mostrando sus permisos. 
Ls -l 
16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA. 
Rm – rf Prueba 
17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312. 
Mk dir 1 dir3 dir 3 
Mkdir dir1/dir11 
Mkdir dir 3/dir31 
mkdir dir3/dir31/dir311 dir3/dir31/dir312 
18.Copiar el archivo /etc/mtab a vuestro directorio PRUEBA. 
cp /etc/mtab ~/PRUEBA/ 
19.Copiar /etc/mtab en dir1, dir2 y dir3. 
cp /etc/mtab ~/PRUEBA/dir1/ 
cp /etc/mtab ~/PRUEBA/dir2/ 
cp /etc/mtab ~/PRUEBA/dir3/ 
20.Comprobar el ejercicio anterior mediante un solo comando. 
ls -l ~/PRUEBA/dir{1,2,3}/mtab 