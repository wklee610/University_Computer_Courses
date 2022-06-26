#include <stdlib.h>
#include <stdio.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>
#include <random>
#include <math.h>
#include <ctime>
#include <string.h>

#define X_RESN 800
#define Y_RESN 800

#define G 6.67
#define T 3.0

#define MAX_MASS 10
#define MIN_MASS 5


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

int MAX_ITER;
int num_dot;

int main(int argc, char * argv[]){
    num_dot = atoi(argv[1]);
    MAX_ITER = atoi(argv[2]);
	Dot dots[num_dot];






	int a = 0;              
	int b = X_RESN; 

    double * before_vx;                 
    double * before_vy;                 

    before_vx = (double*)malloc(sizeof(double) * num_dot);                      
    before_vy = (double*)malloc(sizeof(double) * num_dot);                  

    double * after_vx;                      
    double * after_vy;                      

    after_vx = (double*)malloc(sizeof(double) * num_dot);                   
    after_vy = (double*)malloc(sizeof(double) * num_dot);                       

    double * x_col;                 
    double * y_col;                 

    x_col = (double*)malloc(sizeof(double) * num_dot);                      
    y_col = (double*)malloc(sizeof(double) * num_dot);              

    double * vy_col;                
    double * vx_col;                    

    vx_col = (double*)malloc(sizeof(double) * num_dot);                 
    vy_col = (double*)malloc(sizeof(double) * num_dot);                
    


	

    
    for(int i = 0; i < num_dot; i++){                   
		dots[i].x = (rand() % (b - a + 1)) + a;                                                                 
		dots[i].y = (rand() % (b - a + 1)) + a;                                     
		dots[i].mass = (rand() % (MAX_MASS - MIN_MASS + 1)) + MIN_MASS;                                     
		dots[i].size = 5;           
		dots[i].now_x = 0;                                                              
		dots[i].now_y = 0;  
		dots[i].vx = 0; 
		dots[i].vy = 0;                                 
	}




        clock_t beginTime, finishTime;              
        beginTime = clock();        
        
        
        
        Window          win;                            /* initialization for a window */
        unsigned
        int             width, height,                  /* window size */
                        x, y,                           /* window position */
                        border_width,                   /*border width in pixels */
                        display_width, display_height,  /* size of screen */
                        screen;                          //which screen 

        char            *window_name = "N-body sequential version", *display_name = NULL;
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

       


        if (  (display = XOpenDisplay (display_name)) == NULL ) {
           fprintf (stderr, "drawon: cannot connect to X server %s\n",
                                XDisplayName (display_name) );
        exit (-1);
        }
        
        /* get screen size */

        screen = DefaultScreen (display);
        display_width = DisplayWidth (display, screen);
        display_height = DisplayHeight (display, screen);

        /* set window size */

        width = X_RESN;
        height = Y_RESN;

        /* set window position */

        x = 0;
        y = 0;

        /* create opaque window */

        border_width = 4;
        win = XCreateSimpleWindow (display, RootWindow (display, screen),
                                x, y, width, height, border_width, 
                                BlackPixel (display, screen), WhitePixel (display, screen));

        
        
        
        size_hints.flags = USPosition|USSize;
        size_hints.x = x;
        size_hints.y = y;
        size_hints.width = width;
        size_hints.height = height;
        size_hints.min_width = 300;
        size_hints.min_height = 300;
        
        XSetNormalHints (display, win, &size_hints);
        XStoreName(display, win, window_name);

        /* create graphics context */

        gc = XCreateGC (display, win, valuemask, &values);

        XSetBackground (display, gc, WhitePixel (display, screen));
        XSetForeground (display, gc, BlackPixel (display, screen));
        XSetLineAttributes (display, gc, 1, LineSolid, CapRound, JoinRound);

        attr[0].backing_store = Always;
        attr[0].backing_planes = 1;
        attr[0].backing_pixel = BlackPixel(display, screen);

        XChangeWindowAttributes(display, win, CWBackingStore | CWBackingPlanes | CWBackingPixel, attr);

        XMapWindow (display, win);
        XSync(display,0);


//---------------------------------------------


    for(int i = 0; i < MAX_ITER; i++){              
    	for(int j = 0; j < num_dot; j++){               
	    	double cor_x = dots[j].x;               
	    	double cor_y = dots[j].y;           
	    	
            int size = dots[j].size;        
	    	
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
	    		vx = F_x * T / dots[j].mass + vx;
	    		vy = F_y * T / dots[j].mass + vy;
	    	}
	    	
            
            after_vx[j] = vx;
	    	after_vy[j] = vy;
	    	
    	}

    	for (int l = 0; l < num_dot; l++){

    		dots[l].vx = after_vx[l];
    		dots[l].vy = after_vy[l];

    		dots[l].x = dots[l].x + T*(after_vx[l]+before_vx[l] / 2);					

	    	dots[l].y = dots[l].y + T*(after_vy[l]+before_vy[l] / 2);						
	    	double cor_x = dots[l].x;					
	    	double cor_y = dots[l].y;					
	    	int size = dots[l].size;					

	        if(cor_x <= size or cor_x >= X_RESN - size){   
	        	    dots[l].vx = -dots[l].vx;
	        	    continue;
	    		}
	    	if(cor_y <= size or cor_y >= Y_RESN-size){ 
	    			dots[l].vy = -dots[l].vy;
	    		}
	        usleep(1);
    	}
//---------------------------------------------
    	double vx_col[num_dot];                     
    	double vy_col[num_dot];                 
    	double x_col[num_dot];                      
    	double y_col[num_dot];  

                        
    	for(int i = 0; i < num_dot; i++){
    		vx_col[i] = dots[i].vx;                             
    		vy_col[i] = dots[i].vy;                         
    		x_col[i] = dots[i].x;                       
    		y_col[i] = dots[i].y;
    	}





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
				double k_x_v = dots[k].vx;                          
	    		double k_yv = dots[k].vy;                          
	    		double x_dif = k_cor_x - cor_x;                                 
	    		double y_dif = k_cor_y - cor_y;                       
	    		double space_sqrt = pow(x_dif,2) + pow(y_dif,2);                            
	    		double space = sqrt(space_sqrt);                    

	    		if(space <= size + dots[k].size){
	    			if(space < 20){
	    				space = 20;                         
	    			}

	    			x_col[j]-=space*x_dif / space;                                      
	    			y_col[j]-=space*y_dif / space;                                    

	    			double mass_A = dots[j].mass;                   
	    			double mass_B = dots[k].mass;                           
    				vx_col[j] = (mass_A - mass_B) *dots[j].vx / (mass_A + mass_B) + (2*mass_B) *dots[k].vx / (mass_A + mass_B);                             
    				vy_col[j] = (mass_A - mass_B)*dots[j].vy / (mass_A + mass_B) + (2*mass_B)*dots[k].vy / (mass_A + mass_B);                 
	    		}
    		}
    	}




    	for(int i = 0; i < num_dot; i++){
    		dots[i].vx = vx_col[i];             
    		dots[i].vy = vy_col[i];             
    		dots[i].x = x_col[i];                                                                     
    		dots[i].y = y_col[i];               
    	}




    	if(i == 0){
    		XClearWindow(display,win);
    	}



    	for(int i = 0; i < num_dot; i++){                           
    		unsigned int size = dots[i].size;                           
    		double cor_x = dots[i].x;                           
    		double cor_y = dots[i].y;                           
   	    	XFillArc(display, win, gc, cor_x, cor_y, size, size, 0, 360*64);
	        usleep(100);
    	}
    	XFlush (display);
    	usleep(50000);
    	XClearWindow(display,win);
	}


        XFlush (display);
        sleep (20);
        
        
        finishTime = clock();
        printf("NAME: HAJUN LEE\n");
        printf("STUDENT ID: 117010437\n");
        printf("ASSIGNMENT 3, N-body Simulation, Sequential.\n");
        printf("num_dot : %d, MAX_ITER : %d\n", num_dot, MAX_ITER);
        printf("Total Runtime is: %f s\n", (float)(finishTime - beginTime) / CLOCKS_PER_SEC);
        return 0;
}


