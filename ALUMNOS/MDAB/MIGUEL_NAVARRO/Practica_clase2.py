# CLASE 2
# 27/07/2025

# print("EJERCICIO 1:") # Imprime cada número de la lista multiplicado por el número
# num = 7
# listnum = [1, 2, 3, 4]
# for contador in listnum:
#     print(contador*num)


# print("EJERCICIO 2:") # Imprime cada número del -10 al -1 con range
# rane2 = range(-10, 0, 1)
# for contador in rane2:
#     print(contador)


# print("EJERCICIO 3:") # Imprime todos los números divisibles por 5 y por 7, dentro del rango (150, 350)
# rane3 = range(150,351)
# for contador in rane3:
#     if contador % 5 == 0 and contador % 7 == 0:
#         print(contador)


# print("EJERCICIO 4:") # Imprime un patrón de números por pantalla
# rane4 = range(5, 0, -1)
# for x in rane4: # "x" va a ser el mayor número del rango
#     for y in range(x, 0, -1): # "y" es cada número (desde el mayor "x" hasta el último , 0)
#         print(y, end=" ") # separa cada valor de "y" con un espacio
#     print() # salto de línea cuando X cambia


# print("EJERCICIO 5:") # Cuenta cuántos nºs especiales (múltiplo de 3 o contiene el dígito "3") hay en una lista
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


# print("EJERCICIO 7:")
# string = "Ole Python como mola! Me está encantando. De verdad que SÍ"
# cont_mayus = 0
# cont_minus = 0
# cont_dig = 0
# for caracter in string:
#     if caracter.isupper():
#         cont_mayus += 1
# for caracter in string:
#     if caracter.islower():
#         cont_minus += 1
# for caracter in string:
#     if caracter.isdigit():
#         cont_dig += 1
# print(f"En la string '{string}'")
# print(f"Hay {cont_mayus} letras en mayúscula, {cont_minus} letras en minúscula y {cont_dig} dígitos en total")


# print("EJERCICIO 8:")
# dias_semana: dict = {
#     1: "lunes",
#     2: "martes",
#     3: "miércoles",
#     4: "jueves",
#     5: "viernes",
#     6: "sábado",
#     7: "domingo"
# }
# def semanal_1(dia):
#     print(dias_semana[dia])
# semanal_1(5)
# def semanal_2(dia):
#     match dia:
#         case 1:
#             print("lunes")
#         case 2:
#             print("martes")
#         case 3:
#             print("miércoles")
#         case 4:
#             print("jueves")
#         case 5:
#             print("viernes")
#         case 6:
#             print("sábado")
#         case 7:
#             print("domingo")
#         case _:
#             print("Error")
# semanal_2(6)


