def ultimoCaracter(frase):

    if frase.isnumeric():
        return 'Debo ser ejecutada con un string'

    return frase[-1]
    
    

entrada = input("Introduce una frase y te devolverá el último carácter: ")
resultado = ultimoCaracter(entrada)
print("Resultado: ", resultado)