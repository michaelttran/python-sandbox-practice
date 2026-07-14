def factorial(num: int):
    if num == 0:
        return 1
    
    return num * factorial(num - 1)

def sum_list(l: list):
    if not l:
        return 0
    print(f"l: {l[1:]}")
    
    return l[0] + sum_list(l[1:])

def main():
    # f = factorial(3)
    # print(f"factorial: {f}")
    
    l = [1, 2, 3]
    s_list = sum_list(l)
    print(f"s_list: {s_list}")

if __name__ == "__main__":
    main()