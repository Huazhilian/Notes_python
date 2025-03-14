def lowertocapital(lower):
    b=''
    for letter in lower:
        if ord(letter) >= 97 and ord(letter) <= 122:
            b=b+(chr(ord(letter)-32))
        else:
            b=b+letter
    return b
        
string='word 123'
print(lowertocapital(string))  # ASCII conversion