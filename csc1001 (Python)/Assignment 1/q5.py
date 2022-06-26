# Created on Ha Jun의 iPad.

n = int(input('Enter a number : '))

if n > 0:
    print('The prime numbers smaller than', n, 'include :')
    count = 0
    for i in range (2,n):
        prime = 1
        for j in range (2, i):
            if (i % j == 0):
                prime = 0
        if (prime == 1):
            count = count + 1
            print(i, end = '   ')
            if (count % 8 == 0):
                print()
    print()
else:
    print('invalid ')