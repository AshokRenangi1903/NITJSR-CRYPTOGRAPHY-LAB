def encrypt(text, key):
    result = ""
    for ch in text:
        if ch.islower():
            result += chr(((ord(ch) - 97) * key) % 26 + 97)
        elif ch.isupper():
            result += chr(((ord(ch) - 65) * key) % 26 + 65)
        else:
            result += ch
    return result


plain = input("Enter plain text: ")
key = int(input("Enter key value among valid keys: 1,3,5,7,9,11,15,17,19,21,23,25 :")) 
print("Cipher:", encrypt(plain, key))
