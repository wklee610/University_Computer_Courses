/* Sequential Mandelbrot program */
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <iostream>
#include <time.h>

using namespace std;


#define         X_RESN  800       /* x resolution */
#define         Y_RESN  800       /* y resolution */
#define         NUM_THREADS 4

typedef struct complextype
{
    float real, imag;
} Compl;

typedef struct _thread_data {
	int thread_id;
}thread_data;


int *result;



void *cal_func(void *arg) {         
	thread_data *input_data = (thread_data *)arg;
	int thread_id = input_data -> thread_id;            
	int tot_part = X_RESN / NUM_THREADS;               
	int tot_start = thread_id * tot_part;                                                   

    /* Calculate points */
    int i, j, k;
    Compl   z, c;
    float   lengthsq, temp;

    for (i = tot_start; i < tot_start + tot_part; i++){
        for(j=0; j < Y_RESN; j++) {
            z.real = z.imag = 0.0;
            c.real = ((float) j - 400.0)/200.0;               /* scale factors for 800 x 800 window */
            c.imag = ((float) i - 400.0)/200.0;
            k = 0;

            do  {                                             /* iterate for pixel color */

            temp = z.real*z.real - z.imag*z.imag + c.real;
            z.imag = 2.0*z.real*z.imag + c.imag;
            z.real = temp;
            lengthsq = z.real*z.real+z.imag*z.imag;
            k++;
            } while (lengthsq < 12.0 && k < 100);
            if (k >= 100) {
                result[i*Y_RESN + j] = 1;
            }
        }

    }

	pthread_exit(NULL);
	//exit
}


int main ()
{
    Window          win;                            /* initialization for a window */
    unsigned
    int             width, height,                  /* window size */
                    x, y,                           /* window position */
                    border_width,                   /*border width in pixels */
                    display_width, display_height,  /* size of screen */
                    screen;                         /* which screen */

    char            *window_name = "Mandelbrot Set", *display_name = NULL;
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

    /* Mandlebrot variables */
    int i, j, k;
    Compl   z, c;
    float   lengthsq, temp;
    
    /* connect to Xserver */

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
    XSync(display, 0);


	struct timeval starTime, endTime, timeSystemStart;                                      
	double totalTime = 0, systemRunTime;                                    
	
    
    gettimeofday(&starTime, NULL);                          


    //INIT THREAD                               

	result = (int *)malloc(sizeof(int) * (X_RESN * Y_RESN));                    

	pthread_t thread[NUM_THREADS];                                                  
	thread_data input_data[NUM_THREADS];                                                

	int tot_part = X_RESN / NUM_THREADS;                                            

	Compl   z, c;
	int i, j, k;
	double  lengthsq, temp;                         
	int tempA;                                          

	for (tempA = 0; tempA < NUM_THREADS; tempA++) {                                     
		input_data[tempA].thread_id = tempA;                                                            

		int rc = pthread_create(&thread[tempA], NULL, cal_func, &input_data[tempA]);                                            
		if(rc){                                                     
			fprintf(stderr, "error: pthread_create, rc: %d\n", rc);                                                         
			return EXIT_FAILURE;                            
		}
	}

	if (X_RESN % NUM_THREADS != 0){                                 
		int tot_left = X_RESN % NUM_THREADS;                                                                            
		int tot_start = NUM_THREADS * tot_part;                                                     
		int tot_part = tot_left;                                            

		for (i = tot_start; i < tot_start + tot_part; i++) {
			for (j = 0; j < Y_RESN; j++) {
				z.real = z.imag = 0.0;
				c.real = ((float)j - Y_RESN / 2) / (Y_RESN / 4);  //scale factors for 800 x 800 window 
				c.imag = ((float)i - X_RESN / 2) / (X_RESN / 4);
				k = 0;

				do {

					temp = z.real*z.real - z.imag*z.imag + c.real;
					z.imag = 2.0*z.real*z.imag + c.imag;
					z.real = temp;
					lengthsq = z.real*z.real + z.imag*z.imag;
					k++;

				} while (lengthsq < 12 && k < 100); //lengthsq and k are the threshold

				if (k >= 100) {
					result[i * Y_RESN + j] = 1;                     
				}
			}
		}
	}
	
    
    
    for (tempA = 0; tempA < NUM_THREADS; tempA++){                                                      
		pthread_join(thread[tempA], NULL);                                                      

	}

	gettimeofday(&endTime, NULL);                       
	totalTime = (endTime.tv_sec - starTime.tv_sec) + (double)(endTime.tv_usec - starTime.tv_usec) / 1000000;                
        
        
    printf("NAME: Hajun Lee\n");                                                                                                    
    printf("STUDENT ID: 117010437\n");                                                      
    printf("ASSIGNMENT 2, PTHREAD VERSION\n");                                          
    printf("TOTAL TIME IS %lf\n", totalTime);                                           


	for (i = 0; i < X_RESN; i++) {
		for (int j = 0; j < Y_RESN; j++) {
			if (result[i * Y_RESN + j] == 1) {
				XDrawPoint(display, win, gc, j, i);
				usleep(1);
			}
		}
	}

    usleep(200000);
    XFlush (display);
    sleep (30);
    /* Program Finished */

    return 0;

}