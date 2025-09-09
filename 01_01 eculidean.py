def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Example usage
x = int(input("Enter first number: "))
y = int(input("Enter second number: "))
print("GCD of", x, "and", y, "is:", gcd(x, y))
