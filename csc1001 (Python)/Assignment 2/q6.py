import random
def confict(state, position):
    nextX = len(state)
    if position in state: 
        return True
    for i in range(nextX):
        if nextX-position == i-state[i]: 
            return True
        if nextX+position == i+state[i]: 
            return True
    return False
def queens(number, state=()):
    if number-1 == len(state):
        for position in range(number):
            if not confict(state, position):
                yield (position,)
    else:
        for position in range(number):
            if not confict(state, position):
                for result in queens(number, state+(position,)):
                    yield (position,) + result
i=list(queens(8))
i=random.sample(i,1)
j=list(i[0])
print(j)
for k in j:
    count=0
    while count<k:
        print('| ',end='')
        count=count+1
    while count==k:
        print('|Q',end='')
        count=count+1
    while count>k and count<8:
        print('| ',end='')
        count=count+1
    while count==8:
        print('|',end='')
        count=count+1
        print()