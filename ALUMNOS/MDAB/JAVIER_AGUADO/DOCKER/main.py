import sys

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            p1 = int(sys.argv[1])
            p2 = int(sys.argv[2])
            print(f"Sum: {p1 + p2}")
        except ValueError:
            print("Error: Los dos parámetros deben ser numéricos.")
            sys.exit(1)
    else:
        print("Error: Debes introducir dos parámetros.")
        sys.exit(1)

        