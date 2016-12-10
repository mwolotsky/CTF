cipher = "LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ"
text = "SECCON{"
keysize=12

LIST = [[] for i in range(keysize)]
for i in range(len(cipher)):
    LIST[i % keysize].append(cipher[i])
print LIST
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}"
key = "VIGENERECODE"

for i in range(len(text)):
    val = ALPHABET.index(cipher[i]) - ALPHABET.index(text[i]) 
    print ALPHABET[val]
PLAIN = [[] for i in range(keysize)]
for i in range(len(key)):
    for l in LIST[i]:
        val = (ALPHABET.index(l) - ALPHABET.index(key[i])) % len(ALPHABET)
        PLAIN[i].append(ALPHABET[val])
print PLAIN

Ans = []
for i in range(len(cipher)):
    try:
        Ans.append(PLAIN[i%keysize][i/keysize])
    except:
        Ans.append("-")
print "".join(Ans)
