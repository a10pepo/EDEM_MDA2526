#!/bin/bash
ls /bin
ls /tmp
ls /etc/t*
ls /dev/tty*
ls /dev/tty*3
ls /dev/t*C1
ls -a /
ls /etc/[!t]*
ls -R /usr
cd /tmp && mkdir PRUEBA
pwd
date
cd ~
pwd
ls -l ~
rm -rf /tmp/PRUEBA/*
mkdir -p /tmp/PRUEBA/dir1/dir11 /tmp/PRUEBA/dir2 /tmp/PRUEBA/dir3/dir31/dir311 /tmp/PRUEBA/dir3/dir31/dir312
cp /etc/mtab /tmp/PRUEBA/
cp /etc/mtab /tmp/PRUEBA/dir1 /tmp/PRUEBA/dir2 /tmp/PRUEBA/dir3
ls -l /tmp/PRUEBA/dir*
