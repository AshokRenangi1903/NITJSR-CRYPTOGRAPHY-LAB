def mod_inverse(a, p):
    a = a % p
    if a == 0:
        return None

    old_r, r = p, a
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    if old_r != 1:
        return None 
    else:
        return old_t % p  


a = int(input("Enter number (a): "))
p = int(input("Enter prime modulus (p): "))

inverse = mod_inverse(a, p)

if inverse is None:
    print(f"No inverse exists for {a} modulo {p}")
else:
    print(f"Inverse of {a} mod {p} is: {inverse}")
    print(f"Verification: ({a} * {inverse}) % {p} = {(a * inverse) % p}")
