class flower():
    def __init__(self,name='tulip',petals=int(6),price=float(10)):
        self.name=name
        self.petals=petals
        self.price=price

    def update_name(self):
        new_name=input('What is the name of the flower?:')
        self.name=new_name
    
    def  update_petals(self):
        while True:
            new_petals=input('How many petals does it have?:')
            if new_petals.isdigit():
                self.petals=int(new_petals)
                break
            else:
                print('Please enter the correct information')
    
    def update_price(self):
        while True:
            new_price=input('How much is it?:')
            try:
                self.price=float(new_price)
                break
            except:
                print('Please enter the correct information')
        
def main():
    new_flower=flower()
    new_flower.update_name()
    new_flower.update_petals()
    new_flower.update_price()
    print('\tname','\tpetals','\tprice')
    print('\t',new_flower.name,'\t',new_flower.petals,'\t',new_flower.price,sep='')

main()
