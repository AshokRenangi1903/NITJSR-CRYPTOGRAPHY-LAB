import random

def is_prime_fermat(n, k=5):
    
    if n <= 1:
        return False
    if n <= 3:
        return True

    # Perform k tests
    for _ in range(k):
        a = random.randint(2, n - 2)  
        if pow(a, n - 1, n) != 1:     
            return False               
    return True                        

# Example usage
num = int(input("Enter a number: "))
if is_prime_fermat(num):
    print(f"{num} is probably prime.")
else:
    print(f"{num} is composite.")
