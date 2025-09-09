def encrypt_affine(text, a, b):
    result = ""
    for ch in text:
        if ch.islower():
            result += chr(((a * (ord(ch) - 97) + b) % 26) + 97)
        elif ch.isupper():
            result += chr(((a * (ord(ch) - 65) + b) % 26) + 65)
        else:
            result += ch
    return result

plain = input("Enter plain text: ")

print("a = multiplicative key (valid values: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)")
a = int(input("Enter key 'a': "))

print("b = additive key (valid values: 0–25)")
b = int(input("Enter key 'b': "))

print("Cipher:", encrypt_affine(plain, a, b))
