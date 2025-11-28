import sys

def suma(a, b):
    return a + b

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <a> <b>")
        sys.exit(1)

    suma_result = suma(int(sys.argv[1]), int(sys.argv[2]))
    print(f"La suma de {sys.argv[1]} + {sys.argv[2]} es: {suma_result}")

if __name__ == "__main__":
    main()
