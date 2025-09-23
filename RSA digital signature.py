import secrets
import hashlib

# ----------------- Primitives -----------------

def is_probable_prime(n, k=20):
    """Miller-Rabin probabilistic primality test."""
    if n < 2:
        return False
    # small primes quick test
    small_primes = (2,3,5,7,11,13,17,19,23,29)
    for p in small_primes:
        if n % p == 0:
            return n == p
    # write n-1 = d * 2^s
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

def generate_prime(bits):
    """Generate a probable prime of specified bit length."""
    if bits < 2:
        raise ValueError("bits must be >=2")
    while True:
        # ensure top bit set and odd
        p = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(p):
            return p

def egcd(a, b):
    """Extended gcd -> (g, x, y) with a*x + b*y = g = gcd(a,b)"""
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

# ----------------- RSA Key Generation -----------------

def generate_rsa_keypair(bits=1024, e=65537):
    """
    Generate RSA keypair (n, e, d).
    bits = total size of n (so primes will be ~bits/2 each).
    """
    if bits < 16:
        raise ValueError("bits too small for secure usage")
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

# ----------------- Signing & Verification -----------------

def sha256_int(message: bytes) -> int:
    """Return SHA-256 digest as an integer."""
    h = hashlib.sha256(message).digest()
    return int.from_bytes(h, byteorder='big')

def sign_raw(message: bytes, d: int, n: int) -> int:
    """
    Sign message by hashing with SHA-256 and applying raw RSA:
    signature = (Hash(message) as integer) ^ d mod n
    NOTE: raw (no padding) — NOT recommended for real use.
    """
    h_int = sha256_int(message)
    if h_int >= n:
        # In practice hashed value must be encoded/padded to length of modulus.
        raise ValueError("hash integer >= modulus; use larger key or proper padding")
    sig = pow(h_int, d, n)
    return sig

def verify_raw(message: bytes, signature: int, e: int, n: int) -> bool:
    """Verify raw RSA signature against SHA-256 hash."""
    h_int = sha256_int(message)
    m_from_sig = pow(signature, e, n)
    return m_from_sig == h_int

# ----------------- Helpers for display -----------------

def int_to_hex(i: int) -> str:
    return hex(i)[2:]

# ----------------- Demo -----------------

if __name__ == "__main__":
    # generate small key for demonstration (use >=2048 bits for real security)
    print("Generating RSA keypair (this may take a moment)...")
    n, e, d = generate_rsa_keypair(bits=1024)   # change bits as needed
    print("Generated keys:")
    print("n (modulus) bit-length:", n.bit_length())
    print("e (public exponent):", e)
    print()

    message = b"Hello, this is a message to sign."
    print("Message:", message)

    signature = sign_raw(message, d, n)
    print("\nSignature (hex):", int_to_hex(signature))

    ok = verify_raw(message, signature, e, n)
    print("\nVerification OK?", ok)

    # try tampering
    tampered = b"Hello, this is a tampered message."
    print("Verify tampered message:", verify_raw(tampered, signature, e, n))

    # Example of how to transmit: signature as hex, verify on receiver side with public (n,e)
    print("\n--- Example: receiver side ---")
    sig_hex = int_to_hex(signature)
    # receiver converts back:
    sig_int = int(sig_hex, 16)
    print("Receiver verification:", verify_raw(message, sig_int, e, n))

