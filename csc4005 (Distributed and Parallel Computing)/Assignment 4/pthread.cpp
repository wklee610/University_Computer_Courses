#include <iostream>                 
#include <stdlib.h>                     
#include <stdio.h>              
#include <X11/Xlib.h>                           
#include <X11/Xutil.h>      
#include <X11/Xos.h>        
#include <time.h>
#include <pthread.h>    
#include <math.h>   
#include "paint.h"  

using namespace std;    


typedef struct Fire {               
	int thread_id;  
}data_thread;   



int *change;        
int *temp;                              





pthread_barrier_t barrier_ITER;                     
pthread_barrier_t barrier_total;                        






int refreshScreen();                    
int fire_X;                             
int fire_Y;   
int NUM_THREADS;                            
int MAX_ITER;                           
struct timeval startTime, endTime, startsysTime;                                            
double totalTime, totalsysTime;                                         









void *cal_func(void *arg){              
	data_thread *data_input = (data_thread *)arg;                   
	int thread_id = data_input -> thread_id;                    
	int fireBound = fire_X / NUM_THREADS;                   
	int fireStart = thread_id * fireBound;                          
  






	if(thread_id == (NUM_THREADS - 1)){                 
		if(fire_X % NUM_THREADS != 0){                      

			fireBound = fire_X - 1 - fireStart + 1;                 
		}                           
	}                           
  



	int k;                      
	int i, j;                           
	int x_cor, y_cor;               
	
    
    


    
    for(k = 0; k < MAX_ITER; k++){                                      

		for(i = fireStart; i < fireStart + fireBound; i++){             
			if(i != 0 && i != (fire_X - 1)){                            
				
                
                
                for(j = 0; j < fire_Y; j++){                                                                
					
                    if(j != 0 && j != (fire_Y - 1)){                            
						y_cor = change[fire_Y * i + j + 1] - 2 * change[fire_Y * i + j] + change[fire_Y * i + j - 1];                                   
						x_cor = change[fire_Y * (i + 1) + j] - 2 * change[fire_Y * i + j] + change[fire_Y * (i - 1) + j];                               
						temp[fire_Y * i + j] = change[fire_Y * i + j] + 0.001 * (x_cor + y_cor);                                    

					}                           
                    
                    
                    
                    else{                               
                        temp[fire_Y * i + j] = change[fire_Y * i + j];                          
                        }                               
				    }                           
			}                                       
            else{                                               
                
                
                for(j = 0; j < fire_Y; j++){                            
					temp[fire_Y * i + j] = change[fire_Y * i + j];                      
				}               
            }                       
		}                           

		pthread_barrier_wait(&barrier_ITER);                                                    

		for(i = fireStart; i < fireStart + fireBound; i++){                             
			
            
            if(i != 0 && i != (fire_X - 1)){                                
				
                
                for(j = 1; j < fire_Y - 1; j++){                                    
					
					change[fire_Y * i + j] = temp[fire_Y * i + j];                                  
					
				}                       
			}                               
		}                               
    
		pthread_barrier_wait(&barrier_ITER);                                

		
        
        if(thread_id == 0){                     
			if(k % 10 == 0){                     
				refreshScreen();                     
			}                     
		}                     
		pthread_barrier_wait(&barrier_ITER);                     

	}                     





	pthread_barrier_wait(&barrier_total);                     





	return NULL;                     
}                     






int refreshScreen(){                     
	int i;                                      
	for(i = 0; i<fire_X; i++){                              
		for(int j = 0; j<fire_Y; j++){                                          
   
			XSetForeground(display, gc, temperature_to_color_pixel(change[fire_Y * i + j]));                                 
      
			XDrawPoint(display, win, gc, j, i);                                         

		}                           
	}                       

	
	XFlush(display);                

}                                   











int main(int argc, char* argv[]){                       

	NUM_THREADS = atoi(argv[1]);                    
	fire_X = atoi(argv[2]);             
	fire_Y = atoi(argv[3]);                     
    MAX_ITER = atoi(argv[4]);                               







	if((display = XOpenDisplay(display_name)) == NULL){                             
		fprintf(stderr, "drawon: cannot connect to X server %s\n", XDisplayName(display_name));                     
		exit(-1);                                                   
	}                                                               



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

	/* create graphics context */
	gc = XCreateGC(display, win, valuemask, &values);                               
	XSetBackground(display, gc, BlackPixel(display, screen));                       
	XSetForeground(display, gc, WhitePixel(display, screen));                   
	XSetLineAttributes(display, gc, 1, LineSolid, CapRound, JoinRound);                         

	default_cmap = DefaultColormap(display, screen);                            

	attr[0].backing_store = Always;                                     
	attr[0].backing_planes = 1;                                     
	attr[0].backing_pixel = BlackPixel(display, screen);                                        

	XChangeWindowAttributes(display, win, CWBackingStore | CWBackingPlanes | CWBackingPixel, attr);                 

	XMapWindow(display, win);               
	XSync(display, 0);                          

	XFlush(display);                        

	setColor();                         











	change = (int *)malloc(sizeof(int) * (fire_X * fire_Y));                                    
	temp = (int *)malloc(sizeof(int) * (fire_X * fire_Y));                              





	int i, j;                           



	for(i = 0; i < fire_X * fire_Y; i++){                       
		change[i] = 20;                         
	}                                                   
	
    
    
    for(i = 0; i < 100; i++){                                                           
		for(j = floor(fire_Y * 0.25); j < floor(fire_Y * 0.75); j++){                                                        
			change[fire_Y * i + j] = 100;                               
		}                       
	}                           




    refreshScreen();                        
  



	pthread_t thread[NUM_THREADS];                      
	data_thread data_input[NUM_THREADS];                                    




	int rp;                                     




	pthread_barrier_init(&barrier_ITER, NULL, NUM_THREADS);                         
	pthread_barrier_init(&barrier_total, NULL, NUM_THREADS+1);                          
 



    totalTime = 0;                      
	gettimeofday(&startTime, NULL);                     





	for(rp = 0; rp < NUM_THREADS; rp++){                                
		data_input[rp].thread_id = rp;                                  

		int rc = pthread_create(&thread[rp], NULL, cal_func, &data_input[rp]);                                  
		if(rc){                                 
			fprintf(stderr, "can't create pthread, %d\n", rc);                                  
			
            
            return EXIT_FAILURE;                                                    
		}               
	}                                                           



	pthread_barrier_wait(&barrier_total);                           





	gettimeofday(&endTime, NULL);                                       
	totalTime = (endTime.tv_sec - startTime.tv_sec) + (double)(endTime.tv_usec - startTime.tv_usec) / 1000000;                              
	printf("NAME: HAJUN LEE\n");                            
	printf("STUDENT ID: 117010437\n");                                  
	printf("Assignment 4, Heat Simulation, pthread version\n");                         
	printf("totalTime is %lf\n", totalTime);                
  




    for(rp = 0; rp < NUM_THREADS; rp++){                                        
		pthread_join(thread[rp], NULL);                         
	}                                   



	free(change);                           
	free(temp);                             



	pthread_barrier_destroy(&barrier_ITER);                                 
	pthread_barrier_destroy(&barrier_total);                            




	return 0;                               
}