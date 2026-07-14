def add(a: int, b:int) -> int:
    print(f"adding: {a} + {b}")
    return a + b

FCN = {
    "add": add
}

def main():
    total = FCN.get("add")(1, 1)
    print(f"total: {total}")

if __name__ == "__main__":
    main()