a = eval(input('Enter the final account value: '))
b = eval(input('Enter the annual interest rate: '))
c = eval(input('Enter the number of years: ' ))
d = a / (1 + b / 100) ** c

print('The initial value is: ', d)
