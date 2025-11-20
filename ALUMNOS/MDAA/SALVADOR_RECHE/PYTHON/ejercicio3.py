def ultimoCaracter(palabra):
    return palabra[-1]

palabra = "Marina de Empresas"

if type(palabra) == str:
    print("El último carácter de la palabra es:", ultimoCaracter(palabra))
else:
    print("Debo ser ejecutada con un string")