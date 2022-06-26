
/* Sequential Mandelbrot program */

#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <mpi.h>
#include <time.h>
#include <stdlib.h>
#include <iostream>

using namespace std;


#define         X_RESN  800       /* x resolution */
#define         Y_RESN  800       /* y resolution */
#define         MASTER    0

typedef struct complextype
        {
        float real, imag;
        } Compl;




int main(int argc, char *argv[])
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
        int a;
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

        //init MPI
        int NumofTask;
        int task;
        
        //start time
        struct timeval startTime, endTime, timeSystemStart;                                             
        double totalTime = 0, systemRunTime;                            
       
        MPI_Init(&argc, &argv);
        MPI_Comm_size(MPI_COMM_WORLD, &NumofTask);
        MPI_Comm_rank(MPI_COMM_WORLD, &task);   
        
        int part_width = X_RESN / NumofTask;                                                        
        unsigned long tot_part[part_width * Y_RESN]= {0};           
        unsigned long total[NumofTask * part_width * Y_RESN] = {0};                     

        if(task == MASTER){

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

            gettimeofday(&startTime, NULL);
        }

        
        
        
        /* Calculate and draw points */
        for(a = 0; a < NumofTask; a++){
            if(task == a){

                for(i= part_width * a; i < part_width * (a + 1); i++)
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

                } while (lengthsq < 4.0 && k < 100);

                if (k == 100){
                    tot_part[i - (part_width * a) + j * part_width] = 1;
                }
            
            }
            
            MPI_Gather(&tot_part, part_width * Y_RESN, MPI_INT, total, part_width * Y_RESN, MPI_INT, MASTER, MPI_COMM_WORLD);
             
        }
        }
            
    if (task == MASTER){
		gettimeofday(&endTime, NULL);
		totalTime = (endTime.tv_sec - startTime.tv_sec) + (double)(endTime.tv_usec - startTime.tv_usec) / 1000000;
        
        printf("NAME: Hajun Lee\n");                                
        printf("STUDENT ID: 117010437\n");                  
        printf("ASSIGNMENT 2, MPI VERSION\n");                          
        printf("TOTAL TIME IS %lf\n", totalTime);                               
    
        int l;

        for(l = 0; l < X_RESN * Y_RESN; l++){
            if(total[l] == 1){                  
                XDrawPoint (display, win, gc, (l % (part_width * Y_RESN)) / part_width, (l % (part_width * Y_RESN)) % part_width + (l / (part_width * Y_RESN)) * part_width);
                usleep(1);
            }       
        }    
            

        
         
        XFlush (display);
        sleep (30);
        }
        /* Program Finished */

    
}


