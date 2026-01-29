def norm(s: str) -> str:
    return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = norm(input("Dime una sola palabra: "))



if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios)")
elif norm(palabra) in bad:
    print(f"NO CORRECTA")
else:
    print("CORRECTA")

