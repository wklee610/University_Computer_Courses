import random

class ecosystem:
    def __init__(self,fish=1,bear=1,river=['N','F','B']):
        self.fish=fish
        self.bear=bear
        self.river=river
    
    def setfish(self):
        while True:
            new_fish=input('How many fishes?:')
            if new_fish.isdigit():
                self.fish=int(new_fish)
                break
            else:
                print('Please enter the correct information')
    
    def setbear(self):
        while True:
            new_bear=input('How many bears?:')
            if new_bear.isdigit():
                self.bear=int(new_bear)
                break
            else:
                print('Please enter the correct information')
    
    def setriver(self):
        while True:
            len_river=input('How long is the river?:')
            if len_river.isdigit() and int(len_river)>=self.bear+self.fish:
                len_river=int(len_river)
                break
            else:
                print('Please enter the correct information')
        self.river=list()
        position_list=list(range(len_river))
        for i in range(len_river):
            self.river.append('N')
        fish_list=random.sample(position_list,self.fish)
        for i in fish_list:
            position_list.remove(i)
            self.river[i]='F'
        bear_list=random.sample(position_list,self.bear)
        for i in bear_list:
            self.river[i]='B'
    
    def simulation(self,n=1):
        while True:
            n=input('How many steps?:')
            if n.isdigit() and int(n)>0:
                n=int(n)
                break
            else:
                print('Please enter the correct information')
        total_count=0
        while total_count<n:
            position_list=list()
            none_list=list()
            move_list=[-1,0,1]
            left_move_list=[0,1]
            right_move_list=[-1,0]
            count=0
            for i in self.river:
                if i=='F' or i=='B':
                    position_list.append(count)
                elif i=='N':
                    none_list.append(count)
                count=count+1        
            for i in position_list:
                if i==0:
                    move=random.sample(left_move_list,1)[0]
                if i==len(self.river)-1:
                    move=random.sample(right_move_list,1)[0]
                else:
                    move=random.sample(move_list,1)[0]
                if self.river[i]=='F' and not move==0:
                    if self.river[i+move]=='N':
                        self.river[i]='N'
                        self.river[i+move]='F'
                    if self.river[i+move]=='B':
                        self.river[i]='N'
                    if self.river[i+move]=='F':
                        if len(none_list)>0:
                            pick=random.sample(none_list,1)[0]
                            self.river[pick]='F'
                            none_list.remove(pick)
                if self.river[i]=='B' and not move==0:
                    if self.river[i+move]=='N' or self.river[i+move]=='F':
                        self.river[i]='N'
                        self.river[i+move]='B'
                    if self.river[i+move]=='B':
                        if len(none_list)>0:
                            pick=random.sample(none_list,1)[0]
                            self.river[pick]='B'
                            none_list.remove(pick)
            total_count=total_count+1
    
a=ecosystem()
a.setfish()
a.setbear()
a.setriver()
print(a.river)
a.simulation()
print(a.river)
        