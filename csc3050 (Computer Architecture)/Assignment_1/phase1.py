def getfile(f_addr = './testfile.asm'):                     
    line_cnt = 0                
    fileDict = dict()                       
    try:                
        f = open(f_addr, 'r')                   
        for l in f.readlines():                  
            if len(l.strip()) == 0 or l.startswith('#'):                      
                continue                
            else:                       
                result = l.find(':')                 
                if not result == -1:            
                    idx = l[0 : result]                      
                    fileDict[idx] = bin(line_cnt)[2:]                   
                line_cnt += 1                   
    except IOError:                     
        print("Error, can't open file")                     
    finally:                
        if f:                       
            f.close()               
    return fileDict                 
            








if __name__ == '__main__':
    getfile()

        
                    