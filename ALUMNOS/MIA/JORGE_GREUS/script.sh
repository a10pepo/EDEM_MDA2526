!/bin/bash
# Linux_Comandos

# Para entregar este ejercicio, debes copiar este archivo en tu carpeta de alumno y completar las respuestas a las preguntas que se formulan en el mismo.
# Una vez completado, debes subirlo a vuestro repositorio remoto de GitHub y realizar una Pull Request poniendo a Pedro Nieto como reviewer.


# Ejercicio de comandos en la consola de linux.

echo 1.Listar todos los archivos del directorio bin.
    ls /bin
    
echo 2.Listar todos los archivos del directorio tmp.

    ls /tmp
    
echo   3.Listar todos los archivos del directorio etc que empiecen por t 
    
    ls /etc/t* 

echo   4.Listar todos los archivos del directorio dev que empiecen por tty.
    
    ls /dev/tty*
    
echo   5.Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3.
    
    ls /dev/tty*3
    
echo   6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1.
    
    ls dev/t*C1

echo   7.Listar todos los archivos, incluidos los ocultos, del directorio raíz.
    
    ls -a /
    
echo   8.Listar todos los archivos del directorio etc que no empiecen por t.
    
    ls /etc/[!t]

echo   9.Listar todos los archivos del directorio usr y sus subdirectorios.
    
    ls -R /usr

echo   10.Cambiarse al directorio tmp, crear directorio PRUEBA.
    
    cd /tmp 
    mkdir PRUEBA

echo   11.Verificar que el directorio actual ha cambiado.
    
    pwd

echo   12.Mostrar el día y la hora actual.
    
    date

echo   13.Con un solo comando posicionarse en el directorio $HOME.
    
    cd

echo   14.Verificar que se está en él.
    
    pwd

echo   15.Listar todos los ficheros del directorio HOME mostrando sus permisos.
    
    ls -l /$HOME

echo   16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA.
    
    rm -rf /tmp/PRUEBA/*

echo   17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio 
echo   dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312.
    
    cd /tmp/PRUEBA
    mkdir dir1 dir2 dir3
    cd dir1 
    mkdir dir11
    cd ..
    cd dir3
    mkdir dir31
    cd dir31
    mkdir dir311 dir312
    
echo   18.Copiar el archivo /etc/mtab a vuestro directorio PRUEBA.
    
    
    cp etc/mtab /tmp/PRUEBA


echo   19.Copiar /etc/mtab en dir1, dir2 y dir3.
    
    cp mtab /tmp/PRUEBA/dir1
    cp mtab /tmp/PRUEBA/dir2
    cp mtab /tmp/PRUEBA/dir3
    
echo   20.Comprobar el ejercicio anterior mediante un solo comando.
    
    ls /tmp/PRUEBA/dir1 /tmp/PRUEBA/dir2 /tmp/PRUEBA/dir3
