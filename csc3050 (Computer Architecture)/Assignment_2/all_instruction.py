reg_dict = {'$zero' : 0
               , '$at' : ''
               , '$v0' : 0
               , '$v1' : ''
               , '$a0' : ''
               , '$a1' : ''
               , '$a2' : ''
               , '$a3' : ''
               , '$t0' : 0
               , '$t1' : ''
               , '$t2' : ''
               , '$t3' : ''
               , '$t4' : ''
               , '$t5' : ''
               , '$t6' : ''
               , '$t7' : ''
               , '$s0' : ''
               , '$s1' : ''
               , '$s2' : ''
               , '$s3' : ''
               , '$s4' : ''
               , '$s5' : ''
               , '$s6' : ''
               , '$s7' : ''
               , '$t8' : ''
               , '$t9' : ''
               , '$k0' : ''
               , '$k1' : ''
               , '$gp' : ''
               , '$sp' : ''
               , '$fp' : ''
               , '$ra' : ''}

ll = list()                 

def twosComplement(i):                                                 
    bc = bin(abs(i))[2:].zfill(32)                                   
    index = bc.rfind('1')                                       
    pc = bc[0: index].replace('1', 'a').replace('0', '1').replace('a', '0')                 
    bc = pc + bc[index:]                    
    return bc       

def sign_change(n):                         
    bc = twosComplement(n)                      
    n = int(bc, 2)                  
    return n                                
                                    
def binary(n):
    try:                      
        if n >= 0:                          
            return bin(n)[2:].zfill(32)                         
        else:                           
            return twosComplement(n)
    except:
        pass                                

def decimal(bc):                    
    if bc[0] == 1:                          
        return int(bc[1: len(bc)], 2)-2**(len(bc)-1)                    
    else:                                           
        return int(bc, 2)                       
    