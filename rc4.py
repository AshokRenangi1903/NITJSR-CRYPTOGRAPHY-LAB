def rc4(key, data):
    # Key Scheduling Algorithm (KSA)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-Random Generation Algorithm (PRGA)
    i = j = 0
    out = []
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(char ^ K)
    return bytes(out)


# -------- Main Program --------
key_input = input("Enter key: ").encode()         # user enters key as string
plaintext_input = input("Enter plaintext: ").encode()

ciphertext = rc4(key_input, plaintext_input)
print("\nCiphertext (hex):", ciphertext.hex())

decrypted = rc4(key_input, ciphertext)  # decrypt (same function)
print("Decrypted text:", decrypted.decode())
