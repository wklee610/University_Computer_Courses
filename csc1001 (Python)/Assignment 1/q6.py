# Created on Ha Jun의 iPad.

from math import sin, cos, tan #이렇게 한줄에 적을수 있따 이말임

#function = (b - a) / n * f(a + ((b - a) / n * (i - 1/2)))

def function(a,b,i,n,temp):                 #나중에 다시 쓰기 귀찮아서 처음에 이거 쓴거
    if temp == 1:                           #1이면 sin, 2면 cos, 3부터는 tan
        cal = sin(a + ((b-a)/n * (i - 1/2)))    #계산 하라고하는거임
    elif temp == 2:
        cal = cos(a + ((b-a)/n * (i - 1/2)))
    else:
        cal = tan(a + ((b-a)/n * (i - 1/2)))
    return (b-a)/n * cal                    #위에서 계산 완료한 결과가 나오면 
                                            #리턴해서 다시 밖에꺼 계산
print('Enter trigonometric function (sin, cos, tan) : ')
c = input()                                 #인풋 받고
#and와 or에 대한 개념 숙지해봐, True False True 가 있으면 and를 넣을경우 False/ or 하면 true
while c != 'sin' and c != 'tan' and c != 'cos': #sin아니고, cos아니고, tan아니면
    print('Invalid input!')                     #응아니야
    print('Enter trigonometric function (sin, cos, tan) : ')   #다시 넣으렴 1
    c = input()                                         #다시 넣으렴 2

if c == 'sin':          #sin이면 1
    temp = 1
elif c == 'cos':        #cos이면 2
    temp = 2
else:                   #나머지 = tan = 3 인데 위에 def에 3이상이면 전부 tan으로 받으니까 3
    temp = 3    #이미 위 while문에서 sin,cos,tan 아니면 전부 에러나게 설정해서
                #어쩌피 나머지는 사실 tan밖에 없는거임
while True:       #!!!!중요!!!!! 여기서 사실 나도 애먹음 (밑에 b,n 동일한방법으로 쓴거임 이것만봐)
    print('Enter lower bound a : ') #넣어라 메세지
    a = input()                     #인풋 ㄱ
    try:                            #예외 처리 (이거 안하면 계속 예외 발생해서 딥빡)
        a = int(a)    #인풋된걸 인트형으로 바꿔라 (여기서 소수, 문자는 바로 에러발생해서 except)
        if a > 0:                   #숫자들 중에 a가 만약 0보다 크면                
            a = int(a)              #그냥 그대로 인트형 되게 하셈
        else:
            print('Invalid input!') #0보다 크지않으면 에러 ㄱ
            continue                #continue쓴건 try문 계속 진행해야하니까
        break                       #여기까지 에러가 없으면 while문 깨짐
    except:                         #아니면 다시 while처음으로 ㄱㄱ
        print('Invalid input!')

while True:                         #이하동일
    print('Enter upper bound b : ')
    b = input()
    try:
        b = int(b)
        if b > 0 and a < b:         #a는 b보다 커야합니다를 추가로 붙인거
            b = int(b)
        else:
            print('Invalid input!')
            continue
        break
    except:
        print('Invalid input!')

while True:                         #이하동일
    print('Enter the number of sub-intervals n : ')
    n = input()
    try:
        n = int(n)
        if n > 0:
            n = int(n)
        else:
            print('Invalid input!')
            continue
        break
    except:
        print('Invalid input!')

sum = 0                             #그래서 결과를 제출합니다.
                                    #계산하는거예요
for i in range(1, n+1):             #n+1은 왜인지 당연히 알겠지요?
    sum += function(a,b,i,n,temp)   #위에 함수 정의해놓은거 그대로 가져와서 계산하고 sum에 넣음

print(sum)                          #마지막에 결과 나옴
