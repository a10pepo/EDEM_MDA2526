# Monitor de Expediciones de Almacén

## ¿Qué es esto?

Un pequeño sistema que simula y muestra en tiempo real las expediciones (envíos) de un almacén: qué productos se mandan, a qué clientes y en qué cantidades.

Imagina un panel de control que se actualiza solo, mostrando cuántos pedidos ha despachado el almacén hoy, cuáles son los productos más demandados y quiénes son los clientes que más compran.

## ¿Cómo funciona?

El sistema se compone de tres piezas que trabajan juntas:

1. **La base de datos** — Es donde se guarda toda la información: el catálogo de productos, la lista de clientes y el historial de cada expedición (qué se envió, a quién, cuánto y cuándo).

2. **El generador de pedidos** — Un pequeño programa que simula la actividad de un almacén real: cada 10 segundos "crea" una expedición ficticia (elige un producto, un cliente y una cantidad al azar) y la guarda en la base de datos. Así, sin intervención humana, el sistema siempre tiene actividad nueva que mostrar.

3. **El panel web (dashboard)** — Una página visual a la que se accede desde el navegador. Muestra de un vistazo:
   - Cuántas expediciones se han hecho en las últimas 24 horas
   - Cuántas unidades se han enviado en total
   - A cuántos clientes distintos se ha servido
   - Un ranking de los productos más solicitados
   - Un ranking de los clientes con más volumen de compra
   - Un listado con las últimas expediciones realizadas

   La página se refresca sola cada 15 segundos, así que siempre se ve la información más reciente sin tener que recargar nada.

## ¿Dónde vive todo esto?

Todo el sistema está empaquetado con **Docker**, lo que significa que las tres piezas (base de datos, generador y panel web) funcionan de forma aislada y coordinada, sin necesidad de instalar nada más en el ordenador salvo Docker.

Además, existe la posibilidad de llevar la base de datos a **la nube de Amazon (AWS)**, de modo que los datos no se queden solo en un ordenador, sino en un servidor remoto al que se puede acceder desde cualquier lugar — igual que hacen las aplicaciones reales de las empresas. Esa parte se gestiona con una herramienta llamada **Terraform**, que permite crear esa infraestructura en la nube de forma automática y repetible, sin tener que hacer clics manuales en la consola de Amazon.
