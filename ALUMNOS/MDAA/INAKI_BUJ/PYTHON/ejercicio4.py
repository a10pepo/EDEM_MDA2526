def ultimoCaracter(valor):
    if not isinstance(valor,str):
        return 'Debo ser ejecutada con una string'
    if len(valor) == 0:
        return ''
    
    return valor[-1]

## ejemplos de prueba
print(ultimoCaracter("Hola"))
print(ultimoCaracter(123))
print(ultimoCaracter(""))