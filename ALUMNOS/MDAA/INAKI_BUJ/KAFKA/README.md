# 🚀 Sistema de Detección de Fraude Financiero con Kafka y KSQL

## 1. Definición del Caso de Uso (Business Target)
El objetivo de este proyecto es monitorizar transacciones bancarias en tiempo real para detectar fraudes.
Se utiliza un dataset de Kaggle (Credit Card Fraud Detection) simulando un flujo continuo de datos.

## 2. Dataset Seleccionado
**Fuente:** [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
**Nota:** Dado que el dataset original tiene campos anonimizados (V1, V2...), he simulado datos de negocio (Cliente, País) en el Productor para enriquecer la demostración.

## 3. Arquitectura Implementada
El flujo de datos ("Pipeline") es el siguiente:
1. **Ingesta:** Lectura del CSV y envío a Kafka (Topic: `raw_transactions`).
2. **Procesamiento:** Script Python que convierte divisa y calcula riesgo.
3. **Filtrado KSQL:** Stream que detecta Riesgo > 50.
4. **Alerta:** Consumidor final que notifica a seguridad.

## 4. Modelos de Datos (JSON)
Ejemplo de transacción enriquecida:
```json
{
  "id": "TXN-100024",
  "cliente": "Carlos",
  "monto_usd": 86.9,
  "riesgo_calculado": 30,
  "pais": "US"
}