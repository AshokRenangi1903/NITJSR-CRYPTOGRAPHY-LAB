def text_to_nums(text):
    return [ord(c.upper()) - 65 for c in text if c.isalpha()]

def nums_to_text(numbers):
    return ''.join(chr(x % 26 + 65) for x in numbers)

# Hill Cipher Encryption
def hill_encrypt(plaintext, key, n):
    nums = text_to_nums(plaintext)

    while len(nums) % n != 0:
        nums.append(ord('X') - 65)

    ciphertext = []
    for i in range(0, len(nums), n):
        block = nums[i:i+n]
        for row in key:
            val = sum(row[j] * block[j] for j in range(n)) % 26
            ciphertext.append(val)

    return nums_to_text(ciphertext)

# --- User Input ---
plaintext = input("Enter plaintext: ")
n = int(input("Enter key matrix size (n for n x n): "))

print(f"Enter {n*n} numbers (0-25) for key matrix row-wise:")
elements = list(map(int, input().split()))
key = [elements[i*n:(i+1)*n] for i in range(n)]

ciphertext = hill_encrypt(plaintext, key, n)
print("Encrypted Text:", ciphertext)
