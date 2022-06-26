def superfloat(n):
    if n%1==0:
        return int(n)
    else:
        return float(n)

import string

class polynomial():
    def __init__(self,expression='x^2'):
        self.expression=expression
    
    def new_expression(self):
        new_expression=input('Please enter a polynomial:')
        self.expression=new_expression
    
    def derivation(self):
        begin=0
        alphabet=string.ascii_lowercase+string.ascii_uppercase
        item_list=list()
        self.expression+='+'
        variable='x'
        for i in self.expression:
            if i in alphabet:
                variable=i
        if self.expression.startswith('+') or self.expression.startswith('-'):
            re=self.expression[0]
            self.expression=self.expression[1:]
        else:
            re='+'
        for i in self.expression:
            if i=='+' or i=='-':
                item_list.append(self.expression[begin:self.expression.index(i,begin+1)])
                begin=self.expression.index(i,begin+1)
        item_list[0]=re+item_list[0]
        for i in item_list:
            if i.count(variable)>1:
                list1=list(i)
                sum=0
                while '*' in list1[list1.index(variable):] and list1.count(variable)>1:
                    if list1[list1.index(variable)+1]=='^':
                        a=float(''.join(list1[list1.index(variable)+2:list1.index('*',list1.index(variable))]))
                        a=superfloat(a)
                        del list1[list1.index(variable):list1.index('*',list1.index(variable))+1]
                    else:
                        a=1
                        del list1[list1.index(variable):list1.index('*',list1.index(variable))+1]
                    sum=sum+a
                if list1.count(variable)==1 and (not '*' in list1[list1.index(variable):]):
                    if list1[list1.index(variable)+1]=='^':
                        a=float(''.join(list1[list1.index(variable)+2:]))
                        a=superfloat(a)
                        del list1[list1.index(variable):]
                    else:
                        a=1
                        del list1[list1.index(variable):]
                    sum=sum+a
                    list1.append(variable+'^'+str(sum))
                if list1.count(variable)==1 and '*' in list1[list1.index(variable):]:
                    if list1[list1.index(variable)+1]=='^':
                        a=float(''.join(list1[list1.index(variable)+2:list1.index('*',list1.index(variable))]))
                        a=superfloat(a)
                        del list1[list1.index(variable):list1.index('*',list1.index(variable))+1]
                    else:
                        a=1
                        del list1[list1.index(variable):list1.index('*',list1.index(variable))+1]
                    sum=sum+a
                    list1.append('*'+variable+'^'+str(sum))
                item_list[item_list.index(i)]=''.join(list1)
        for i in item_list:
            if not variable in i:
                item_list.remove(i)
        for i in item_list:
            tem_list=i.split('*')
            final_list=list()
            final_list.append(i[0])
            for j in tem_list:
                if j.startswith('+') or j.startswith('-'):
                    tem_list[tem_list.index(j)]=j[1:]
            for j in tem_list:
                if not variable in j:
                    final_list.append(j)
            for j in tem_list:
                if '^' in j and variable in j:
                    a=j.index('^')
                    b=float(j[a+1:])
                    b=superfloat(b)
                    c=b-1
                    if c==1:
                        j=str(b)+'*'+j[a-1]
                    elif c>1:
                        j=str(b)+'*'+j[a-1]+'^'+str(c)
                    final_list.append(j)
                if not '^' in j and variable in j:
                    j='1'
                    final_list.append(j)                   
            item_list[item_list.index(i)]='*'.join(final_list)
        for k in item_list:
            new_list=list(k)
            del new_list[1]
            item_list[item_list.index(k)]=''.join(new_list)
        for i in item_list:
            if i.count(variable)>0:
                item_list[item_list.index(i)]=i[0]+str(eval(i[1:i.index(variable)-1]))+i[i.index(variable)-1:]
        for i in item_list:
            if i[len(i)-2:len(i)]=='*1':
                item_list[item_list.index(i)]=i[:-2]
        for i in item_list:
            if not variable in i:
                item_list[item_list.index(i)]=i[0]+str(eval(i[1:]))
        final_item_list=list()
        final_item_list.append(0)
        for i in item_list:
            if variable in i:
                if not i[i.index(variable):] in final_item_list:
                    final_item_list.append(i[i.index(variable):])
            if not variable in i:
                if i.startswith('-'):
                    final_item_list[0]-=superfloat(float(i[1:]))
                else:
                    final_item_list[0]+=superfloat(float(i[1:]))
        if final_item_list[0]==0:
            del final_item_list[0]
        else:
            final_item_list[0]=str(final_item_list[0])
        for i in final_item_list:
            sum=0
            if '^' in i and variable in i:
                for j in item_list:
                    if i in j:
                        if j[0]=='-':
                            if j[1]==variable:
                                sum=sum-1
                            else:
                                sum=sum-float(j[1:j.index('*')])
                        if j[0]=='+':
                            if j[1]==variable:
                                sum=sum+1
                            else:
                                sum=sum+float(j[1:j.index('*')])
            if not '^' in i and variable in i:
                for j in item_list:
                    if not '^' in j and variable in j:
                        if j[0]=='-':
                            if j[1]==variable:
                                sum=sum-1
                            else:
                                sum=sum-float(j[1:j.index('*')])
                        if j[0]=='+':
                            if j[1]==variable:
                                sum=sum+1
                            else:
                                sum=sum+float(j[1:j.index('*')])
            sum=str(superfloat(sum))
            if not (sum.startswith('+') or sum.startswith('-')):
                sum='+'+sum
            if not (final_item_list.index(i)==0 and not variable in i):
                final_item_list[final_item_list.index(i)]=sum+'*'+final_item_list[final_item_list.index(i)]            
        if len(item_list)==0:
            derivation='0'
        else:
            derivation=''.join(final_item_list)
        if derivation.startswith('+'):
            derivation=derivation[1:]
        print(derivation)

def main():
    a=polynomial()
    a.new_expression()
    a.derivation()

main()