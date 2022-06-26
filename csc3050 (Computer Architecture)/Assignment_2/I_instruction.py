import all_instruction              

decimal = getattr(all_instruction, 'decimal')           
sign_change = getattr(all_instruction, 'sign_change')           
binary = getattr(all_instruction, 'binary')         

def I_main(I_instruction, reg_cd):              
    instruction_name = I_instruction['instruction_name']                    
    func = eval('{}_instruction'.format(instruction_name))                      
    return func(I_instruction, reg_cd)                          

def addi_instruction(I_instruction, reg_cd):                    
    rt = I_instruction['rt']                    
    rs = I_instruction['rs']                        
    immediate = I_instruction['immediate']                          
    reg_cd[rt] = str((reg_cd[rs])) + str((decimal(immediate)))                                        

def addiu_instruction(I_instruction, reg_cd):                   
    rt = I_instruction['rt']                        
    rs = I_instruction['rs']                            
    immediate = I_instruction['immediate']                  
    reg_cd[rt] = reg_cd[rs] + int(immediate, 2)             

def andi_instruction(I_instruction, reg_cd):                        
    B_rt = ''                       
    rt = I_instruction['rt']                            
    rs = I_instruction['rs']                            
    immediate = I_instruction['immediate']                                  
    V_rs = reg_cd[rs]                       
    if V_rs >= 0:                       
        V_rs = bin(V_rs)[2:].zfill(16)                      
    else:                           
        V_rs = all_instruction.twosComplement(V_rs)                         
    for i in range(0, 32):                      
        if int(V_rs[i]) * int(immediate[i]):                            
            B_rt += '1'                     
        else:                           
            B_rt += '0'                         
    reg_cd[rt] = decimal(B_rt)                      

def beq_instruction(I_instruction, reg_cd):                             
    rt = I_instruction['rt']                                
    rs = I_instruction['rs']                                
    immediate = I_instruction['immediate']                      
    if reg_cd[rt] == reg_cd[rs]:                        
        return decimal(immediate)                                   
    else:                   
        pass                            

def bgez_instruction(I_instruction, reg_cd):                        
    rs = I_instruction['rs']                            
    immediate = I_instruction['immediate']                      
    if reg_cd[rs] >= 0:                 
        return decimal(immediate)                           
    else:                           
        pass                        

def bgtz_instruction(I_instruction, reg_cd):                    
    rs = I_instruction['rs']                    
    immediate = I_instruction['immediate']                      
    if reg_cd[rs] > 0:                  
        return decimal(immediate)                   
    else:                                       
        pass                            

def blez_instruction(I_instruction, reg_cd):                        
    rs = I_instruction['rs']                    
    immediate = I_instruction['immediate']                      
    if reg_cd[rs] <= 0:                     
        return decimal(immediate)                       
    else:                               
        pass                                

def bne_instruction(I_instruction, reg_cd):                                                
    rt = I_instruction['rt']                   
    rs = I_instruction['rs']                   
    immediate = I_instruction['immediate']                                      
    if reg_cd[rt] != reg_cd[rs]:                   
        return decimal(immediate)                   
    else:                   
        pass                   
                   
def lb_instruction(I_instruction, reg_cd):                   
    rt = I_instruction['rt']                   
    rs = I_instruction['rs']                   
    reg_cd[rt] = reg_cd[rs]                     
                   
def lbu_instruction(I_instruction, reg_cd):                     
    rt = I_instruction['rt']                    
    rs = I_instruction['rs']                    
    reg_cd[rt] = reg_cd[rs]                                                                         

def lh_instruction(I_instruction, reg_cd):                      
    rt = I_instruction['rt']                                                        
    rs = I_instruction['rs']                        
    reg_cd[rt] = reg_cd[rs]                                                                   

def lhu_instruction(I_instruction, reg_cd):                                                  
    rt = I_instruction['rt']                        
    rs = I_instruction['rs']                                                            
    reg_cd[rt] = reg_cd[rs]                 

def lui_instruction(I_instruction, reg_cd):                                                    
    rt = I_instruction['rt']                                            
    rs = I_instruction['rs']
    reg_cd[rt] = reg_cd[rs]                             

def lw_instruction(I_instruction, reg_cd):                  
    rt = I_instruction['rt']                                                            
    rs = I_instruction['rs']                                                                
    reg_cd[rt] = reg_cd[rs]                     

def ori_instruction(I_instruction, reg_cd):                                                                             
    rt = I_instruction['rt']                                                            
    rs = I_instruction['rs']                                                                
    immediate = I_instruction['immediate'].zfill(32)                                                          
    B_rs = binary(reg_cd[rs])                                                            
    B_rt = ''                                                       
    for i in range(0, 32):                                                      
        if int(B_rs[i]) or int(immediate[i]):                                           
            B_rt += '1'                                             
        else:                                                   
            B_rt += '0'                                     
    reg_cd[rt] = decimal(B_rt)              

def sb_instruction(I_instruction, reg_cd):                                          
    rt = I_instruction['rt']                                                                                                    
    rs = I_instruction['rs']                                                        
    reg_cd[rs] = reg_cd[rt]                                                                 

def slti_instruction(I_instruction, reg_cd):                                                    
    rt = I_instruction['rt']                                                            
    rs = I_instruction['rs']                                    
    immediate = I_instruction['immediate'].zfill(32)                        
    V_rs = reg_cd[rs]           
    immediate_val = decimal(immediate)                      
    if V_rs < immediate_val:                            
        reg_cd[rt] = 1              
    else:                   
        reg_cd[rt] = 0              

def sltiu_instruction(I_instruction, reg_cd):                   
    rt = I_instruction['rt']                    
    rs = I_instruction['rs']                        
    immediate = I_instruction['immediate'].zfill(32)                
    V_rs = reg_cd[rs]                                   
    if V_rs < 0:                        
        V_rs = sign_change(V_rs)                            
    immediate_val = decimal(immediate)              
    if immediate_val < 0:                   
        immediate_val = sign_change(immediate_val)                  
    if V_rs < immediate_val:                                
        reg_cd[rt] = 1                  
    else:                   
        reg_cd[rt] = 0                      

def sh_instruction(I_instruction, reg_cd):                          
    rt = I_instruction['rt']                    
    rs = I_instruction['rs']                
    reg_cd[rs] = reg_cd[rt]                     

def sw_instruction(I_instruction, reg_cd):              
    rt = I_instruction['rt']                            
    rs = I_instruction['rs']                    
    reg_cd[rs] = reg_cd[rt]                         

def xori_instruction(I_instruction, reg_cd):                    
    rt = I_instruction['rt']                            
    rs = I_instruction['rs']                
    immediate = I_instruction['immediate'].zfill(32)                        
    B_rs = binary(reg_cd[rs])                       
    B_rt = ''                   
    for i in range(0, 32):      
        if int(B_rs[i]) == int(immediate[i]):                   
            B_rt += '0'             
        else:                           
            B_rt += '1'                 
    reg_cd[rt] = int(B_rt, 2)                   
    
def lwl_instruction(I_instruction, reg_cd):                     
    rt = I_instruction['rt']                    
    rs = I_instruction['rs']                    
    reg_cd[rt] = reg_cd[rs]                     

def lwr_instruction(I_instruction, reg_cd):             
    rt = I_instruction['rt']                    
    rs = I_instruction['rs']                
    reg_cd[rt] = reg_cd[rs]                     

def swl_instruction(I_instruction, reg_cd):                     
    rt = I_instruction['rt']                    
    rs = I_instruction['rs']                    
    reg_cd[rt] = reg_cd[rs]                 
    
def swr_instruction(I_instruction, reg_cd):                 
    rt = I_instruction['rt']                    
    rs = I_instruction['rs']                        
    reg_cd[rt] = reg_cd[rs]                         