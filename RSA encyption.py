
import secrets

# --- Miller-Rabin primality test ---
def is_probable_prime(n, k=40):     
    if n < 2:
        return False
    small_primes = (2,3,5,7,11,13,17,19,23,29)
    for p in small_primes:
        if n % p == 0:
            return n == p
    # write n-1 as d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2 
        s += 1
    def trial(a):
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            return True
        for _ in range(s-1):
            x = (x * x) % n
            if x == n-1:
                return True
        return False
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # in [2, n-2]
        if not trial(a):
            return False
    return True

# --- generate a random prime of bit-length bits ---
def generate_prime(bits):
    if bits < 2:
        raise ValueError("bits must be >= 2")
    while True:
        # ensure highest bit set to get correct bit length, and make odd
        p = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(p):
            return p

# --- extended gcd and modular inverse ---
def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        return None  # inverse doesn't exist
    return x % m

# --- RSA key generation ---
def generate_keypair(bits=1024, e=65537):
    if bits < 16:
        raise ValueError("Use at least 512 bits for real use; small values only for testing")
    half = bits // 2
    while True:
        p = generate_prime(half)
        q = generate_prime(bits - half)
        if p == q:
            continue
        n = p * q
        phi = (p - 1) * (q - 1)
        if egcd(e, phi)[0] == 1:
            d = modinv(e, phi)
            if d is not None:
                return (n, e, d)

# --- Encrypt/Decrypt integer messages ---
def encrypt_int(m, e, n):
    if m < 0 or m >= n:
        raise ValueError("message out of range")
    return pow(m, e, n)

def decrypt_int(c, d, n):
    return pow(c, d, n)

# --- Helpers to encrypt/decrypt text strings ---
def text_to_int(s, encoding='utf-8'):
    b = s.encode(encoding)
    return int.from_bytes(b, byteorder='big')

def int_to_text(i, encoding='utf-8'):
    # compute needed byte-length
    length = (i.bit_length() + 7) // 8
    if length == 0:
        return ""
    return i.to_bytes(length, byteorder='big').decode(encoding, errors='replace')

def encrypt_text(s, e, n):
    m = text_to_int(s)
    if m >= n:
        raise ValueError("message too long for this key; use padding or shorter message")
    return encrypt_int(m, e, n)

def decrypt_text(c, d, n):
    m = decrypt_int(c, d, n)
    return int_to_text(m)

# --- Simple demo ---
if __name__ == "__main__":
    print("Generating 1024-bit RSA keypair (this may take a moment)...")
    n, e, d = generate_keypair(bits=1024)
    print("Public key (n, e):")
    print("n =", n)
    print("e =", e)
    print("\nPrivate exponent d (keep secret):")
    print("d =", d)

    msg = input("Enter plaintext: ")
    print("\nPlaintext:", msg)
    c = encrypt_text(msg, e, n)
    print("Ciphertext (integer):", c)
    pt = decrypt_text(c, d, n)
    print("Decrypted text:", pt)
