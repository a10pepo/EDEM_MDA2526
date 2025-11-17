# =============================================
# EJERCICIO: ¿Qué hace encode('utf-8') y cómo se ve en binario?
# =============================================
# Objetivo: Ver cómo un texto (str) se convierte en bytes y luego en bits (0 y 1).
# =============================================

# PASO 1: Texto original con caracteres especiales
mensaje = "Motor está caliente 🔥 a 95°C"
print("Texto original:", mensaje)
print("Tipo:", type(mensaje))  # <class 'str'>

# PASO 2: Convertimos el texto a bytes usando UTF-8
mensaje_bytes = mensaje.encode('utf-8')
print("\nTexto convertido a bytes:", mensaje_bytes)
print("Tipo:", type(mensaje_bytes))  # <class 'bytes'>

# PASO 3: Mostramos los bytes en binario (0 y 1)
print("\nRepresentación en bits (primeros 10 bytes):")
for b in mensaje_bytes[:10]:  # Mostramos solo los primeros 10 para no saturar
    print(f"{b:08b}", end=" ")  # Cada byte en formato binario (8 bits)
print("\n(¡Así se ve en binario!)")

# PASO 4: Decodificamos de nuevo a texto
mensaje_decodificado = mensaje_bytes.decode('utf-8')
print("\nTexto decodificado:", mensaje_decodificado)
print("Tipo:", type(mensaje_decodificado))  # <class 'str'>

# =============================================
# EJERCICIOS PARA PRACTICAR:
# 1. Cambia el mensaje por tu nombre (si tiene acentos) y repite el proceso.
# 2. Añade un emoji diferente y observa cómo se convierte en varios bytes.