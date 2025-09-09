def ceaser_encrypt(plaintext, key):
    res = []
    k = key % 26
    for ch in plaintext:
        if 'a' <= ch <= 'z':
            res.append(chr((ord(ch) - 97 + k) % 26 + 97))
        elif 'A' <= ch <= 'Z':
            res.append(chr((ord(ch) - 65 + k) % 26 + 65))
        else:
            res.append(ch)
    return ''.join(res)

def ceaser_decrypt(ciphertext, key):
    return ceaser_encrypt(ciphertext, -key)


text = input("Enter text: ")
key = int(input("Enter key (0-25): "))
c = ceaser_encrypt(text, key)
p = ceaser_decrypt(c, key)
print("Ciphertext:", c)
print("Decrypted :", p)
