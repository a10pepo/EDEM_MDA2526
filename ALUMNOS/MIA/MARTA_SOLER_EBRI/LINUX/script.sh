#!/bin/bash

rm -rf /tmp/PRUEBA

echo "Listando todos los archivos del directorio bin..."
cd /
ls /bin  
    
echo "Listando todos los archivos del directorio tmp..."
ls /tmp 

echo "Listando todos los archivos del directorio etc que empiecen por t..."
ls /etc/t*  

echo "Listando todos los archivos del directorio dev que empiecen por tty..."
ls /dev/tty* 

echo "Listando todos los archivos del directorio dev que empiecen por tty y acaben en 3..."
ls /dev/tty*3

echo "Listando todos los archivos del directorio dev que empiecen por t y acaben en C1..."
ls /dev/t*C1  

echo "Listando todos los archivos, incluidos los ocultos, del directorio raíz..."
ls -a /  

echo "Listando todos los archivos del directorio etc que no empiecen por t..."
ls /etc/[!t]*  

echo "Listando todos los archivos del directorio usr y sus subdirectorios..."
ls -R /usr  

echo "Cambiando al directorio tmp, creando directorio PRUEBA..."
cd /tmp
mkdir PRUEBA  

echo "Verificando que el directorio actual ha cambiado..."
pwd  

echo "Mostrando el día y la hora actual..."
date  

echo "Con un solo comando posicionándose en el directorio \$HOME..."
cd $HOME

echo "Verificando que se está en él..."
pwd  

echo "Listando todos los ficheros del directorio HOME mostrando sus permisos..."
ls -l   

echo "Borrando todos los archivos y directorios visibles del directorio PRUEBA..."
rm -rf /tmp/PRUEBA/*  

echo "Creando los directorios dir1, dir2 y dir3 en el directorio PRUEBA... Dentro de dir1 creando el directorio dir11... Dentro del directorio 
dir3 creando el directorio dir31... Dentro del directorio dir31, creando los directorios dir311 y dir312..."
mkdir /tmp/PRUEBA/dir1 /tmp/PRUEBA/dir2 /tmp/PRUEBA/dir3
mkdir /tmp/PRUEBA/dir1/dir11
mkdir /tmp/PRUEBA/dir3/dir31
mkdir /tmp/PRUEBA/dir3/dir31/dir311 /tmp/PRUEBA/dir3/dir31/dir312 

echo "Copiando el archivo /etc/mtab al directorio PRUEBA..."
cp /etc/mtab /tmp/PRUEBA  

echo "Copiando /etc/mtab en dir1, dir2 y dir3..."
cp /etc/mtab /tmp/PRUEBA/dir1
cp /etc/mtab /tmp/PRUEBA/dir2
cp /etc/mtab /tmp/PRUEBA/dir3

echo "Comprobando el ejercicio anterior mediante un solo comando..."
ls /tmp/PRUEBA/dir1 /tmp/PRUEBA/dir2 /tmp/PRUEBA/dir3

echo "Estructura final creada:"
ls -R /tmp/PRUEBA

echo "Script completado correctamente."