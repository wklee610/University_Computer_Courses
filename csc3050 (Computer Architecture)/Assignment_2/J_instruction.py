import all_instruction              

def J_main(J_instruction):              
    instruction_name = J_instruction['instruction_name']                    
    func = eval('{}_instruction'.format(instruction_name))              
    return func(J_instruction)                      

def j_instruction(J_instruction):                   
    return all_instruction.decimal(J_instruction['target'])             

def jal_instruction(J_instruction):         
    return all_instruction.decimal(J_instruction['target'])             