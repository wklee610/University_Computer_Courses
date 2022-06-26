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

class LinkedQueue:
    def __init__(self):
        self.head=None
        self.tail=None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size==0

    def first(self):
        if self.is_empty():
            print('Queue is empty.')
        else:
            return self.head.element
    
    def dequeue(self):
        if self.is_empty():
            print('Queue is empty.')
        else:
            answer=self.head.element
            self.head=self.head.pointer
            self.size-=1
            if self.is_empty():
                self.tail=None
            return answer

    def enqueue(self,e):
        newest=Node(e,None)
        if self.is_empty():
            self.head=newest
        else:
            self.tail.pointer=newest
        self.tail=newest
        self.size+=1

def linkedBubble(q):
    listLength=q.size
    while listLength>0:
        index=0
        pointer=q.head
        while index<listLength-1:
            if pointer.element>pointer.pointer.element:
                buf=pointer.element
                pointer.element=pointer.pointer.element
                pointer.pointer.element=buf
            index+=1
            pointer=pointer.pointer
        listLength-=1
    return q

def outputQ(q):
    pointer=q.head
    while pointer:
        print(pointer.element)
        pointer=pointer.pointer
