#ENTREGABLE CLOUD

Antes de crear ambas instancias:

![alt text](Entregable Cloud/Captura de pantalla 2026-03-12 183649.png)


Creamos las dos instancias, una para orders-pp y otra para delivery app.

![alt text](<Entregable Cloud/Captura de pantalla 2026-03-12 111741.png>)
![Captura](<Entregable Cloud/Captura de pantalla 2026-03-12 112326.png>)

Creamos el dataset

![alt text](<Entregable Cloud/Captura de pantalla 2026-03-12 124500.png>)


Iniciamos el DBT tras haber sincronizado el PostgresDB database:

![alt text](<Entregable Cloud/Captura de pantalla 2026-03-12 220341.png>)

Se realiza el DBT run para delivery:

![alt text](<Entregable Cloud/Captura de pantalla 2026-03-12 234039.png>)

El siguiente paso de DBT run --select analytics para crear las tablas:

![alt text](<Entregable Cloud/Captura de pantalla 2026-03-12 234224.png>)

Después de esto se hace deploy del docker-compose y más adelante abrimos Metabase

![alt text](<Entregable Cloud/Captura de pantalla 2026-03-12 234430.png>)
![alt text](<Entregable Cloud/Captura de pantalla 2026-03-13 001122.png>)
![alt text](<Entregable Cloud/Captura de pantalla 2026-03-13 001158.png>)