def decrypt(ciphertext, key):
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += chr(((ord(ch) - 65 - key) % 26) + 65)
        else:
            result += ch
    return result

# --- main program ---
ciphertext = input("Enter the ciphertext: ")

print("\nTrying all possible keys (0–25):")
for key in range(26):
    plaintext = decrypt(ciphertext, key)
    print(f"Key = {key}  -->  Plaintext: {plaintext}")
