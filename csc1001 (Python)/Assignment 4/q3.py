class listStack:
    def __init__(self):
        self.__data=list()
    
    def __len__(self):
        return len(self.__data)

    def is_empty(self):
        return len(self.__data)==0
    
    def push(self,e):
        self.__data.append(e)

    def top(self):
        if self.is_empty:
            print('The stack is empty.')
        else:
            return self.__data[self.__len__()-1]
    
    def pop(self):
        if self.is_empty():
            print('The stack is empty.')
        else:
            return self.__data.pop()

def Alphabet_forward(n):
    Alphabet_list=list(n)
    new_list=list()
    for i in Alphabet_list:
        if i=='A':
            i='B'
        elif i=='B':
            i='C'
        elif i=='C':
            i='A'
        new_list.append(i)
    new_string=''.join(new_list)
    return new_string

def Alphabet_back(n):
    Alphabet_list=list(n)
    new_list=list()
    for i in Alphabet_list:
        if i=='A':
            i='C'
        elif i=='B':
            i='A'
        elif i=='C':
            i='B'
        new_list.append(i)
    new_string=''.join(new_list)
    return new_string

def HanoiTower(n):
    Situation_Stack=listStack()
    step_list=list()
    Situation_Stack.push(step_list)
    for i in range(n):
        step_list=Situation_Stack.pop()
        if  i%2==0:
            new_step_list=list()
            for j in step_list:
                new_step_list.append(Alphabet_back(j))
            step_list.append('A-->B')
            step_list+=new_step_list
        else:
            new_step_list=list()
            for j in step_list:
                new_step_list.append(Alphabet_forward(j))
            step_list.append('A-->C')
            step_list+=new_step_list
        Situation_Stack.push(step_list)
    for i in step_list:
        print(i)

HanoiTower(3)
