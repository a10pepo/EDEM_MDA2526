import sys
file = sys.argv[1]
list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']
def ahorcado() :
    total = 0
    with open(file, "r") as archivo :
        for linea in archivo:
            line = linea.strip().lower()
            count = len(line)
            print(count)
            for letra in list:
                if letra in line: 
                    count = count - line.count(letra)
                    print(count)
                total = total +1
                if count == 0 : break
    print(total)
ahorcado()