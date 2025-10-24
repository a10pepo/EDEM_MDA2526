def norm(string: str) -> str:
    return string.strip().lower()


bad = set()
with open("bad_words.txt", encoding="utf-8") as file:
    for line in file:
        word = line.strip()
        if word and not word.startswith("#"):
            bad.add(norm(word))



palabra = input("Introduce una palabra: ")

if not palabra or " " in palabra.strip():
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_norm = norm(palabra)
    if palabra_norm in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")