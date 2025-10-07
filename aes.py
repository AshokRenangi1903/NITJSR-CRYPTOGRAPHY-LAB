from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Function to encrypt text using AES
def aes_encrypt(plaintext, key):
    key = key.encode()
    data = plaintext.encode()
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return iv, ciphertext

# Function to decrypt text using AES
def aes_decrypt(ciphertext, key, iv):
    key = key.encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

# --- Main Program ---
key = input("Enter AES key (16/24/32 chars): ")
text = input("Enter plaintext to encrypt: ")

# Encrypt
iv, ciphertext = aes_encrypt(text, key)
print("\n--- ENCRYPTION ---")
print("IV (hex):", iv.hex())
print("Ciphertext (hex):", ciphertext.hex())

# Decrypt
decrypted = aes_decrypt(ciphertext, key, iv)
print("\n--- DECRYPTION ---")
print("Decrypted text:", decrypted)
    