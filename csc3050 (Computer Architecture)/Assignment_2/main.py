import labelTable
import R_instruction
import I_instruction
import J_instruction
import all_instruction

ll = all_instruction.ll
reg_dict = all_instruction.reg_dict


def R_hdl(line):            
    global reg_dict                 
    instruction_name = labelTable.R_cd.get(line[26: 32])                
    temp_instruction = dict()           
    temp_instruction['instruction_name'] = instruction_name         
    if not instruction_name == 'syscall':               
        rs = int(line[6: 11], 2)                        
        temp_instruction['rs'] = labelTable.reg_num[rs]             
        rt = int(line[11: 16], 2)                   
        temp_instruction['rt'] = labelTable.reg_num[rt]                     
        rd = int(line[16: 21], 2)                   
        temp_instruction['rd'] = labelTable.reg_num[rd]             
        temp_instruction['sa'] = int(line[21: 26], 2)               
    return R_instruction.R_main(temp_instruction, reg_dict)                     






def I_hdl(line, opcode):                        
    global reg_dict             
    instruction_name = labelTable.I_cd.get(opcode)              
    temp_instruction = dict()               
    temp_instruction['instruction_name'] = instruction_name             

    rs = int(line[6: 11], 2)                
    temp_instruction['rs'] = labelTable.reg_num[rs]             
    rt = int(line[11: 16], 2)               
    temp_instruction['rt'] = labelTable.reg_num[rt]                                   
    immediate = line[16:]                       
    temp_instruction['immediate'] = immediate                       
    return I_instruction.I_main(temp_instruction, reg_dict)                     






def J_hdl(line, name):                  
    global reg_dict                 
    temp_instruction = dict()                   
    temp_instruction['instruction_name'] = name                 
    temp_instruction['target'] = int(line[6:], 2)               
    return J_instruction.J_main(temp_instruction)                           







def main_handle(ll, start=0, end=0):                    
    for i in range(start, end):                     
        line = ll[i]                
        opcode = line[0: 6]                     
        if opcode == '0'.zfill(6):                      
            temp_mem = R_hdl(line)                      
            if temp_mem:                    
                main_handle(ll, temp_mem, len(ll))                          
                break       
        elif opcode == '000010':                        
            temp_mem = J_hdl(line, 'j')                 
            if temp_mem:                        
                main_handle(ll, temp_mem, len(ll))                          
                break                           
        elif opcode == '000011':                        
            temp_mem = J_hdl(line, 'jal')                                   
            if temp_mem:                    
                main_handle(ll, temp_mem, len(ll))                      
                break                       
        else:                       
            temp_mem = I_hdl(line, opcode)              
            print(temp_mem)                 
            if temp_mem:                
                main_handle(ll, temp_mem, len(ll))              
                print(temp_mem)                     
                break                   

                                    

def fileopen(file_addr='fib.asm'):                  
    open_file = open(file_addr, 'r')                    
    global ll                       
    ll.extend(open_file.read().splitlines())                        
    main_handle(ll, 0, len(ll))             
    open_file.close()                           

if __name__ == '__main__':                  
    file_name = input("Enter the machine code file's name: ")                               
    fileopen(file_name)             
