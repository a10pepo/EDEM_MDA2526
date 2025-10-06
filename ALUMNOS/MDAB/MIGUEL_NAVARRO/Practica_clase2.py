# CLASE 2
# 27/07/2025

# print("Ejercicio 1:") # Imprime cada número de la lista multiplicado por el número
# num = 7
# listnum = [1, 2, 3, 4]
# for contador in listnum:
#     print(contador*num)


# print("Ejercicio 2:") # Imprime cada número del -10 al -1 con range
# rane2 = range(-10, 0, 1)
# for contador in rane2:
#     print(contador)


# print("Ejercicio 3:") # Imprime todos los números divisibles por 5 y por 7, dentro del rango (150, 350)
# rane3 = range(150,351)
# for contador in rane3:
#     if contador % 5 == 0 and contador % 7 == 0:
#         print(contador)


# print("Ejercicio 4:") # Imprime un patrón de números por pantalla
# rane4 = range(5, 0, -1)
# for x in rane4: # "x" va a ser el mayor número del rango
#     for y in range(x, 0, -1): # "y" es cada número (desde el mayor "x" hasta el último , 0)
#         print(y, end=" ") # separa cada valor de "y" con un espacio
#     print() # salto de línea cuando X cambia


# print("Ejercicio 5:") # Cuenta cuántos nºs especiales (múltiplo de 3 o contiene el dígito "3") hay en una lista
# listanum = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# esp_cont: int = 0 # empiezo con el contador de nºs especiales en 0
# esp_list = []
# for num in listanum:
#     if num % 3 == 0 or "3" in str(num):
#         esp_cont += 1
#         esp_list.append(num)
# print(f"Hay {esp_cont} números especiales en la lista: {esp_list}")


# print("EJERCICIO 6")
# def cuenta_atras(n):
#     while n > 0:
#         if n % 4 == 0:
#             print("Pum!")
#         else:
#             print(n)
#         n -= 1
#     print("¡Despegue!")

# cuenta_atras(12)


print("EJERCICIO 7:")
