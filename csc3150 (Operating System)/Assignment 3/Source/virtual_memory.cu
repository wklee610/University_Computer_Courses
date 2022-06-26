#include "virtual_memory.h"
#include <cuda.h>
#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>






__device__ void init_invert_page_table(VirtualMemory *vm) {

  for (int i = 0; i < vm->PAGE_ENTRIES; i++) {
    vm->invert_page_table[i] = 0x80000000; // invalid := MSB is 1
    vm->invert_page_table[i + vm->PAGE_ENTRIES] = i;
  }
}

__device__ void vm_init(VirtualMemory *vm, uchar *buffer, uchar *storage,
                        u32 *invert_page_table, int *pagefault_num_ptr,
                        int PAGESIZE, int INVERT_PAGE_TABLE_SIZE,
                        int PHYSICAL_MEM_SIZE, int STORAGE_SIZE,
                        int PAGE_ENTRIES) {
  // init variables
  vm->buffer = buffer;
  vm->storage = storage;
  vm->invert_page_table = invert_page_table;
  vm->pagefault_num_ptr = pagefault_num_ptr;

  // init constants
  vm->PAGESIZE = PAGESIZE;
  vm->INVERT_PAGE_TABLE_SIZE = INVERT_PAGE_TABLE_SIZE;
  vm->PHYSICAL_MEM_SIZE = PHYSICAL_MEM_SIZE;
  vm->STORAGE_SIZE = STORAGE_SIZE;
  vm->PAGE_ENTRIES = PAGE_ENTRIES;

  // before first vm_write or vm_read
  init_invert_page_table(vm);
}




__device__ int idx_search(VirtualMemory *vm, int idx_page){                 
	int LRU_SET = vm -> invert_page_table[vm -> PAGE_ENTRIES];                    
	int idx = 0;                    
	
  for(int i = 0; i < vm -> PAGE_ENTRIES; i++){      
		if(idx_page == vm -> invert_page_table[i]){     
			idx = i;          
			vm -> invert_page_table[idx + vm -> PAGE_ENTRIES] ++;         
			return idx;         
		}
	}
	
  (*vm -> pagefault_num_ptr)++;                  
	
  for(int j = 0; j < vm->PAGE_ENTRIES; j++){      
		if(vm -> invert_page_table[j + vm -> PAGE_ENTRIES] < LRU_SET){    
			idx = j;              
			LRU_SET = vm -> invert_page_table[j + vm -> PAGE_ENTRIES];       
		}
	}         
	
  for(int l = 0; l < vm->PAGESIZE; l++){      
		vm -> storage[vm -> invert_page_table[idx] * vm -> PAGESIZE] = vm -> buffer[idx * vm -> PAGESIZE + l];        
		vm -> buffer[idx * vm -> PAGESIZE + l] = vm -> storage[idx_page * vm -> PAGESIZE + l];        
	}     
	
  vm -> invert_page_table[idx + vm -> PAGE_ENTRIES] ++;       
	vm -> invert_page_table[idx] = idx_page;        
	return idx;                 
}     




__device__ uchar vm_read(VirtualMemory *vm, u32 addr){        
	u32 offset = addr % vm -> PAGESIZE;             
  
  int idx_page = addr / vm -> PAGESIZE;               
	int idx = idx_search(vm, idx_page);             
	
  return vm -> buffer[(u32)(idx * vm -> PAGESIZE) + offset];                         
}




__device__ void vm_write(VirtualMemory *vm, u32 addr, uchar value){         
	u32 offset = addr % vm -> PAGESIZE;                   

  int idx_page = addr / vm -> PAGESIZE;                         
	int idx = idx_search(vm, idx_page);                         
	
  vm -> buffer[(u32)(idx * vm -> PAGESIZE) + offset] = value;               
	vm -> storage[addr] = vm -> buffer[(u32)(idx * vm -> PAGESIZE) + offset];        

}




__device__ void vm_snapshot(VirtualMemory *vm, uchar *results, int offset,        
                            int input_size) {
	for(int i = offset; i < offset + input_size; i++){  
		results[i] = vm_read(vm, i);      

    } 
  } 
