taller de coches

En un taller de coches, los clientes llevan su coche y un primer mecánico que solo se dedica a hacer diagnósticos, averigua que le ocurre al coche. Existen 2 posibles casos: Si no se puede arreglar, el diagnosticador, avisa a administración para que envie un mensaje al cliente. Si se puede arreglar el diagnosticador avisa al taller. El taller tiene dos opciones: si tienen las piezas avisa al mecánico para que lo repare. Una vez reparado, avisa a administración para que notifique al cliente de que su coche ya está listo. Si no tienen las piezas avisan al proveedor. Cuando el proveedor tiene todas las piezas, notifica al almacén para que ponga en marcha el mismo proceso descrito anteriormente.

Diseño de kafka propuesto

- Un consumer cliente que lee cuando su coche está listo (En la realidad podría ser una API que enviara los mensajes a los telefonos, de momento solo será un consumer básico que imprime la matricula del coche)
- Un producer diagnosticador que produce encargos de reparación o avisa a administración de que la reparación no es posible.
- Un consumer/producer taller que consume encargos de reparación y avisos de piezas suministradas y produce encargos de piezas y avisos de reparación finalizada.
- Un consumer/producer proveedor que consume encargos de piezas y envias cuando estan listas 
- Un consumer/producer administración que consume avisos de reparación finalizada y produce notificaciones al cliente. 


- Un topic "encargos_coches" con un filtro de ksql que envie al topic "encargos finalizados" en caso de no poder arreglarlo. Produce el diagnosticador y consume el taller
- Un topic "encargos_piezas". Producen y consumen el taller y el proveedor
- Un topic "encargos_finalizados". Produce taller y diagnosticador a través del filtro de ksql y consume administracíon
- Un topic "avisos_cliente". Produce administración y consume cliente