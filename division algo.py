import math

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check divisibility up to √n
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

# --- Main Program ---
num = int(input("Enter a number to test for primality: "))

if is_prime(num):
    print(f"{num} is a Prime number.")
else:
    print(f"{num} is NOT a Prime number.")
