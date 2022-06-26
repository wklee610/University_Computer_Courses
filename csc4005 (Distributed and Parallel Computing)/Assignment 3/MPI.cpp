#include <stdlib.h>
#include <stdio.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>
#include <random>
#include <math.h>
#include <ctime>
#include "sys/time.h"
#include "mpi.h"
#include <algorithm>

#define X_RESN 800
#define Y_RESN 800

#define G 6.67
#define T 3.0

#define MAX_MASS 10
#define MIN_MASS 5




struct Dot
        {
        double x;       
        double y;                       
        double mass;        
        double vx;          
        double vy;          
        };







int main(int argc, char * argv[]) {
    int num_dot = atoi(argv[1]);
    int MAX_ITER = atoi(argv[2]);
    
    MPI_Status status;
    
    int com_size;
    int id;



    MPI_Init(&argc, &argv);                     
    MPI_Comm_size(MPI_COMM_WORLD, &com_size);           
    MPI_Comm_rank(MPI_COMM_WORLD, &id);             
    






    MPI_Datatype before_types[1] = {MPI_DOUBLE};                                        
    MPI_Datatype MPI_Dot;                                   
    MPI_Aint index[1] = {0};                              
    
    int lengthofBlock[1] = {5};                                     
    
    
    

    MPI_Type_create_struct(1, lengthofBlock, index, before_types, &MPI_Dot);                                   
    MPI_Type_commit(&MPI_Dot);                                          




    Dot * dots;                             
    dots = (Dot *)malloc(sizeof(Dot) * num_dot);                    



    int set = ceil((double)num_dot / com_size);
    int begin = id * set;
    int finish = (id + 1) * set;
    
    
    if(finish > num_dot){
    	finish = num_dot;
    }
    
    
    int total = finish - begin;
    int size = 6;
    double * after_vx;          
	double * after_vy;                      
	double * before_vx; 
	double * before_vy;
    double * vy_col;                
	double * vx_col;
	double * x_col;
	double * y_col;      
    
    
    Dot * total_dots;
    total_dots = (Dot *)malloc(sizeof(Dot) * total);                        
    
    after_vx = (double*)malloc(sizeof(double) * total);                         
    after_vy = (double*)malloc(sizeof(double) * total);             
    before_vx = (double*)malloc(sizeof(double) * total);                            
    before_vy = (double*)malloc(sizeof(double) * total);                

	vx_col = (double*)malloc(sizeof(double) * total);                   
    vy_col = (double*)malloc(sizeof(double) * total);                   
    x_col = (double*)malloc(sizeof(double) * total);                        
    y_col = (double*)malloc(sizeof(double) * total);            

    if(id == 0){
		int a = 0;                          
		int b = 800;                                                        
		for (int i = 0; i < num_dot; i++){

        Dot dot_i;
		dot_i.x = (rand() % (b - a + 1)) + a;                           
		dot_i.y = (rand() % (b - a + 1)) + a;                       
		dot_i.mass = (rand() % (MAX_MASS - MIN_MASS + 1)) + MIN_MASS;                           

		dot_i.vx = 0;
		dot_i.vy = 0;
        dots[i] = dot_i;
        }
    }

    clock_t beginTime, finishTime;                          
    beginTime = clock();                                




    MPI_Bcast(dots, num_dot, MPI_Dot, 0, MPI_COMM_WORLD);               
    
    for(int i = begin; i < finish; i++){
    	total_dots[i % set] = dots[i];                          
    }
    
    int c = 0;
    
    while(c < MAX_ITER){                            
        c++;
        MPI_Barrier(MPI_COMM_WORLD);                                

		for(int i = begin; i < finish; i++){                    
			int z = i % set;                
            double cor_x = total_dots[z].x;                     
            double cor_y = total_dots[z].y;                                         
            double vx = total_dots[z].vx;                   
            double vy = total_dots[z].vy;                       
            
            
            before_vx[z]= total_dots[z].vx;                 
            before_vy[z] = total_dots[z].vy;                        
            
            
            for(int k = 0; k < num_dot; k++){
                if(k == i){
                     continue;
                }
                double k_cor_x = dots[k].x;                     
                double k_cor_y = dots[k].y;             

                double x_dif = k_cor_x - cor_x;                             
                double y_dif = k_cor_y - cor_y;                                 
                double space_sqrt = pow(x_dif, 2) + pow(y_dif, 2);                                                       
                double space = sqrt(space_sqrt);                                                
                double F = G*dots[k].mass*total_dots[z].mass / space_sqrt;                                             
                double F_x = F*x_dif / space;                               
                double F_y = F*y_dif / space;                           
                vx = F_x*T / total_dots[z].mass + vx;                           
                vy = F_y*T / total_dots[z].mass + vy;                               

            }
            after_vx[z] = vx;
            after_vy[z] = vy;
        }



        MPI_Barrier(MPI_COMM_WORLD);



        for(int j = begin; j < finish; j++){
        	int d = j % set;                                
            total_dots[d].vx = after_vx[d];                             
            total_dots[d].vy = after_vy[d];                             

            total_dots[d].x = total_dots[d].x + T*(after_vx[d] + before_vx[d] / 2);                             
            total_dots[d].y = total_dots[d].y + T*(after_vy[d] + before_vy[d] / 2);                                 
            
            
            double cor_x = total_dots[d].x;                             
            double cor_y = total_dots[d].y;                 

            int size = 6;
            
            if(cor_x <= size or cor_x >= X_RESN - size){                   
                total_dots[d].vx = -total_dots[d].vx;                           
                continue;           
            }
            if(cor_y <= size or cor_y >= Y_RESN - size){                       
                total_dots[d].vy = -total_dots[d].vy;                       
            }
            usleep(1);
        }



        MPI_Barrier(MPI_COMM_WORLD);
        
        
        
        for(int i = begin; i < finish; i++){                    
        	int k = i % set;                    
            vx_col[k] = total_dots[k].vx;                       
            vy_col[k] = total_dots[k].vy;                       
            x_col[k] = total_dots[k].x;                 
            y_col[k] = total_dots[k].y;                         
        }
        
        
        MPI_Barrier(MPI_COMM_WORLD);
        
        
        for(int j = begin; j < finish; j++){       
        	int idx = j % set;                            
            double cor_x = total_dots[idx].x;                   
            double cor_y = total_dots[idx].y;                       
            double xv = total_dots[idx].vx;                             
            double yv = total_dots[idx].vy;                     
            int size = 6;
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
                if(space <= size + size){
                    if(space < 20){
                        space = 20;           
                    }                           
                    x_col[idx]-=space*x_dif / space;                              
                    y_col[idx]-=space*y_dif / space;                                          
                    double mass_A = dots[idx].mass;                     
                    double mass_B = dots[k].mass;                       
                    vx_col[idx] = (mass_A - mass_B)*dots[idx].vx / (mass_A + mass_B) + (2*mass_B)*dots[k].vx / (mass_A + mass_B);                                       
                    vy_col[idx] = (mass_A - mass_B)*dots[idx].vy / (mass_A + mass_B) + (2*mass_B)*dots[k].vy / (mass_A + mass_B);                                            

                }
            }
        }

        MPI_Barrier(MPI_COMM_WORLD);

        for(int i = begin; i < finish; i++){
        	int idx = i % set;                      
            total_dots[idx].vx = vx_col[idx];                       
            total_dots[idx].vy = vy_col[idx];                       
            total_dots[idx].x = x_col[idx];                     
            total_dots[idx].y = y_col[idx];                     
            }


        MPI_Barrier(MPI_COMM_WORLD);                    
        MPI_Gather(total_dots, total, MPI_Dot, dots, total, MPI_Dot, 0, MPI_COMM_WORLD);                            
        MPI_Bcast(dots, num_dot, MPI_Dot, 0, MPI_COMM_WORLD);                       
    }


    finishTime = clock();


    if(id == 0){                                
        printf("NAME: HAJUN LEE\n");                            
        printf("STUDENT ID: 117010437\n");                  
        printf("ASSIGNMENT 3, N-body Simulation, MPI\n");                       
        printf("num_dot : %d, MAX_ITER : %d, com_size : %d\n", num_dot, MAX_ITER, com_size);                
        printf("Total Runtime is: %f s\n", (float)(finishTime - beginTime) / CLOCKS_PER_SEC);
    }

    MPI_Finalize();
    return 0;
}