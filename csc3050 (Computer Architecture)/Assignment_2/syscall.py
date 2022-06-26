
def syscall_instruction(reg_cd):                    
    sys_cd = int(reg_cd['$v0'])                          
    if sys_cd == 1:             
        print_integer = int(reg_cd['$a0'])                      
        print(print_integer)                    

    elif sys_cd == 4:                   
        if isinstance(reg_cd['$a0'],list):                  
            for i in reg_cd['$a0']:             
                print(chr(i), end='')                       
        else:                   
            print_string = reg_cd['$a0']                    
            print(print_string)                 

    elif sys_cd == 5:                       
        while True:                 
            read_integer = input('Please enter the integer : ')                     
            if read_integer.isdigit():                          
                reg_cd['$v0'] = int(read_integer)                       
                break                               
    
    elif sys_cd == 8:                       
        readint_integer = reg_cd['$a1']             
        if readint_integer == 1:                    
            read_string = ''                        
            reg_cd['$a0'] = read_string             
        elif readint_integer < 1:           
            pass                
        else:                           
            read_string = input('Please enter the string : '.format(str(readint_integer - 1)))          
            if len(read_string) <= readint_integer - 1:                     
                temp_List = [ord(i) for i in read_string]               
                temp_List.append(ord('\n'))                 
            else:               
                temp_List = [ord(i) for i in read_string[0: readint_integer-1]]                 
                temp_List.append(ord('\n'))                     
            reg_cd['$a0'] = temp_List                   
    
    elif sys_cd == 9:           
        reg_cd['$v0'] = reg_cd['$a0']               
    
    elif sys_cd == 10:          
        print("Exit")           
        exit()                  
    
    elif sys_cd == 11:                      
        print(chr(reg_cd['$a0']))                   

    elif sys_cd == 12:                          
        while True:                     
            read_char = input('Please enter the character : ')              
            if len(read_char) == 1:             
                reg_cd['$v0'] = ord(read_char)              
                break               