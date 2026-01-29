# //---------------------SOLUCION Ejercicio 1--------------------//

# nombre = "Marina de Empresas 2025"
# print(len(nombre))
# print(nombre[0])

# //---------------------SOLUCION Ejercicio 1--------------------//

# //---------------------SOLUCION Ejercicio 2--------------------//

# festivo = False
# if festivo == True:
#     print("Hoy es fiesta voy a echarme una siesta!!")
# else:
#     print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

# //---------------------SOLUCION Ejercicio 2--------------------//

# //---------------------SOLUCION Ejercicio 4--------------------//

# def fun_ultimoCaracter(cadena):
#     try:
#         float(cadena)                                          #Detecta una cadena incorrecta tanto si es int como float, porque un int puede convertirse a float
#         return "Debo ser ejecutada con un string" 
#     except:
#         return cadena[-1]

# //---------------------SOLUCION Ejercicio 4--------------------//

# //---------------------SOLUCION Ejercicio 5--------------------//

# def norm(s):

#     s = s.lower()
#     for letra in s:                                                         #Itera para encontrar 1 o varios espacios delante de la palabra
#         if(letra == " "):
#             s = s[1:]                                                       #Se queda con toda la cadena excepto el primer carácter
#         else: break

#     cadena_invertida = s[::-1]                                              #Invierte la cadena. Hola pasaría a ser aloH

#     for letra in cadena_invertida:                                          #Itera para encontrar 1 o varios espacios al final de la palabra
#         if(letra == " "):
#             cadena_invertida = cadena_invertida[1:]
#         else: break

#     s = cadena_invertida[::-1]                                              #Desinvierte la cadena

#     return s

# bad = set()
# with open("bad_words.txt", encoding="utf-8") as f:
#     for line in f:
#         w = line.strip()
#         if w:
#             bad.add(norm(w))

# palabra_introducida = input("Por favor, introduce una sola palabra: ")

# if palabra_introducida == "" or " " in palabra_introducida:                 #Condición si la palabra está vacía o contiene espacios
#     print("Introduce una sola palabra (sin espacios).")

# elif norm(palabra_introducida) in bad:                                      #Condición si la palabra está en bad
#     print("NO CORRECTA")

# else:
#     print("CORRECTA")

# //---------------------SOLUCION Ejercicio 5--------------------//
