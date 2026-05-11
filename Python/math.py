def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


def floor_divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a // b


def sqrt(a):
    if a < 0:
        raise ValueError("square root of negative number")
    return a ** 0.5


def power(a, b):
    return a ** b


def modulo(a, b):
    if b == 0:
        raise ZeroDivisionError("modulo by zero")
    return a % b


def average(a, b):
    return (a + b) / 2


def square(a):
    return a ** 2


def cube(a):
    return a ** 3


def percentage(a, b):
    if b == 0:
        raise ZeroDivisionError("percentage of zero")
    return (a / b) * 100


def isEven(a):
    return a % 2 == 0


def findEvens(start, end):
    return [num for num in range(start, end + 1) if num % 2 == 0]


def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def findPrimes(start, end):
    return [num for num in range(start, end + 1) if isPrime(num)]


def factorial(n):
    if n < 0:
        raise ValueError("factorial of negative number")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n):
    if n <= 0:
        raise ValueError("Fibonacci of non-positive number")
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]
