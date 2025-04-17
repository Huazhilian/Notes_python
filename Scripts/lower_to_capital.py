def lowertocapital(lower):
    b=''
    for letter in lower:
        if ord(letter) >= 97 and ord(letter) <= 122:
            b=b+(chr(ord(letter)-32))
        else:
            b=b+letter
    return b
        
if __name__ == '__main__': # only run if this is the main module
    print(lowertocapital('word 12345'))  # ASCII conversion