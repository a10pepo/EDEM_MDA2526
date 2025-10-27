#Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.

def ultimoCaracter(cadena: str):
    if type(cadena) == str:
        return cadena[-1]
    
#Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'

    else:
        return "Debo ser ejecutada con un string"


print(ultimoCaracter("Flor"))
print(ultimoCaracter(100))  