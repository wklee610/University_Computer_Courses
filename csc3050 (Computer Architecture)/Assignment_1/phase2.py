import labelTable
import phase1


def twosComplement(i):                  
    bc = bin(i)[2:].zfill(16)               
    index = bc.rfind('1')                   
    pc = bc[0: index].replace('1', 'a').replace('0', '1').replace('a', '0')                 
    bc = pc + bc[index:]                    
    return bc                           

def instruction_fill(raw_instruction, lineL):           
    lineL.extend([i for i   
                      in raw_instruction.values()           
                      if bool(i) != 0])         
    instruction = dict(zip(raw_instruction.keys(), lineL[1:]))          
    return instruction              



def Rtype_controller(lineL):                        
    instruction = instruction_fill(getattr(labelTable
                                           , '{0}_INSTRUCTION'.format(lineL[0].upper()))
                                   , lineL)
    bc = '000000'                   
    rs = instruction.get('rs', '00000')                 
    
    if rs == '00000':       
        bc += rs                            
    else:                           
        bc += bin(labelTable.reg_num.index(rs))[2:].zfill(5)                
        rt = instruction.get('rt', '00000')         
    
    if rt == '00000':                   
        bc += rt            
    else:                       
        bc += bin(labelTable.reg_num.index(rt))[2:].zfill(5)        
        rd = instruction.get('rd', '00000')                             
    
    if rd == '00000':               
        bc += rd                    
    else:                       
        bc += bin(labelTable.reg_num.index(rd))[2:].zfill(5)                        
        sa = instruction.get('sa', '00000')                     
    
    if sa == '00000':               
        bc += sa                        
    else:               
        bc += bin(int(sa))[2:].zfill(5)                         
        bc += instruction.get('function', '000000')     
    return bc               




def Itype_controller(lineL, fileDict):
    instruction = instruction_fill(getattr(labelTable
                                           , '{0}_INSTRUCTION'.format(lineL[0].upper()))
                                   , lineL)             
    raw_im = instruction['immediate']
    if '(' in raw_im and ')' in raw_im:       
        L_index = raw_im.index('(')      
        R_index = raw_im.index(')')      
        raw_rs = raw_im[L_index + 1 : R_index]       
        instruction['rs'] = raw_rs          
        instruction['immediate'] = raw_im[:L_index]      
        bc = instruction.get('opcode')      
        rs = instruction.get('rs', '00000')     
    
    if rs == '00000':           
        bc += rs            
    else:               
        bc += bin(labelTable.reg_num.index(rs))[2:].zfill(5)            
        rt = instruction.get('rt', '00000')         
    
    if rt == '00000':           
        bc += rt                    
    elif rt.isdigit():                          
        bc += rt                
    else:                           
        bc += bin(labelTable.reg_num.index(rt))[2:].zfill(5)                            
        im = instruction.get('immediate', '0'.zfill(16))                 
    
    if im in fileDict.keys():                    
        bc += fileDict[im].zfill(16)                         
    else:                       
        im = int(im)                      
        if im < 0:                   
            bc += twosComplement(abs(im))        
        else:                       
            bc += bin(im)[2:].zfill(16)                      
    return bc                   



def Jtype_controller(lineL, fileDict):              
    instruction = instruction_fill(getattr(labelTable
                                           , '{0}_INSTRUCTION'.format(lineL[0].upper()))
                                   , lineL)             
    bc = instruction.get('opcode', '0'.zfill(6))                
    bc += fileDict.get(lineL[1]).zfill(26)          
    return bc                   


def translate(fileDict, f_addr = "./testfile.asm"):           
    result = list()                   
    try:                
        f = open(f_addr, 'r')                                
        for line in f.readlines():                   
            if len(line.strip()) == 0 or line.startswith('#'):                  
                continue                    

            idx = line.find(':')                        
            if not idx == -1:                       
                line = line[idx + 1:]                   
                temp = line.find('#')           
            
            if not temp == -1:                      
                line = line[0:temp]                         
                lineL = line.replace(',', '').strip().split()               

            if lineL[0] in labelTable.Rtype:                        
                result.append(Rtype_controller(lineL))                  
            elif lineL[0] in labelTable.Itype:          
                result.append(Itype_controller(lineL, fileDict))                                    
            else:                   
                result.append(Jtype_controller(lineL, fileDict))                    
    except IOError:                         
        print("Error, can't open file")                 
    finally:                            
        if f:                       
            f.close()                       
        return result                       


if __name__ == '__main__':                      
    translate(fileDict = phase1.getfile())                      