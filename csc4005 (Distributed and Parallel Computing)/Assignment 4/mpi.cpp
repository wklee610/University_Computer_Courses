#include <iostream> 
#include <stdlib.h>         
#include <stdio.h>          
#include <X11/Xlib.h>   
#include <X11/Xutil.h>      
#include <X11/Xos.h>                
#include <time.h>       
#include <mpi.h>                
#include <math.h>           
#include "paint.h"                  

#define MASTER 0                            






using namespace std;                        








int *change;                        
int refreshScreen();                    
int comm_sz, comm_rank;                         
int fire_X;                             
int fire_Y;                     
int MAX_ITER;                           
double totalTime = 0;
double totalsysTime;                              





void cal_func(){                                    

	int fireBound = fire_X / comm_sz;                                           
	int fireStart = comm_rank * fireBound;                                                                       



    int *localchange = (int *)malloc(sizeof(int) * (fireBound * fire_Y));                                                         


	int i, j, k;                                                       
	int x_cor, y_cor;                                                                                        

	for(k = 0; k < MAX_ITER; k++){                                                                
        
        for(i = fireStart; i < fireStart + fireBound; i++){                                                                                
			
            if(i != 0 && i != (fire_X - 1)){                                                
				
                for(j = 0; j < fire_Y; j++){                                        
					
                    if(j != 0 && j != (fire_Y - 1)){                                                                
                                    
                        y_cor = change[fire_Y * i + j + 1] - 2 * change[fire_Y * i + j] + change[fire_Y * i + j - 1];                                           
                        x_cor = change[fire_Y * (i + 1) + j] - 2 * change[fire_Y * i + j] + change[fire_Y * (i - 1) + j];                               
                        
                        
                        localchange[fire_Y * (i - fireStart) + j] = change[fire_Y * i + j] + 0.001 * (x_cor + y_cor);                             
                        }               
                    
                    
                    
                    
                    else{                       
                        localchange[fire_Y * (i - fireStart) + j] = change[fire_Y * i + j];                                 
                    }

				}
			} 
            
            
            
            else{                                           
                for(j = 0; j < fire_Y; j++){                                
                localchange[fire_Y * (i - fireStart) + j] = change[fire_Y * i + j];                     
        }                               
      }                                     
    }                                                                           
    
    
		MPI_Allgather(localchange, fireBound*fire_Y, MPI_INT, change, fireBound*fire_Y, MPI_INT, MPI_COMM_WORLD);                               
   
    
		if(comm_rank == 0){                                 
			if(k % 10 == 0){                                            
				refreshScreen();                                
			}                           
		}                                               




		MPI_Barrier(MPI_COMM_WORLD);                        

	}                       

}                           

int refreshScreen(){                                    
	int i, j;                                   
  
	for(i = 0; i < fire_X; i++){                                
		for(j = 0; j < fire_Y; j++){                                    
      
			XSetForeground(display, gc, temperature_to_color_pixel(change[fire_Y * i + j]));                             
      
			XDrawPoint(display, win, gc, j, i);                     
		}                       
	}                                   
  
	XFlush(display);                                            
}                           









int main(int argc, char* argv[]){                                   

	fire_X = atoi(argv[1]);                                 
	fire_Y = atoi(argv[2]);                                             
    MAX_ITER = atoi(argv[3]);                                       
 
	



	MPI_Init(&argc, &argv);                                 
	MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);                                
	MPI_Comm_rank(MPI_COMM_WORLD, &comm_rank);                                      
 




    struct timeval startTime, endTime, startsysTime;                                                     
	if((display = XOpenDisplay(display_name)) == NULL){                                                                                
  		fprintf(stderr, "drawon: cannot connect to X server %s\n", XDisplayName(display_name));                                                                
  		exit(-1);                                                                                                                  
  	}                                       





	change = (int *)malloc(sizeof(int) * (fire_X * fire_Y));                    










    if(comm_rank == 0){



  	/* get screen size */
  	screen = DefaultScreen(display);                                            
  	display_width = DisplayWidth(display, screen);                      
  	display_height = DisplayHeight(display, screen);                                            




  	/* set window size */                           

  	width = fire_X;                         
  	height = fire_Y;                                

  	/* set window position */                           

  	x = 0;                                  
  	y = 0;                                  

  	/* create opaque window */          

  	border_width = 4;                       
  	win = XCreateSimpleWindow(display, RootWindow(display, screen),                                 
  		x, y, width, height, border_width,                                  
  		WhitePixel(display, screen), WhitePixel(display, screen));                                                              

  	size_hints.flags = USPosition | USSize;                                                             
  	size_hints.x = x;                               
  	size_hints.y = y;                       
  	size_hints.width = width;                                           
  	size_hints.height = height;                                     
  	size_hints.min_width = 100;                             
  	size_hints.min_height = 100;                                



  	XSetNormalHints(display, win, &size_hints);                                     
  	XStoreName(display, win, window_name);                              




  	/* create graphics context*/                           
  	gc = XCreateGC(display, win, valuemask, &values);                                                   
  	XSetBackground(display, gc, BlackPixel(display, screen));                                   
  	XSetForeground(display, gc, WhitePixel(display, screen));                                           
  	XSetLineAttributes(display, gc, 1, LineSolid, CapRound, JoinRound);                             

  	attr[0].backing_store = Always;                                             
  	attr[0].backing_planes = 1;                                     
  	attr[0].backing_pixel = BlackPixel(display, screen);                                

  	XChangeWindowAttributes(display, win, CWBackingStore | CWBackingPlanes | CWBackingPixel, attr);                                 

  	XMapWindow(display, win);                               
  	XSync(display, 0);                          

  	XFlush(display);                            

    default_cmap = DefaultColormap(display, screen);                                            
    


    setColor();                                 
    








    int i, j;



    for(i = 0; i < fire_X * fire_Y; i++){                       
  		change[i] = 20;                     
  	}                                   
  	
      
      
    for(i = 0; i < 100; i++){                           


        for(j = floor(fire_X * 0.25); j < floor(fire_X * 0.75); j++){                   



        	change[fire_Y * j + i] = 100;                               
  		}
  	}
    
    
    refreshScreen();                                
	  
    gettimeofday(&startTime, NULL);                 

     
	}                           
    
    
    
    
    
    
    
    MPI_Bcast(change, fire_X * fire_Y, MPI_INT, 0, MPI_COMM_WORLD);                       
    
    cal_func();                     

    if(comm_rank == 0){                             
        
        
        
        gettimeofday(&endTime, NULL);                                   
        totalTime = (endTime.tv_sec - startTime.tv_sec) + (double)(endTime.tv_usec - startTime.tv_usec) / 1000000;                      
        
        printf("NAME: HAJUN LEE\n");                        
        printf("STUDENT ID: 117010437\n");                      
        printf("Assignment 4, Heat Simulation, mpi version\n");                     
        printf("totalTime is %lf\n", totalTime);                            
    
        free(change);                   
	  
    }
  
	
    MPI_Finalize();             


	return 0;                       
}