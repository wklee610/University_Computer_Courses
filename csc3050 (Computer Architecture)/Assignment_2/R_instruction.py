import all_instruction          
import syscall          

decimal = getattr(all_instruction, 'decimal')               
sign_change = getattr(all_instruction, 'sign_change')       
binary = getattr(all_instruction, 'binary')                 

def R_main(R_instruction, reg_cd):              
    instruction_name = R_instruction['instruction_name']                    
    if instruction_name == 'syscall':           
        syscall.syscall_instruction(reg_cd)             
    else:               
        func = eval('{}_instruction'.format(instruction_name))                      
        return func(R_instruction, reg_cd)                                              

def add_instruction(R_instruction, reg_cd):                                         
    rs = R_instruction['rs']                                    
    rt = R_instruction['rt']                            
    rd = R_instruction['rd']                                    
    temp_List = list()          
    if isinstance(reg_cd[rs], list):                                                                          
        for i in reg_cd[rs]:
            temp_List.append(i + reg_cd[rt])                    
            reg_cd[rd] = temp_List              
    else:                               
        reg_cd[rd] = str(reg_cd[rs]) + reg_cd[rt]               

def addu_instruction(R_instruction, reg_cd):            
    rs = R_instruction['rs']        
    rt = R_instruction['rt']            
    rd = R_instruction['rd']        
    V_rs = int(reg_cd[rs])          
    V_rt = int(reg_cd[rt])          
    if V_rs < 0:            
        V_rs = sign_change(V_rs)            
    if V_rt < 0:        
        V_rt = sign_change(V_rt)            
    reg_cd[rd] = V_rs + V_rt                        

def and_instruction(R_instruction, reg_cd):             
    rs = R_instruction['rs']        
    rt = R_instruction['rt']    
    rd = R_instruction['rd']                    
    B_rs = binary(reg_cd[rs])               
    B_rt = binary(reg_cd[rt])                   
    B_rd = ''               
    for i in range(0, 32):                  
        if int(B_rs[i]) * int(B_rt[i]):             
            B_rd += '1'                         
        else:                       
            B_rd += '0'                 
    reg_cd[rd] = decimal(B_rd)                  

def div_instruction(R_instruction, reg_cd):                     
    rs = R_instruction['rs']                        
    rt = R_instruction['rt']                
    reg_cd['$lo'] = reg_cd[rs] // reg_cd[rt]                
    reg_cd['$hi'] = reg_cd[rs] % reg_cd[rt]                 

def divu_instruction(R_instruction, reg_cd):                        
    rs = R_instruction['rs']                    
    rt = R_instruction['rt']                                
    V_rs = int(reg_cd[rs])                          
    V_rt = int(reg_cd[rt])                  
    if V_rs < 0:                                            
        V_rs = sign_change(V_rs)                                
    if V_rt < 0:                    
        V_rt = sign_change(V_rt)                        
    reg_cd['$lo'] = V_rs // V_rt                            
    reg_cd['$hi'] = V_rs % V_rt                     

def jr_instruction(R_instruction, reg_cd):                  
    rs = R_instruction['rs']                    
    V_rs = reg_cd[rs]                   
    return V_rs                     

def mfhi_instruction(R_instruction, reg_cd):                        
    rd = R_instruction['rd']                
    reg_cd[rd] = reg_cd['$hi']                  

def mflo_instruction(R_instruction, reg_cd):                    
    rd = R_instruction['rd']                        
    reg_cd[rd] = reg_cd['$lo']                          

def mthi_instruction(R_instruction, reg_cd):                            
    rs = R_instruction['rs']                
    reg_cd['$hi'] = reg_cd[rs]                      

def mtlo_instruction(R_instruction, reg_cd):                
    rs = R_instruction['rs']                
    reg_cd['$lo'] = reg_cd[rs]                      

def mult_instruction(R_instruction, reg_cd):                            
    rs = R_instruction['rs']                    
    rt = R_instruction['rt']                                
    reg_cd['$hi'] = reg_cd['$lo'] = reg_cd[rs] * reg_cd[rt]             

def multu_instruction(R_instruction, reg_cd):               
    rs = R_instruction['rs']            
    rt = R_instruction['rt']    
    V_rs = int(reg_cd[rs])                      
    V_rt = int(reg_cd[rt])                  
    if V_rs < 0:                
        V_rs = sign_change(V_rs)                    
    if V_rt < 0:                        
        V_rt = sign_change(V_rt)                    
    reg_cd['$hi'] = reg_cd['$lo'] = V_rs * V_rt             

def nor_instruction(R_instruction, reg_cd):             
    rs = R_instruction['rs']                        
    rt = R_instruction['rt']                
    rd = R_instruction['rd']                
    B_rs = binary(reg_cd[rs])           
    B_rt = binary(reg_cd[rt])                           
    B_rd = ''                   
    for i in range(0, 32):                  
        if not (int(B_rs[i]) or int(B_rt[i])):                  
            B_rd += '1'                 
        else:                   
            B_rd += '0'                 
    reg_cd[rd] = decimal(B_rd)                                  

def or_instruction(R_instruction, reg_cd):                      
    rs = R_instruction['rs']                
    rt = R_instruction['rt']                
    rd = R_instruction['rd']        
    B_rs = binary(reg_cd[rs])                       
    B_rt = binary(reg_cd[rt])               
    B_rd = ''
    for i in range(0, 32):                  
        if int(B_rs[i]) or int(B_rt[i]):                    
            B_rd += '1'                 
        else:               
            B_rd += '0'                     
    reg_cd[rd] = decimal(B_rd)                  

def sll_instruction(R_instruction, reg_cd):                     
    rs = R_instruction['rs']                
    rd = R_instruction['rd']                    
    sa = R_instruction['sa']                
    try:                        
        reg_cd[rd] = reg_cd[rs] << reg_cd[sa]                   
    except:                     
        pass                        

def slt_instruction(R_instruction, reg_cd):                 
    rs = R_instruction['rs']                
    rd = R_instruction['rd']        
    rt = R_instruction['rt']                        
    if reg_cd[rs] < reg_cd[rt]:             
        reg_cd[rd] = 1      
    else:                   
        reg_cd[rd] = 0                              

def sltu_instruction(R_instruction, reg_cd):                
    rs = R_instruction['rs']                
    rd = R_instruction['rd']                
    rt = R_instruction['rt']                
    V_rs = int(reg_cd[rs])              
    V_rt = int(reg_cd[rt])          
    if V_rs < 0:                    
        V_rs = sign_change(V_rs)                
    if V_rt < 0:                    
        V_rt = sign_change(V_rt)                    
    if V_rs < V_rt:                 
        reg_cd[rd] = 1                  
    else:                   
        reg_cd[rd] = 0                  

def srl_instruction(R_instruction, reg_cd):                 
    rt = R_instruction['rt']                    
    rd = R_instruction['rd']                    
    sa = R_instruction['sa']                
    try:                
        reg_cd[rd] = reg_cd[rt] >> reg_cd[sa]                   
    except:             
        pass                        

def sub_instruction(R_instruction, reg_cd):                     
    rs = R_instruction['rs']                    
    rd = R_instruction['rd']                
    rt = R_instruction['rt']                    
    temp_List = list()              
    if isinstance(reg_cd[rs],list):                 
        for i in reg_cd[rs]:                    
            temp_List.append(i - reg_cd[rt])                            
            reg_cd[rd] = temp_List                  
    else:               
        reg_cd[rd] = reg_cd[rs] - reg_cd[rt]                                

def subu_instruction(R_instruction, reg_cd):                
    rs = R_instruction['rs']                        
    rd = R_instruction['rd']                
    rt = R_instruction['rt']                            
    V_rs = int(reg_cd[rs])                  
    V_rt = int(reg_cd[rt])                      
    if V_rs < 0:                    
        V_rs = sign_change(V_rs)                            
    if V_rt < 0:                    
        V_rt = sign_change(V_rt)            
    reg_cd[rd] = V_rs - V_rt                        

def xor_instruction(R_instruction, reg_cd):                         
    rs = R_instruction['rs']                        
    rd = R_instruction['rd']        
    rt = R_instruction['rt']                    
    B_rs = binary(reg_cd[rs])                       
    B_rt = binary(reg_cd[rt])                   
    B_rd = ''                   
    for i in range(0, 32):                  
        if int(B_rs[i]) == int(B_rt[i]):                
            B_rd += '0'                     
        else:               
            B_rd += '1'                                 
    reg_cd[rd] = int(B_rd, 2)                       

