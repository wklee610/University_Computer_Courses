N = int(input('Please enter a positive integer : '))
print('\tm','\tm+1','\tm**(m+1)')

M = 1
while (M <= N):
    a = str(M)
    b = str(M+1)
    c = str(M**(M+1))
    print('\t', a ,'\t', b ,'\t', c ,sep='')
    M = M+1
