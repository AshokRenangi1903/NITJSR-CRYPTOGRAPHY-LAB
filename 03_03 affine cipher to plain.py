def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def decrypt(ciphertext, a, b):
    inv_a = mod_inverse(a, 26)
    if inv_a is None:
        return None
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += chr(((inv_a * ((ord(ch)-65) - b)) % 26) + 65)
        else:
            result += ch
    return result

# --- main ---
ciphertext = input("Enter the ciphertext: ")

print("\nTrying all possible (a, b) key pairs:")
for a in range(1, 26):
    if gcd(a, 26) == 1:  # only valid 'a'
        for b in range(26):
            pt = decrypt(ciphertext, a, b)
            print(f"a={a}, b={b}  -->  Plaintext: {pt}")
