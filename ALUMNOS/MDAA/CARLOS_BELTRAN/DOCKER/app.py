import sys

def main():
    if len(sys.argv) != 3:
        print("Uso: python sum.py <num1> <num2>")
        sys.exit(1)
        
    try:
        numero1 = sys.argv[1]
        numero2 = sys.argv[2]
        
        sum= int(numero1) + int(numero2)
        print(f"Sum: {sum}")
    except Exception:
        print("Error: ambos parámetros deben ser números")



if __name__ == "__main__":
    main()
