def isvalid(number):
    sum=sumofevendoublespace(number)+sumofoddplace(number)
    if sum%10==0:
        return True
    else:
        return False

def sumofevendoublespace(number):
    step1_sum=0
    number=str(number)
    number_list1=list()
    for i in range(len(number)-1,-1,-1):
        if i%2==0:
            number_list1.append(number[i])
    for i in number_list1:
        m=getdigit(int(i)*2)
        step1_sum+=m
    return step1_sum

def getdigit(number):
    sum=0
    for i in str(number):
        sum+=int(i)
    return sum

def sumofoddplace(number):
    step2_sum=0
    number=str(number)
    number_list2=list()
    for i in range(len(number)-1,-1,-1):
        if i%2==1:
            number_list2.append(number[i])
    for i in number_list2:
        step2_sum+=int(i)
    return step2_sum
number=int(input('please enter your credit card numbers:'))
print(isvalid(number))

    


    