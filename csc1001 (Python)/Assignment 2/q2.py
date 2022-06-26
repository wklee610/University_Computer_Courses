def check_prime(n):
    numberlist=list()
    for i in range(1,n+1):
        if n%i==0:
            numberlist.append(i)
    if len(numberlist)==2:
        return True
    else:
        return False
prime_list=list()
for i in range(1,10000000):
    m=str(i)
    m=m[::-1]
    m=int(m)
    if check_prime(i) and check_prime(m):
        prime_list.append(i)
    if len(prime_list)==100:
        break
count=0
for a in prime_list:
    print(a, end=' ')
    count=count+1
    if count %10==0:
        print()

