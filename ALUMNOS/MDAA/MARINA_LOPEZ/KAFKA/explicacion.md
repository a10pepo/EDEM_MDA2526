# definición del caso

Negocio:Gestión Inteligente de Pedidos en Restaurante Italiano

Objetivo: Automatizar el flujo de pedidos con alta demanda para que cada equipo de cocineros reciba las comandas correspondientes y detectar clientes VIP en tiempo real para darles prioridad.

Problema de Negocio: Los pedidos llegan mezclados (pizzas y pastas) y los cocineros pierden tiempo filtrando manualmente. Además, no existe un sistema inmediato para alertar a la gerencia sobre clientes VIP en la terraza.

Arquitectura:

Ingesta: Camarero toma nota. El script camarero.py genera los pedidos y los envía al topic pedidos_cocina.

Procesamiento 1 (Python): Jefe de Cocina (alertasJefeCocina.py) separa Pizzas de Pastas y las reenvía a topics específicos (pedidos_pizza y pedidos_pasta).

Procesamiento 2 (KSQL): Detectar pedidos "VIP" dentro de las Pizzas. KSQL escucha el topic pedidos_pizza, filtra en tiempo real aquellos donde tipo_cliente = 'VIP' y escribe el resultado en un nuevo topic pizzas_vip_topic.

Resultado:
 Los cocineros (cocinero_pizza.py) leen de sus colas específicas.
 La gerencia (gerente.py) lee del topic VIP generado por KSQL.
