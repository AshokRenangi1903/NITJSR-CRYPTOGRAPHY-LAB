
from typing import Optional

# ---------- Try PyCryptodome implementation ----------
try:
    from Crypto.Cipher import DES3
    from Crypto.Util.Padding import pad, unpad

    def _join_keys(k1: bytes, k2: bytes, k3: Optional[bytes]) -> bytes:
        if k3 is None:
            # two-key 3DES key is K1 || K2 (16 bytes) and libraries treat it as 2-key TDES
            return k1 + k2
        else:
            return k1 + k2 + k3

    def triple_des_encrypt_ecb(data: bytes, k1: bytes, k2: bytes, k3: Optional[bytes] = None) -> bytes:
        key = _join_keys(k1, k2, k3)
        cipher = DES3.new(key, DES3.MODE_ECB)
        return cipher.encrypt(pad(data, 8))

    def triple_des_decrypt_ecb(ciphertext: bytes, k1: bytes, k2: bytes, k3: Optional[bytes] = None) -> bytes:
        key = _join_keys(k1, k2, k3)
        cipher = DES3.new(key, DES3.MODE_ECB)
        return unpad(cipher.decrypt(ciphertext), 8)

    def triple_des_encrypt_cbc(data: bytes, k1: bytes, k2: bytes, k3: Optional[bytes], iv: bytes) -> bytes:
        """3DES-CBC encrypt with IV (8 bytes)."""
        key = _join_keys(k1, k2, k3)
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        return cipher.encrypt(pad(data, 8))

    def triple_des_decrypt_cbc(ciphertext: bytes, k1: bytes, k2: bytes, k3: Optional[bytes], iv: bytes) -> bytes:
        key = _join_keys(k1, k2, k3)
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), 8)

    _backend = "pycryptodome"

except Exception:
    try:
        # check that des_encrypt_ecb / des_decrypt_ecb exist in globals()
        des_encrypt_ecb  # type: ignore
        des_decrypt_ecb  # type: ignore
    except NameError:
        raise ImportError(
            "PyCryptodome not found and DES helper functions not present. "
            "Install pycryptodome (pip install pycryptodome) or provide des_encrypt_ecb/des_decrypt_ecb."
        )

    def triple_des_encrypt_ecb(data: bytes, k1: bytes, k2: bytes, k3: Optional[bytes] = None) -> bytes:
        """EDE: C = E_k3(D_k2(E_k1(P))) using provided des_encrypt_ecb/des_decrypt_ecb functions.
           Note: des_encrypt_ecb/des_decrypt_ecb handle padding for full message blocks.
        """
        if k3 is None:
            k3 = k1
        # Step 1: E_k1
        step1 = des_encrypt_ecb(data, k1)
        # Step 2: D_k2
        step2 = des_decrypt_ecb(step1, k2)
        # Step 3: E_k3
        step3 = des_encrypt_ecb(step2, k3)
        return step3

    def triple_des_decrypt_ecb(ciphertext: bytes, k1: bytes, k2: bytes, k3: Optional[bytes] = None) -> bytes:
        if k3 is None:
            k3 = k1
        # inverse of E_k3(D_k2(E_k1(P))) is D_k1(E_k2(D_k3(C)))
        step1 = des_decrypt_ecb(ciphertext, k3)
        step2 = des_encrypt_ecb(step1, k2)
        step3 = des_decrypt_ecb(step2, k1)
        return step3

    # CBC mode fallback using ECB-block operations; we must manage IV and CBC chaining ourselves.
    def _xor_bytes(a: bytes, b: bytes) -> bytes:
        return bytes(x ^ y for x, y in zip(a, b))

    def triple_des_encrypt_cbc(data: bytes, k1: bytes, k2: bytes, k3: Optional[bytes], iv: bytes) -> bytes:
        if k3 is None:
            k3 = k1
        # PKCS#5 padding
        pad_len = 8 - (len(data) % 8)
        data_padded = data + bytes([pad_len])*pad_len
        out = bytearray()
        prev = iv
        for i in range(0, len(data_padded), 8):
            block = data_padded[i:i+8]
            block_xor = _xor_bytes(block, prev)
            enc = triple_des_encrypt_ecb(block_xor, k1, k2, k3) 
            out.extend(enc)
            prev = enc
        return bytes(out)

    def triple_des_decrypt_cbc(ciphertext: bytes, k1: bytes, k2: bytes, k3: Optional[bytes], iv: bytes) -> bytes:
        if k3 is None:
            k3 = k1
        out = bytearray()
        prev = iv
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            dec = triple_des_decrypt_ecb(block, k1, k2, k3)
            plain_block = _xor_bytes(dec, prev)
            out.extend(plain_block)
            prev = block
        # unpad PKCS#5
        pad_len = out[-1]
        return bytes(out[:-pad_len])

    _backend = "fallback_DES_wrappers"

# ------------- Example usage -------------
if __name__ == "__main__":
    print("3DES backend:", _backend)
    # sample 8-byte keys (DES keys must be 8 bytes each)
    K1 = b"8bytekey"
    K2 = b"secondk!"
    K3 = b"thirdkey"

    plaintext = b"The quick brown fox jumps over the lazy dog"
    print("Plaintext:", plaintext)

    # ECB example
    c = triple_des_encrypt_ecb(plaintext, K1, K2, K3)   # pass K3=None for 2-key 3DES
    print("Cipher (hex):", c.hex())

    p = triple_des_decrypt_ecb(c, K1, K2, K3)
    print("Recovered (ECB):", p)

    # CBC example (if using pycryptodome backend or correct block-level fallback)
    iv = b"\x00\x01\x02\x03\x04\x05\x06\x07"
    try:
        c_cbc = triple_des_encrypt_cbc(plaintext, K1, K2, K3, iv)
        p_cbc = triple_des_decrypt_cbc(c_cbc, K1, K2, K3, iv)
        print("Recovered (CBC):", p_cbc)
    except Exception as e:
        print("CBC example skipped due to:", e)
