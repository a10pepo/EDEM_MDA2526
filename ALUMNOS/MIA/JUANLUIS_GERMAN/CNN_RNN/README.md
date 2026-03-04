
---

# 🚗 Clasificación de Tráfico en Autopistas: Enfoque CNN-RNN

Clasificación de densidad de tráfico (*Ligero/Medio/Pesado*) en secuencias de vídeo mediante arquitectura híbrida CNN-RNN.

## ⚙️ Contexto sobre los datos

* **Fuente:** [Highway Traffic Videos Dataset](https://www.kaggle.com/datasets/aryashah2k/highway-traffic-videos-dataset).
* **Entrada:** secuencias de **15 fotogramas** equiespaciados (224 x 224px).
* **Partición:** estratificada 70/15/15 (163 / 35 / 36 vídeos).

## 🧠 Arquitectura final (iteración nº8)

Aproximación basada en incrementación gradual en la complejidad del diseño de la red:

1. **Encoder** `MobileNetV2` (Pesos ImageNet, **Congelados**).
   * *Decisión:* MobileNetV3 no convergió durante el entrenamiento (val_accuracy ~14% tras varias épocas). ResNet50 y EfficientNetV2 resultaron inviables por coste computacional (hasta 10x más tiempo por época). El fine-tuning degradó el rendimiento (val_accuracy 34% en época 1 vs. 85% sin fine-tuning).

2. **Wrapper:** `ManualTimeDistributedCNN`.
   * *Implementación:* Capa personalizada para resolver incompatibilidad de serialización `TimeDistributed` en entornos TF/Windows/GPU.

3. **Decoder:** `GRU Bidireccional` (64 unidades).
   * *Decisión:* GRU frente a LSTM por eficiencia computacional equivalente con menor número de parámetros. Bidireccionalidad para capturar el contexto global del flujo vehicular.

4. **Regularización:** `Dropout (0.5)`.
   * *Efecto:* Redujo el sobreajuste observado en las iteraciones con LSTM unidireccional.

## 📉 Resultados (test set)

El entrenamiento finalizó por *early stopping* con una **loss de validación de 0.09**.

| Clase | Precisión | Recall | F1-Score | Soporte |
| --- | --- | --- | --- | --- |
| **Light** | 1.00 | 1.00 | 1.00 | 25 |
| **Medium** | 0.60 | 0.60 | 0.60 | 5 |
| **Heavy** | 0.67 | 0.67 | 0.67 | 6 |
| **Accuracy global** | | | **0.89** | 36 |

> ⚠️ El soporte de las clases Medium (5) y Heavy (6) en el test set es muy reducido. Las métricas de estas clases deben interpretarse con cautela.

## 💡 Conclusión Principal

La combinación **MobileNetV2 + Bi-GRU** demostró ser la mejor opción para este dataset limitado. Una arquitectura ligera bien regularizada supera a alternativas más pesadas (ResNet50, EfficientNetV2) en este contexto, donde el coste computacional y el riesgo de sobreajuste pesan más que la capacidad bruta del encoder.

## 🔭 Líneas futuras

El principal cuello de botella es el reducido soporte de las clases Medium y Heavy; ampliar el dataset o aplicar *data augmentation* temporal, podría mejorar la robustez del modelo en estas fronteras de decisión. Como línea de investigación, cabría comparar el Bi-GRU contra un Transformer encoder pre-entrenado en vídeo, que modela dependencias temporales globales, aunque solo estaría justificado decantarse por esta última si los resultados superan a la solución actual.
