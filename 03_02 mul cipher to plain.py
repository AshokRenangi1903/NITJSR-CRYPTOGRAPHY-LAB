def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def decrypt(ciphertext, key):
    inv = mod_inverse(key, 26)
    if inv is None:
        return None
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += chr(((ord(ch) - 65) * inv) % 26 + 65)
        else:
            result += ch
    return result


ciphertext = input("Enter the ciphertext: ")

print("\nTrying all possible multiplicative keys (coprime with 26):")
for key in range(1, 26):
    if gcd(key, 26) == 1:
        pt = decrypt(ciphertext, key)
        print(f"Key = {key}  -->  Plaintext: {pt}")
