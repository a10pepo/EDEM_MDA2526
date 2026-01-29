#!/bin/bash

# Directorio de trabajo = carpeta donde está el script (carpeta LINUX).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo "   Prueba automática - Linux_Comandos"
echo "   Directorio de trabajo: $SCRIPT_DIR"
echo "========================================"
echo

# Limpieza y preparación
echo "[PRE] Limpiar ejecuciones anteriores"
rm -rf "$SCRIPT_DIR/PRUEBA"
echo

# 1
echo "[1] Listar todos los archivos del directorio bin"
echo '$ ls /bin'
ls /bin
echo

# 2
echo "[2] Listar todos los archivos del directorio tmp"
echo '$ ls /tmp'
ls /tmp
echo

# 3
echo "[3] Listar todos los archivos de /etc que empiecen por t"
echo '$ ls /etc/t*'
ls /etc/t*
echo

# 4
echo "[4] Listar todos los archivos de /dev que empiecen por tty"
echo '$ ls /dev/tty*'
ls /dev/tty*
echo

# 5
echo "[5] Listar todos los archivos de /dev que empiecen por tty y acaben en 3"
echo '$ ls /dev/tty*3'
ls /dev/tty*3
echo

# 6
echo "[6] Listar todos los archivos de /dev que empiecen por t y acaben en C1"
echo '$ ls /dev/t*C1'
ls /dev/t*C1
echo

# 7
echo "[7] Listar todos los archivos, incluidos los ocultos, del directorio raíz"
echo '$ ls -a /'
ls -a /
echo

# 8
echo "[8] Listar todos los archivos de /etc que NO empiecen por t"
echo '$ ls /etc/[!t]*'
ls /etc/[!t]*
echo

# 9
echo "[9] Listar todos los archivos de /usr y sus subdirectorios (recursivo)"
echo '$ ls -R /usr'
ls -R /usr
echo

# 10
echo "[10] Crear PRUEBA en el directorio del script (sin cambiar de carpeta)"
echo "\$ mkdir -p \"$SCRIPT_DIR/PRUEBA\""
mkdir -p "$SCRIPT_DIR/PRUEBA"
echo

# 11
echo "[11] Verificar directorio actual"
echo '$ pwd'
pwd
echo

# 12
echo "[12] Mostrar día y hora actual"
echo '$ date'
date
echo

# 13
echo "[13] Posicionarse en el directorio \$HOME con un solo comando"
echo '$ cd "$HOME"'
cd "$HOME"
echo

# 14
echo "[14] Verificar que estamos en \$HOME"
echo '$ pwd'
pwd
echo

# 15
echo "[15] Listar ficheros de \$HOME mostrando permisos"
echo '$ ls -la "$HOME"'
ls -la "$HOME"
echo

# 16
echo "[16] Borrar todos los archivos y directorios visibles de PRUEBA (en la carpeta del script)"
echo "\$ rm -rf \"$SCRIPT_DIR/PRUEBA/*\""
rm -rf "$SCRIPT_DIR/PRUEBA/"*
echo

# 17
echo "[17] Crear árbol de directorios en PRUEBA (dir1/dir11, dir2, dir3/dir31/{dir311,dir312})"
echo "\$ mkdir -p \"$SCRIPT_DIR/PRUEBA/dir1/dir11\" \"$SCRIPT_DIR/PRUEBA/dir2\" \"$SCRIPT_DIR/PRUEBA/dir3/dir31/dir311\" \"$SCRIPT_DIR/PRUEBA/dir3/dir31/dir312\""
mkdir -p \
    "$SCRIPT_DIR/PRUEBA/dir1/dir11" \
    "$SCRIPT_DIR/PRUEBA/dir2" \
    "$SCRIPT_DIR/PRUEBA/dir3/dir31/dir311" \
    "$SCRIPT_DIR/PRUEBA/dir3/dir31/dir312"
echo

# 18
echo "[18] Copiar /etc/hosts a PRUEBA"
echo "Se utiliza /etc/hosts ya que ha sido ejecutado en macOS y no existe /etc/mtab"
echo "\$ cp /etc/hosts \"$SCRIPT_DIR/PRUEBA/\""
cp /etc/hosts "$SCRIPT_DIR/PRUEBA/"
echo

# 19
echo "[19] Copiar /etc/hosts en dir1, dir2 y dir3"
echo "\$ cp /etc/hosts \"$SCRIPT_DIR/PRUEBA/dir1/\"; cp /etc/hosts \"$SCRIPT_DIR/PRUEBA/dir2/\"; cp /etc/hosts \"$SCRIPT_DIR/PRUEBA/dir3/\""
cp /etc/hosts "$SCRIPT_DIR/PRUEBA/dir1/"; cp /etc/hosts "$SCRIPT_DIR/PRUEBA/dir2/"; cp /etc/hosts "$SCRIPT_DIR/PRUEBA/dir3/"
echo

# 20
echo "[20] Comprobar el ejercicio anterior en un solo comando"
echo "\$ ls \"$SCRIPT_DIR/PRUEBA/dir\"{1,2,3}/hosts"
ls "$SCRIPT_DIR/PRUEBA/dir"{1,2,3}/hosts
echo

echo "========================================"
echo "Prueba finalizada."
echo "========================================"
