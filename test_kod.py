print("Tohle je testovací kód")


def fibonacci(n):
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    else:
        fibo = [0, 1]
        while n >= len(fibo):
            fibo.append(fibo[-1]+fibo[-2])
    return fibo


print(fibonacci(10))

print('Informatika je super')