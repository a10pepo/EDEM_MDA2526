# Pasos para Subir la Imagen a Docker Hub

### 1. Hacemos log in
docker login
### 2. Verificamos el nombre de la Imagen
docker images
En este caso docker-pysum con el tag latest
### 3. Etiquetamos la imagen
docker tag docker-pysum [usuario]/pysum-mda:latest
### 4. Subimos la Imagen (Push)
docker push [usuario]/pysum-mda:latest
### 5. URL del repo
https://hub.docker.com/r/elmope/pysum-mda           
- Link a la imagen docker generada y subida a Docker Hub!!!
### 6. Comprobación: Usamos la imagen con el comando
docker run elmope/pysum-mda:latest 3 4