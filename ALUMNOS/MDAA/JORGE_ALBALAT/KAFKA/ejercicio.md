El caso de uso seleccionado es el de una empresa de delivery como podria ser UberEats.
Primero creo los datos y la distancia a cada cliente desde el restaurante, envío los datos a un consumer que con una velocidad establecida del repartidor calcula el tiempo de llegada del pedido, estos datos los uso en ksql para poder filtrar los que van a tardar mucho y esto lo recibe un consumer que saca la alerta.


Mi JSON de ejemplo es :
{"pedido_id": "0", "restaurante": "SushiTime", "cliente": "Maria", "distancia": "15"}