import string

# Leo el fichero y lo guardo en words (list)
with open("palabras.txt", 'r') as archive:
    content = archive.read()
    words = content.split()
# Guardo el abecedario en letters (string)
letters = string.ascii_uppercase

total_strikes = 0

for word in words:          # cada palabra
    known_letters = 0
    for letter in letters:  # cada letra
        total_strikes += 1
        if letter in word:  # letra en la palabra
            print(letter, " in ", word)
            known_letters += word.count(letter)
        if known_letters == len(word):
            break
    

print("Total strikes: ", total_strikes)
print(len(letters))




                








# Adivinar primera palabra




