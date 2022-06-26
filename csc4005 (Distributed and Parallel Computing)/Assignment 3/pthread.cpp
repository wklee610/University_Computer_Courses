#include <stdlib.h>
#include <stdio.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>
#include <random>
#include <math.h>
#include <pthread.h>
#include <ctime>
#include "sys/time.h"

#define X_RESN 800
#define Y_RESN 800

#define G 6.67
#define T 3.0

#define MAX_MASS 10
#define MIN_MASS 1


typedef struct Dot
        {
        double x;                               
        double y;                   
        double mass;        
        double vx;                  
        double vy;                  
        unsigned int size;          
        } dot;              


typedef struct Info
{
    int rank;                       
} info;             

Dot ** dots;
pthread_barrier_t barrier;

int NUM_THREADS;                                     
int MAX_ITER;                              
int set;                                                    
int num_dot;                        



double * after_vx;                                  
double * after_vy;
double * before_vx;                                     
double * before_vy;                                 
double * vy_col;                            
double * vx_col;                            
double * x_col;                             
double * y_col;                             








Window          win;                            /* initialization for a window */
unsigned
int             width, height,                  /* window size */
                x, y,                           /* window position */
                border_width,                   /*border width in pixels */
                display_width, display_height,  /* size of screen */
                screen;                         /* which screen */

char            *window_name = "N-body Simulation", *display_name = NULL;
GC              gc;
unsigned
long            valuemask = 0;
XGCValues       values;
Display         *display;
XSizeHints      size_hints;
Pixmap          bitmap;
XPoint          points[800];
FILE            *fp, *fopen ();
char            str[100];

XSetWindowAttributes attr[1];

       


void * cal_function(void * arg) {                       
    Info * info = (Info *)arg;                          
    int rank = info -> rank;                            
    int begin = rank * set;                         
    int finish = (rank + 1) * set;              
    
    if(finish > num_dot){                  
        finish = num_dot;                       
    }
    
    
    int total = finish - begin;                     
    int iter = 0;                                       
    
    while(iter < MAX_ITER){                 
        iter++;                             



        pthread_barrier_wait(&barrier);

        for(int i = begin; i < finish; i++){                            
            
            double cor_x = dots[i]  ->  x;                      
            double cor_y = dots[i]  ->  y;                      
            
            int size = dots[i]  ->  size;                       
            
            double vx = dots[i] -> vx;
            double vy = dots[i] -> vy;                        
            
            before_vx[i]= dots[i] -> vx;                      
            before_vy[i] = dots[i] -> vy;                             
            
            for(int j = 0; j<num_dot;j++){
                if(j == i){
                    continue;
                 }
                double j_cor_x = dots[j] -> x;                          
                double j_cor_y = dots[j] -> y;                          

                double x_dif = j_cor_x - cor_x;                             
                double y_dif = j_cor_y - cor_y;                             
                double space_sqrt = pow(x_dif,2) + pow(y_dif,2);                            
                double space = sqrt(space_sqrt);                            
                double F = G*dots[j] -> mass*dots[i] -> mass / space_sqrt;
                double F_x = F*x_dif / space;   
                double F_y = F*y_dif / space;                       
                vx = F_x*T / dots[i] -> mass+vx;                                    
                vy = F_y*T / dots[i] -> mass+vy;                        

            }
            after_vx[i] = vx;                               
            after_vy[i] = vy;                                                   
        }



        pthread_barrier_wait(&barrier);

        for(int i  = begin; i < finish; i++){                           

            dots[i] -> vx = after_vx[i];                        
            dots[i] -> vy = after_vy[i];                    

            dots[i] -> x = dots[i] -> x + T*(after_vx[i]+before_vx[i] / 2);                                 

            dots[i] -> y = dots[i] -> y + T*(after_vy[i]+before_vy[i] / 2);                 
            double cor_x = dots[i] -> x;                            
            double cor_y = dots[i] -> y;                            
            int size = dots[i] -> size;                     

            if(cor_x <= size or cor_x >= X_RESN - size){                            
                dots[i] -> vx = -dots[i] -> vx;             
                continue;                   
            }
            if(cor_y<=size or cor_y>=Y_RESN-size){                  
                    dots[i] -> vy = -dots[i] -> vy;                     
            }

        }



        pthread_barrier_wait(&barrier);

        for(int i = begin; i < finish; i++){                
            vx_col[i] = dots[i] -> vx;                  
            vy_col[i] = dots[i] -> vy;                  
            x_col[i] = dots[i] -> x;                        
            y_col[i] = dots[i] -> y;                        
        }



        pthread_barrier_wait(&barrier);

        for(int j=begin; j < finish; j++){
            double cor_x = dots[j] -> x;                        
            double cor_y = dots[j] -> y;                            
            double xv = dots[j] -> vx;
            double yv = dots[j] -> vy;                      
            int size = dots[j] -> size;                     
            
            for(int k=0; k < num_dot; k++){
                if(k == j){               
                    continue;                   
                }
                
                double k_cor_x = dots[k] -> x;                              
                double k_cor_y = dots[k] -> y;              
                double k_xv = dots[k] -> vx;                            
                double k_yv = dots[k] -> vy;                        
                double x_dif = k_cor_x - cor_x;                         
                double y_dif = k_cor_y - cor_y;                         
                double space_sqrt = pow(x_dif,2)+pow(y_dif,2);                          
                double space = sqrt(space_sqrt);                            

                if(space <= size + dots[k] -> size){
                    if(space < 20){
                        space = 20;
                    }

                    x_col[j]-= space*x_dif / space;  
                    y_col[j]-= space*y_dif / space;                              

                    double mass_A = dots[j] -> mass;                                                
                    double mass_B = dots[k] -> mass;                                        
                    vx_col[j] = (mass_A - mass_B)*dots[j] -> vx / (mass_A + mass_B) + (2*mass_B)*dots[k] -> vx / (mass_A + mass_B);                         
                    vy_col[j] = (mass_A - mass_B)*dots[j] -> vy / (mass_A + mass_B) + (2*mass_B)*dots[k] -> vy / (mass_A + mass_B);                                         

                }
            }
        }
        
        
        pthread_barrier_wait(&barrier);
        
        for(int i = begin; i < finish; i++){
            dots[i] -> vx = vx_col[i];                          
            dots[i] -> vy = vy_col[i];                      
            dots[i] -> x = x_col[i];                    
            dots[i] -> y = y_col[i];    
         }
          pthread_barrier_wait(&barrier);
    }
    pthread_exit(NULL); 
}











int main(int argc, char * argv[]) {
    
    
    num_dot = atoi(argv[1]);
    MAX_ITER = atoi(argv[2]);
    NUM_THREADS = atoi(argv[3]);

    dots = (Dot **)malloc(sizeof(Dot*) * num_dot);
    after_vx = (double*)malloc(sizeof(double) * num_dot);                           
    after_vy = (double*)malloc(sizeof(double) * num_dot);                               
    before_vx = (double*)malloc(sizeof(double) * num_dot);                      
    before_vy = (double*)malloc(sizeof(double) * num_dot);                              
    vx_col = (double*)malloc(sizeof(double) * num_dot);                         
    vy_col = (double*)malloc(sizeof(double) * num_dot);                             
    x_col = (double*)malloc(sizeof(double) * num_dot);      
    y_col = (double*)malloc(sizeof(double) * num_dot);                                  




    int a = 0;
	int b = X_RESN;
	for(int i = 0; i < num_dot; i++){

        Dot * dot_i = new Dot();
		dot_i -> x = (rand() % (b - a + 1)) + a;                        
		dot_i -> y = (rand() % (b - a + 1)) + a;                    
		dot_i -> mass = (rand() % (MAX_MASS - MIN_MASS + 1)) + MIN_MASS;                
		dot_i -> size = 6;
		dot_i -> vx = 0;                            
		dot_i -> vy = 0;    
        dots[i] = dot_i;    
	}



    pthread_t thread[NUM_THREADS];                          
    pthread_barrier_init(&barrier, 0, NUM_THREADS);                     
    
    
    clock_t beginTime, finishTime;          
    beginTime = clock();                                        
    
    
    set = ceil((double) num_dot / NUM_THREADS);                     
    for (int i = 0; i < NUM_THREADS; i++){                               
        Info * info = new Info;                                     
        info -> rank = i;

        int rc = pthread_create(&thread[i], NULL, &cal_function, info);                                         
        if(rc){                                                         
            fprintf(stderr, "Can't create %d thread\n", i);                               
            return EXIT_FAILURE;                                    
        }
        else{                                                   
        }                           
    }                               
    
    
    
    
    for (int i = 0; i < NUM_THREADS; ++i) {                                                              
        pthread_join(thread[i], NULL);                                                                                                 
    }

    
    
    
    finishTime = clock();
    printf("NAME: HAJUN LEE\n");                                                               
	printf("STUDENT ID: 117010437\n");
	printf("ASSIGNMENT 3, N-body Simulation, pthread.\n");                                          
    printf("num_dot : %d, MAX_ITER : %d, NUM_THREADS : %d \n", num_dot, MAX_ITER, NUM_THREADS);             
    printf("Total Runtime is: %f s\n", (float)(finishTime - beginTime) / CLOCKS_PER_SEC);                               
    return 0;
}
