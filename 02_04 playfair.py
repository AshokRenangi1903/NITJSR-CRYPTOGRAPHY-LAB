
def generate_matrix(key):
    key = key.upper().replace("J","I")
    matrix = []
    for c in key:
        if c.isalpha() and c not in matrix:
            matrix.append(c)
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in matrix:
            matrix.append(c)
    return [matrix[i:i+5] for i in range(0,25,5)]

def prepare_text(text):
    text = text.upper().replace("J","I")
    text = ''.join([c for c in text if c.isalpha()])
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a==b:
            b='X'
            i+=1
        else:
            i+=2
        result += a+b
    return result

def find_pos(c, matrix):
    for r,row in enumerate(matrix):
        if c in row:
            return r,row.index(c)

def encrypt_pair(a,b,matrix):
    r1,c1 = find_pos(a,matrix)
    r2,c2 = find_pos(b,matrix)
    if r1==r2:
        return matrix[r1][(c1+1)%5]+matrix[r2][(c2+1)%5]
    elif c1==c2:
        return matrix[(r1+1)%5][c1]+matrix[(r2+1)%5][c2]
    else:
        return matrix[r1][c2]+matrix[r2][c1]

def playfair_encrypt(text,key):
    mat = generate_matrix(key)
    text = prepare_text(text)
    cipher = ""
    for i in range(0,len(text),2):
        cipher += encrypt_pair(text[i],text[i+1],mat)
    return cipher


plaintext = input("Enter plaintext: ")
key = input("Enter key: ")

print("Encrypted Text:", playfair_encrypt(plaintext,key))
