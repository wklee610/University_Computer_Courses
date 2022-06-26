import phase1
import phase2
import difflib




def main():         
    inputFile = input("Enter MIPS code file : ")            
    outputFile = input("Enter the name of output file : ")          
    expectedFile = input("Enter expected output file you want to compare : ")           
    result = phase2.translate(fileDict = phase1.getfile(inputFile)
                              , f_addr=inputFile)           
    
    #input
    try:        
        ofile = open(outputFile, 'w')       
        for data in result:     
            ofile.write(data+'\n')      
        print("Finished")                   
    except:                 
        print("Error, can't export data")               
    finally:                
        if ofile:               
            ofile.close()                   
    
    #output/expectedfile
    try:                
        outputFile = open(outputFile, 'r')              
        finalFile = open(expectedFile, 'r')             
        
        print(outputFile.read())        
        print(finalFile.read())             
        
        rate = difflib.SequenceMatcher(None, outputFile.read()
                                       , finalFile.read())           
        if rate.ratio() == 1.0:         
            print('Match percent is 100%')      
        else:               
            print('Match percent is not 100%')                          
            print('Match rate is : ', rate.ratio())                         
        
    
    except:         
        print("Error, failed to compare")                   
    finally:                    
        if outputFile:                      
            outputFile.close()                  
        if finalFile:                   
            finalFile.close()                   

if __name__ == '__main__':          
    main()      
    







