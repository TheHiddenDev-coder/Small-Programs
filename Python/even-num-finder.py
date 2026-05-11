def findEvens(start, fin):
    for i in range(start, fin + 1):
        if i % 2 == 0:
            print(i)


def isEven(number):
    if number % 2 == 0:
        print(f"{number} is even")
    else:
        print(f"{number} isn't even")


findEven(0, 10)
isEven(25)
isEven(32)
