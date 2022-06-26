class Node:
    def __init__(self,element,pointer):
        self.element=element
        self.pointer=pointer

class Linkedlist:
    def __init__(self):
        self.head=None
        self.tail=None
        self.size=0
    
    def add_first(self,e):
        newest=Node(e,None)
        newest.pointer=self.head
        self.head=newest
        self.size+=1
        if self.size==1:
            self.tail=newest

    def add_last(self,e):
        newest=Node(e,None)
        if self.size>0:
            self.tail.pointer=newest
        else:
            self.head=newest
        self.tail=newest
        self.size+=1

    def remove_first(self):
        if self.size==0:
            print('The linked list is empty')
        elif self.size==1:
            answer=self.head.element
            self.head.element=None
            self.tail.element=None
            self.size-=1
            return answer
        else:
            answer=self.head.element
            self.head=self.head.pointer
            self.size-=1
            return answer
    
def len_Linkedlist(n):
    if not (isinstance(n,Node) or n==None):
        return 'Your input is wrong'       
    elif n==None:
        return 0
    else:
        try:
            return 1+len_Linkedlist(n.pointer)
        except:
            return 'Your input is wrong'

a=Linkedlist()
a.add_last(10)
a.add_last(8)
a.add_first(9)
a.add_last(15)
c=3
b=Node(7,c)
print(len_Linkedlist(a.head))
print(len_Linkedlist(b))