def cleanbin(num, numbits):
    numstr = str(num).split('0b')[1]
    zfill = ""
    for _ in range(numbits-len(numstr)):
        zfill += '0'
    
    return zfill + numstr

s = ""
for i in range(int("1000000",2)):
    b = cleanbin(bin(i), 6)
    # print(b)
    

    # b[0:3] is A
    # b[3:6] is B

    

    product = int(b[0:3],2) * int(b[3:6],2)
    bin_product = bin(product)

    # print(b, cleanbin(bin_product, 6), "{}*{}={}".format(int(b[0:3],2), int(b[3:6],2), product))
    s = s + b + " " + cleanbin(bin_product, 6) + '\n'
print(s)