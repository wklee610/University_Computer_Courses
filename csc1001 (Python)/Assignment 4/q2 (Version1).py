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

def outputQ(q):
    pointer=q.head
    while pointer:
        print(pointer.element)
        pointer=pointer.pointer

def add_Linkedlist(g,h,j):
    new_list=Linkedlist() 
    if isinstance(g,Linkedlist):
            pivot=g.head
            while pivot:
                new_list.add_last(pivot.element)
                pivot=pivot.pointer
    if isinstance(h,Linkedlist):
            pivot=h.head
            while pivot:
                new_list.add_last(pivot.element)
                pivot=pivot.pointer
    if isinstance(j,Linkedlist):
            pivot=j.head
            while pivot:
                new_list.add_last(pivot.element)
                pivot=pivot.pointer
    return new_list    
  
def Linked_Quicksort(n):
    if not (isinstance(n,Linkedlist) or n==None):
        print('Your input is wrong')
    if n.size<=1:
        return n
    if n.size>1:
        small_list=Linkedlist()
        large_list=Linkedlist()
        mid_list=Linkedlist()
        pivot=n.head
        k=n.head.element
        while pivot:
            if pivot.element<k:
                small_list.add_last(pivot.element)
            elif pivot.element>k:
                large_list.add_last(pivot.element)
            elif pivot.element==k:
                mid_list.add_last(pivot.element)
            pivot=pivot.pointer
        small_list=Linked_Quicksort(small_list)
        large_list=Linked_Quicksort(large_list)
        n=add_Linkedlist(small_list,mid_list,large_list)
        return n

a=Linkedlist()
a.add_last(10)
a.add_last(8)
a.add_first(9)
a.add_last(15)
outputQ(Linked_Quicksort(a))
