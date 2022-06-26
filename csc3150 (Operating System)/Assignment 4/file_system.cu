#include "file_system.h"
#include <cuda.h>
#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>

using namespace std;          





__device__ __managed__ u32 gtime = 0;     





__device__ struct File
{
	char name[20];
	int size;               
	int last_dt;            
	int create_dt;            
};








__device__ void fs_init(FileSystem *fs, uchar *volume, int SUPERBLOCK_SIZE,           
							int FCB_SIZE, int FCB_ENTRIES, int VOLUME_SIZE,         
							int STORAGE_BLOCK_SIZE, int MAX_FILENAME_SIZE,            
							int MAX_FILE_NUM, int MAX_FILE_SIZE, int FILE_BASE_ADDRESS)         
{
  // init variables
  fs->volume = volume;

  // init constants
  fs->SUPERBLOCK_SIZE = SUPERBLOCK_SIZE;
  fs->FCB_SIZE = FCB_SIZE;
  fs->FCB_ENTRIES = FCB_ENTRIES;
  fs->STORAGE_SIZE = VOLUME_SIZE;
  fs->STORAGE_BLOCK_SIZE = STORAGE_BLOCK_SIZE;
  fs->MAX_FILENAME_SIZE = MAX_FILENAME_SIZE;
  fs->MAX_FILE_NUM = MAX_FILE_NUM;
  fs->MAX_FILE_SIZE = MAX_FILE_SIZE;
  fs->FILE_BASE_ADDRESS = FILE_BASE_ADDRESS;

}







__device__ int cnt(int num){
	int count = 0;              
	while(num > 1){           
		num /= 2;                 
		count++;              
	}
	return count;       
}


//sb = super block
//b = block


__device__ void sb_change(FileSystem *fs, int s_byte, int s_idx, int b_change, int run){             
	
  if(b_change == 0 && run == 0){                              
		fs -> volume[s_byte] -= 2 << (7 - s_idx - 1);                       
		return;                             
	}

	for(int j = 0; j < b_change; j++){                    
		
    if(run == 1){                        
			fs -> volume[s_byte] += 2 << (7 - s_idx - 1);                     
		}               
		
    else          
		{                               
			fs -> volume[s_byte] -= 2 << (7 - s_idx - 1);                     
		}                 
		s_idx++;                      
		
    if(s_idx > 7){                          
			s_byte++;                   
			s_idx = 0;                                              
		}       
	}   
}           






__device__ int file_search(FileSystem *fs, char * s){                                 
	for(int i = 0; i < fs -> FCB_ENTRIES; i++){                               
    int start_addr = fs -> SUPERBLOCK_SIZE + i * fs -> FCB_SIZE;                          
		char file_name[20];                       
		int refer = 0;                                       
		
    while(true){                          
			char andy = fs -> volume[start_addr + refer];                                               
			file_name[refer] = andy;                   
			if(refer == 19){                                 
        break;              
      }                                   
			refer += 1;                                  
		}                             
		bool cd = true;                   
		
    for(int i = 0; i < sizeof(s); i++){                 
			if(file_name[i] != s[i]){                   
        cd = false;                   
      }                     
		}

		if(cd){               
      return start_addr;                        
    }                   

	}                         
	return -1;
}








__device__ int FCB_info(FileSystem *fs, int FCB_addr, int run){              
	
  u32 info = 0;               
	int refer = 0;                  
	
  
  if(run == 0){         
		refer = 20;                     
		for(int i = 0; i < 4; i++){                     
			info += (fs -> volume[FCB_addr + refer + i]) << (32 - (i + 1) * 8);                 
		}               
	}                 
	

  else if(run == 1){            
		refer = 24;                   
		for(int j = 0; j < 4; j++){                                            
			info += (fs -> volume[FCB_addr + refer + j]) << (32 - (j + 1) * 8);                                           
		}               
	}           
  
  
  else if(run == 2){                    
		refer = 28;                 
		for(int k = 0; k < 2; k++){                       
			info += (fs -> volume[FCB_addr + refer + k]) << (16 - (k + 1) * 8);                             
		}             
	}                     


  else if(run == 3){                                  
		refer = 30;                                             
		for(int l = 0; l < 2; l++){                                               
			info += (fs -> volume[FCB_addr + refer + l]) << (16 - (l + 1) * 8);                                               
		}                 
	}             


  else{           
		return -1;                
	}               


	return info;                      
}







__device__ void swap(File *xp, File *yp)                  
{       
	File reset = *xp;            
	*xp = *yp;              
	*yp =  reset;         
}       








__device__ void insertSort(File list[], int n, int type_Sort){                    
	int i, j, max_idx;                      
	if(type_Sort == LS_D){                
		printf("===sort by modified time===\n");                  
		
    for(i = 0; i < n - 1; i++){                             
			max_idx = i;            
			
      for(j = i + 1; j < n; j++){                 
				
        if(list[j].last_dt > list[max_idx].last_dt){                                
					max_idx = j;                  
        }                 
      }                     
			swap(&list[max_idx], &list[i]);                           
		}                           
		

    while(list -> name[0] != '\0'){                   
			printf("%s \n", list -> name);                    
			list++;                 
		}         
	}                 



  else if(type_Sort == LS_S){                 
			printf("===sort by size===\n");                 
			for(i = 0; i < n - 1; i++){                                               
				max_idx = i;                            
				
        for(j = i + 1; j < n; j++){               
					if(list[j].size > list[max_idx].size){                    
						max_idx = j;                  
          }                 
					
          else if(list[j].size == list[max_idx].size){                  
						if(list[j].create_dt < list[max_idx].create_dt){                    
							max_idx = j;                
            }                                                     
					}                 
				}               

				swap(&list[max_idx], &list[i]);                           
			}                           
			while(list -> name[0] != '\0'){                       
				printf("%s    %i\n", list -> name, list -> size);                      
				list++;             
		}           
	}             
}             








__device__  File * get_file(FileSystem *fs, int type_Sort){                       
	File files[1024];

  memset(files, 0, sizeof(files));                            

  int count = 0;                            
	for(int i = 0; i < fs -> FCB_ENTRIES; i++){                                   
		int start_addr = fs -> SUPERBLOCK_SIZE + i * fs -> FCB_SIZE;                      
		char file_name[20];                               
		
    for(int j = 0; j < 20; j++){                      
      file_name[j] = fs -> volume[start_addr + j];                          
    }               
		
    if(file_name[0] != '\0'){                 
			File file;                                      
			file.last_dt = FCB_info(fs, start_addr, 2);                   
			file.create_dt = FCB_info(fs, start_addr, 3);                 
			
      for(int j = 0; j < 20; j++){                              
        file.name[j] = file_name[j];                              
      }

			file.size = FCB_info(fs, start_addr, 1);                
			files[count] = file;                       
			count++;            
		}             
	}                 


  insertSort(files, count, type_Sort);                                       


  return files;                                     
}               



__device__ u32 change_addr(FileSystem *fs, int s_byte, int s_idx){             
	if(s_byte > 0){               
    return (s_byte - 1) * 8 * 32 + s_idx * 32 + fs -> FILE_BASE_ADDRESS;        
  }           

  return s_idx * 32 + fs -> FILE_BASE_ADDRESS;          
}                         





__device__ void FCB_update(FileSystem *fs, u32 addr, int size, u32 fp, int run){  
	int start_addr = fp + 20;                           
	int reset = 0;                        
	
  for(int i = 0; i < 4; i++){     
		reset = (addr - (u32)(reset << (32 - 8 * i))) >> (32 - 8 * (i + 1));              
		fs -> volume[start_addr + i] = reset;           
	}                                                   
	
  
  reset = 0;                        
	start_addr = fp + 24;             
	
  
  for(int j = 0; j < 4; j++){                   
		reset = (size - (u32)(reset << (32 - 8 * j))) >> (32 - 8 * (j + 1));            
		fs -> volume[start_addr + j] = reset;   
	}               
	
  
  gtime++;              
	reset = 0;            
	start_addr = fp + 28;               
	
  
  for(int k = 0; k < 2; k++){                   
		reset = (gtime - (u32)(reset << (16 - 8 * k))) >> (16 - 8 * (k + 1));                     
		fs -> volume[start_addr + k] = reset;               
	}                                                                       
	
  
  if(run == 1){                       
		reset = 0;                
		start_addr = fp + 30;             
		
    for(int l = 0; l < 2; l++){                      
			reset = (gtime - (u32)(reset << (16 - 8 * l))) >> (16 - 8 * (l + 1));                       
			fs -> volume[start_addr + l] = reset;                 
		}           
	}             
}           
























__device__ u32 fs_open(FileSystem *fs, char *s, int op){                  
	/* Implement open operation here */
	
  

  u32 addr = NULL;                  
	int start_addr = file_search(fs, s);                              
	
  
  if(start_addr != -1){                                               
    return start_addr;                        
  }                                   

  if(op  ==   G_READ){                                                     
		printf("No file");                                             
		return -1;                                                              
	}                 

	bool cd = false;                                 
	int b_idx = 0;                                                  
	
  for(int m = 0; m < fs -> SUPERBLOCK_SIZE; m++){                         
		if(cd){                         
      break;                        
    }               

		int total = fs -> volume[m];                                   
		
    if(total != 255){                                         
			for(int i = 128;  i > 1;  i /= 2){              
				if(total / i == 0){              
					cd = true;       
					fs -> volume[m] += i;           
					addr = change_addr(fs, m, b_idx);             
					break;                
				}

        else{                   
					total -= i;                 
					b_idx++;                
				}             
			}               
		}             
	}               





	for(int i = 0; i < fs -> FCB_ENTRIES; i++){                   
		int start_addr = fs -> SUPERBLOCK_SIZE + i * fs -> FCB_SIZE;                  
		
    if(fs -> volume[start_addr] != '\0'){           
      continue;                 
    }                         
    
		int index = 0;                             

    while(s[index] != '\0'){                            
	  		fs -> volume[start_addr + index] = s[index];                    
			  index++;                    
		}                                    

		FCB_update(fs, addr, 0, start_addr, 1);                     
		return start_addr;                  
	}                             

	return -1;                  

}





__device__ void fs_read(FileSystem *fs, uchar *output, u32 size, u32 fp){
	/* Implement read operation here */
	int addr = FCB_info(fs, fp, 0);                       
	if(addr == -1){             
    return;             
  }                     
	for(int i = 0; i < size; i++){                    
		output[i] = fs -> volume[addr + i];           
	}         

  gtime++;                  
}                               










__device__ u32 fs_write(FileSystem *fs, uchar* input, u32 size, u32 fp){                
	/* Implement write operation here */
	int b_use = size  % 32 ==  0 ? size / 32 :  size / 32 +  1;             
	int addr = FCB_info(fs, fp, 0);                     
	
  if(addr == -1){       
    return;         
  }                         
	

  int b_addr = (addr - fs -> FILE_BASE_ADDRESS) / 32;                            
	int s_byte = b_addr / 8;                          
	int s_idx = b_addr % 8;                   
	int first_size = FCB_info(fs, fp, 1);                         
                            
  first_size = first_size % 32 == 0 ? first_size / 32 : first_size / 32 + 1;                
	sb_change(fs, s_byte, s_idx, first_size, 0);            


	int b_cnt = 0;                
	bool first_cd =  true;         
	int index = 0;                  
	
  
  
  
  while(b_cnt < b_use){                                             
		int total = fs -> volume[index];                    
		for(int i = 128; i > 1; i /= 2){                  
			if(total / i == 0){                       
				if(first_cd){                     
					s_idx = 7 - cnt(i);                   
					s_byte = index;                   
					first_cd = false;                 
				}                     

				b_cnt++;                          
				if(b_cnt == b_use){                               
          break;              
        }           
			}               
			

      else{             
				first_cd = true;              
				b_cnt = 0;              
				total -= i;           
			}               

		}                 
		index++;                      
		
    if(index > fs -> SUPERBLOCK_SIZE - 1 && b_cnt < b_use){               
      return -1;            
    }                     
	}                   
	
  sb_change(fs, s_byte, s_idx, b_use, 1);                                  
	addr = change_addr(fs, s_byte, s_idx);                         
	
  FCB_update(fs, addr, size, fp, 0);                              
	for(int k = 0; k < size; k++){            
    fs -> volume[addr + k] = input[k];              
  }                       
}                   





__device__ void fs_gsys(FileSystem *fs, int op){                
	/* Implement LS_D and LS_S operation here */  
  get_file(fs, op);               
}             








__device__ void fs_gsys(FileSystem *fs, int op, char *s){                         
	/* Implement rm operation here */
	if(op != RM){                                                     
    return;                         
  }                     
	
  int FCB_file_addr = file_search(fs, s);                             
	
  if(FCB_file_addr == -1){                
		printf("No file\n");                      
		return;                 
	}             

	int space_addr = FCB_info(fs, FCB_file_addr, 0);                            
	int size = FCB_info(fs, FCB_file_addr, 1);                   
	
  
  for(int i = 0; i < size; i++){                                    
    fs -> volume[space_addr + i] = 0;             
  }                       
	
  size =  size  %  32 == 0  ?  size / 32 : size  /  32  + 1;                                              
	
  int b_addr = (space_addr - fs -> FILE_BASE_ADDRESS) / 32;                     
	int s_byte = b_addr / 8;              
	int s_idx = b_addr % 8;                             
	sb_change(fs, s_byte, s_idx, size, 0);                  

	for(int j = 0; j < fs -> FCB_SIZE; j++){                
    fs -> volume[FCB_file_addr + j] = 0;                
  }           
}                 
