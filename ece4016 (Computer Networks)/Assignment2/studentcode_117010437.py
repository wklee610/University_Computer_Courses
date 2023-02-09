#ABR algorithm in low quality video
#A practical Evaluation of Rate Adaptation Algorithms in HTTP-based Adaptive Streaming-Published.pdf
#Algorithm 3, Bitrate adaptation algorithm of Bitmovin player
#HAJUN LEE 117010437
#import pdb

bitrate = 0 #used to save previous bitrate


def student_entrypoint(Measured_Bandwidth, Previous_Throughput, Buffer_Occupancy, Available_Bitrates, Video_Time, Chunk, Rebuffering_Time, Preferred_Bitrate ):
    #student can do whatever they want from here going forward
    global bitrate
    R_i = list(Available_Bitrates.items())  #previous and current
    R_i.sort(key=lambda tup: tup[1] , reverse=True)
    
    est_Bandwidth = Previous_Throughput #estimate Bandwidth using previous throughpsut
    
    bitrate = algorithm3(time = Video_Time,         
                        switch_rate = bitrate,          
                        pref_rate = Preferred_Bitrate,          
                        R_i = R_i,          
                        bandwidth = Buffer_Occupancy['current']) #bandwidth = current buffer            
    #bitrate = bufferbased(rate_prev=bitrate, buf_now= Buffer_Occupancy, r=Chunk['time']+1,R_i= R_i )
    return bitrate          

#helper function, to find the corresponding size of previous bitrate
def match(value, list_of_list):     
    for e in list_of_list:
        if value == e[1]:
            return e
            
#helper function, to find the corresponding size of previous bitrate
#if there's was no previous assume that it was the highest possible value
def prevmatch(value, list_of_list):
    for e in list_of_list:
        if value == e[1]:
            return e
    value = max(i[1] for i in list_of_list)
    
    for e in list_of_list:
        if value == e[1]:
            return e

def algorithm3(time, switch_rate, pref_rate, R_i, bandwidth):           
    time = time #the time passed from start         
    total_bitrate_video = len(R_i)  #total bitrate of video, R_i is array of bitrate of video           
                                    #key = bitrate, value = byte size of chunk          
    previous_rate = prevmatch(switch_rate, R_i) #Suggest rate from the previous     
    prefer_rate = prevmatch(pref_rate, R_i)   #Get prefer rate          
    #switch base bitrate            
    min_R = ['float("inf")', float("inf")] #Highest         
    max_R = ['0', 0]                        #Lowest         
    #threshold of video time            
    if time < 10:           
        for i in range(total_bitrate_video):            
            #if suggested rate > prefer rate            
            if R_i[i] == previous_rate:                     
                decision_rate = previous_rate[0]        
                return decision_rate            

            if R_i[i][1] <= prefer_rate[1]:         
                decision_rate = R_i[i][0]           
                return decision_rate        
        #else (or nothing matches in previous, return the high bitrate video)
        decision_rate = R_i[0][0]       
        return decision_rate            
        
    else:           
        #From lowest bitrate --> To highest bitrate         
        for i in range(total_bitrate_video - 1, -1, -1):            
            #Lowest bitrate         
            if min_R[1] > R_i[i][1]:        
                min_R = R_i[i]              
                
            #Highest bitrate            
            if max_R[1] < R_i[i][1] and R_i[i][1] < bandwidth:          
                max_R = R_i[i]      
            
        
        #if max_R[1] is not 0, decision_rate            
        if max_R[1] > 0:            
            decision_rate = max_R[0]            
        #rest, set to lowest            
        else:           
            decision_rate = min_R[0]        
        return decision_rate            
        
#if __name__ == "__main__":         
    
