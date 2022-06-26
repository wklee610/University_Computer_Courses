#include <stdlib.h>
#include <stdio.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>
#include <random>
#include <math.h>
#include <ctime>
#include "sys/time.h"
#include <string.h>
#include <omp.h>

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
        double now_x;
        double now_y;
        unsigned int size;
        } dot;

int num_dot;                    
int MAX_ITER;                       
int NUM_THREADS;                    

int main(int argc, char * argv[]) {
    num_dot = atoi(argv[1]);                            
    MAX_ITER = atoi(argv[2]);                       
    NUM_THREADS = atoi(argv[3]);                    

    Dot dots[num_dot];                      
    
    
    
    double * after_vx;              
    double * after_vy;      
    double * before_vx;         
    double * before_vy;             
    double * vy_col;            
    double * vx_col;            
    double * x_col;             
    double * y_col;                 
    
    
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
    

    #pragma omp parallel for
    
    
    for(int i = 0; i < num_dot; i++){                                               
        dots[i].x = (rand() % (b - a + 1)) + a;                     
        dots[i].y = (rand() % (b - a + 1)) + a;                             
        dots[i].mass = (rand() % (MAX_MASS - MIN_MASS + 1)) + MIN_MASS;                         
        dots[i].size = 6;                           
        dots[i].now_x = 0;                                  
        dots[i].now_y = 0;                                  
        dots[i].vx = 0;                                 
        dots[i].vy = 0;                                                     
    }

    
    omp_set_num_threads(NUM_THREADS);
    
    
    
    clock_t beginTime, finishTime;              
    beginTime = clock();                 
    
    for(int i = 0; i < MAX_ITER; i++){                  
        
        
        #pragma omp parallel for    
        
        
        for(int j = 0; j < num_dot; j++){
            
            int size = dots[j].size;                            
            double cor_x = dots[j].x;                           
            double cor_y = dots[j].y;                       
            double force_x = 0;                     
            double force_y = 0;                     
            double vx = dots[j].vx;                             
            double vy = dots[j].vy;                     
            before_vx[j]= dots[j].vx;                       
            before_vy[j] = dots[j].vy;                      
            
            for(int k = 0; k < num_dot; k++){
                if(k == j){
                    continue;                               
                }

                double k_cor_x = dots[k].x;
                double k_cor_y = dots[k].y;

                double x_dif = k_cor_x - cor_x;
                double y_dif = k_cor_y - cor_y;                                 
                
                double space_sqrt = pow(x_dif, 2) + pow(y_dif, 2);                      
                double space = sqrt(space_sqrt);                        

                double F = G*dots[k].mass*dots[j].mass / space_sqrt;                             
                double F_x = F*x_dif / space;                                   
                double F_y = F*y_dif / space;                             
                
                vx = F_x*T / dots[j].mass + vx;                               
                vy = F_y*T / dots[j].mass + vy;                             
                }


            after_vx[j] = vx;
            after_vy[j] = vy;
            
        }
        
        
        
        #pragma omp parallel for
        
        
        for(int l = 0; l < num_dot; l++){

            dots[l].vx = after_vx[l];                       
            dots[l].vy = after_vy[l];                           
            dots[l].x = dots[l].x + T*(after_vx[l] + before_vx[l] / 2);                     
            dots[l].y = dots[l].y + T*(after_vy[l] + before_vy[l] / 2);                         
            double cor_x = dots[l].x;                               
            double cor_y = dots[l].y;                               
            int size = dots[l].size;                                
            
            if(cor_x <= size or cor_x >= X_RESN - size){
                    dots[l].vx = -dots[l].vx;                       
                    continue;                       
                }
            
            if(cor_y <= size or cor_y >= Y_RESN - size){
                    dots[l].vy = -dots[l].vy;                           
                }   
            
            usleep(1);
        }

        double vx_col[num_dot];                     
        double vy_col[num_dot];                     
        double x_col[num_dot];                              
        double y_col[num_dot];                          
        
        
        
        #pragma omp parallel for 
        
        
        
        
        for(int m = 0; m < num_dot; m++){
            vx_col[m] = dots[m].vx;             
            vy_col[m] = dots[m].vy;                 
            x_col[m] = dots[m].x;                       
            y_col[m] = dots[m].y;               
        }
        
        
        
        #pragma omp parallel for                            
        
        
        
        for(int j = 0; j < num_dot; j++){
            double cor_x = dots[j].x;                                       
            double cor_y = dots[j].y;                       
            double xv = dots[j].vx;
            double yv = dots[j].vy;                                         
            int size = dots[j].size;                                        
            
            for(int k = 0; k < num_dot; k++){
                if(k == j){                             
                    continue;
                }
                
                double k_cor_x = dots[k].x;                                             
                double k_cor_y = dots[k].y;                             
                double k_xv = dots[k].vx;                               
                double k_yv = dots[k].vy;                               
                double x_dif = k_cor_x - cor_x;                 
                double y_dif = k_cor_y - cor_y;             
                double space_sqrt = pow(x_dif, 2) + pow(y_dif, 2);                          
                double space = sqrt(space_sqrt);                            
                
                
                if(space <= size + dots[k].size){
                    if(space < 20){                 
                        space = 20;
                    }
                    x_col[j]-=space*x_dif / space;                              
                    y_col[j]-=space*y_dif / space;                      
                    
                    
                    double mass_A = dots[j].mass;                           
                    double mass_B = dots[k].mass;
                    
                    vx_col[j] = (mass_A - mass_B)*dots[j].vx / (mass_A + mass_B) + (2*mass_B)*dots[k].vx / (mass_A + mass_B);                               
                    vy_col[j] = (mass_A - mass_B)*dots[j].vy / (mass_A + mass_B) + (2*mass_B)*dots[k].vy / (mass_A + mass_B);           

                }
            }
        }
        
        
        
        #pragma omp parallel for 
        
        
        
            for(int n = 0 ; n < num_dot; n++){
                dots[n].vx = vx_col[n];                                       
                dots[n].vy = vy_col[n];                               
                dots[n].x = x_col[n];                                           
                dots[n].y = y_col[n];                                       
            }
        
        
        finishTime = clock();


        printf("NAME: HAJUN LEE\n");
        printf("STUDENT ID: 117010437\n");
        printf("ASSIGNMENT 3, N-body Simulation, openmp.\n");
        printf("num_dot : %d, MAX_ITER : %d, NUM_THREADS : %d\n", num_dot, MAX_ITER, NUM_THREADS);
        printf("Total Runtime is: %f s\n", (float)(finishTime - beginTime) / CLOCKS_PER_SEC);
        return 0;
    }
    }