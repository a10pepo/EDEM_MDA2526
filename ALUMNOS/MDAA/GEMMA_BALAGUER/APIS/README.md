# **ENTREGABLE API: CREA TU PRIMERA API USANDO SWAGGER**

Imagina que trabajas en una empresa industria donde hay un robot. Contamos con un sensor que monitorea la temperatura del robot en tiempo real. Las mediciones se guardan en una base de datos. 

**Información que envía el sensor**

- id del sensor - > string. 

- fecha de muestreo - > string. 

- unidad -> string.

- medición -> number.

**Método que debe seguir la api**

```sh
/getLastMeassureBySensor/{sensor}
```
Donde:

- sensor -> string.

Cuando el método se **ejecuta correctamente**, debe devolver un objeto Measure con los siguientes campos:

- code (id del sensor) –> string.

- fecha de muestreo –> string.

- unidad –> string.

- medición –> number

Cuando el método **no se ejecuta correctamente**, debe devolver:

- 404 -> sensor no encontrado.

- 400 → ID inválido proporcionado.



