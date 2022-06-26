numberdict=dict()
for i in range(1,101):
    numberdict[str(i)]='close'
n=1
while n<=100:
    for i in range(1,101):
        if i%n==0:
            if numberdict[str(i)]=='close':
                numberdict[str(i)]='open'
            elif numberdict[str(i)]=='open':
                numberdict[str(i)]='close'
    n=n+1
for key,value in numberdict.items():
    if value=='open':
        print('L',key,' ',value,sep='')
