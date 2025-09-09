def extended_gcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1  # Initial coefficients

    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0, y0  # gcd, x, y

# Example usage
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
gcd, x, y = extended_gcd(a, b)

print(f"GCD of {a} and {b} is {gcd}")
print(f"Coefficients: x = {x}, y = {y}")
print(f"Verification: {a}*({x}) + {b}*({y}) = {a*x + b*y}")
