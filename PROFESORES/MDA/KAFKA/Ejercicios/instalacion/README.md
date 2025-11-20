# Guía rápida: Instalar Python 3.10, crear entornos virtuales e instalar la librería de Kafka

Este documento explica cómo instalar **Python 3.10** y crear un **entorno virtual** e instalar la **librería de Kafka** en Windows, Linux y macOS. 

Puedes usarlo si cuando lanzas un Producer o Consumer de Kafka no te funciona por posibles incompatibilidades de Python y Kafka.

---

## Windows

### 1. Instalar Python 3.10
```powershell
winget install Python.Python.3.10
```
**¿Qué hace?** Descarga e instala Python 3.10 usando el gestor de paquetes `winget`.

### 2. Verificar instalación
```powershell
py -3.10 --version
```
**¿Por qué este comando?** Comprueba que la versión instalada es **3.10**. Usamos `-3.10` para asegurarnos de que no estamos usando otra versión (por ejemplo, 3.11). Si solo usas `python --version`, puede mostrar otra versión si tienes varias instaladas.

### 3. Crear entorno virtual
```powershell
py -3.10 -m venv venv
```
**¿Qué hace?** Crea una carpeta llamada `venv` con un entorno aislado donde instalarás tus dependencias sin afectar el sistema.

### 4. Activar entorno virtual
```powershell
venv\Scripts\activate
```
**¿Qué hace?** Activa el entorno virtual para que los comandos `python` y `pip` usen la versión y librerías del entorno.

---

## Linux (Debian/Ubuntu)

### 1. Instalar Python 3.10
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv -y
```
**¿Qué hace?** Actualiza los repositorios e instala Python 3.10 y el módulo `venv` necesario para crear entornos virtuales.

### 2. Verificar instalación
```bash
python3.10 --version
```
**¿Por qué este comando?** Igual que en Windows, asegura que estás usando la versión correcta (3.10) y no otra.

### 3. Crear entorno virtual
```bash
python3.10 -m venv venv
```
**¿Qué hace?** Crea la carpeta `venv` con el entorno virtual.

### 4. Activar entorno virtual
```bash
source venv/bin/activate
```
**¿Qué hace?** Activa el entorno virtual para usarlo.

---

## macOS (Homebrew)

### 1. Instalar Homebrew (si no lo tienes)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
**¿Qué hace?** Instala Homebrew, el gestor de paquetes para macOS.

### 2. Instalar Python 3.10
```bash
brew install python@3.10
```
**¿Qué hace?** Instala Python 3.10 usando Homebrew.

### 3. Verificar instalación
```bash
python3.10 --version
```
**¿Por qué este comando?** Igual que en otros sistemas, confirma que usas la versión correcta.

### 4. Crear entorno virtual
```bash
python3.10 -m venv venv
```
**¿Qué hace?** Crea la carpeta `venv` con el entorno virtual.

### 5. Activar entorno virtual
```bash
source venv/bin/activate
```
**¿Qué hace?** Activa el entorno virtual para trabajar en él.

---

## Nota importante
- Usamos `python3.10 --version` en lugar de `python --version` porque en muchos sistemas hay varias versiones instaladas. Este comando asegura que trabajas con la versión correcta.