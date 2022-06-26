#pragma once



Window          win;									
char            *window_name = "Heat Simulation", *display_name = NULL;                     /* initialization for a window */					
Display         *display;								
GC              gc;				
unsigned long   valuemask = 0;							
XGCValues       values;		
XSizeHints      size_hints;						
Pixmap          bitmap;				
XSetWindowAttributes attr[1];								
int             width, height,                  /* window size */				
				x, y,                           /* window position */			
				border_width,                   /*border width in pixels */			
				display_width, display_height,  /* size of screen */				
				screen;                         /* which screen */						
				Colormap	default_cmap;					
XColor color[16];							




int setColor(){										
	int i;					
	for(i = 0; i < 16; i++){						
		color[i].flags = DoRed | DoGreen | DoBlue;					
	}								


//case 1
	color[0].red    =  0;									
	color[0].green  =  0;						
	color[0].blue   =  255 * 256;								
	XAllocColor(display, default_cmap, &color[0]);								


//case 2
	color[1].red    =  0;								
	color[1].green  =  75 * 256;							
	color[1].blue   =  255 * 256;						
	XAllocColor(display, default_cmap, &color[1]);										



//case 3
	color[2].red    =  0;											
	color[2].green  =  150 * 256;							
	color[2].blue   =  255 * 256;								
	XAllocColor(display, default_cmap, &color[2]);									


//case 4
	color[3].red    =  0;										
	color[3].green  =  200 * 256;							
	color[3].blue   =  255 * 256;										
	XAllocColor(display, default_cmap, &color[3]);										


//case 5
	color[4].red    =  50 * 256;																	
	color[4].green  =  255 * 256;							
	color[4].blue   =  255 * 256;											
	XAllocColor(display, default_cmap, &color[4]);						


//case 6
	color[5].red    =  150 * 256;							
	color[5].green  =  255 * 256;						
	color[5].blue   =  255 * 256;								
	XAllocColor(display, default_cmap, &color[5]);								


//case 7
	color[6].red    =  200 * 256;						
	color[6].green  =  255 * 256;							
	color[6].blue   =  255 * 256;											
	XAllocColor(display, default_cmap, &color[6]);								


//case 8
	color[7].red    =  255 * 256;						
	color[7].green  =  255 * 256;						
	color[7].blue   =  150 * 256;									
	XAllocColor(display, default_cmap, &color[7]);									


//case 9
	color[8].red    =  255 * 256;								
	color[8].green  =  255 * 256;								
	color[8].blue   =  50 * 256;										
	XAllocColor(display, default_cmap, &color[8]);											


//case 19
	color[9].red    =  255 * 256;									
	color[9].green  =  200 * 256;									
	color[9].blue   =  0;										
	XAllocColor(display, default_cmap, &color[9]);								


//case 11
	color[10].red    =  255 * 256;								
	color[10].green  =  150 * 256;									
	color[10].blue   =  100 * 256;											
	XAllocColor(display, default_cmap, &color[10]);								


//case 12
	color[11].red    =  255 * 256;									
	color[11].green  =  150 * 256;								
	color[11].blue   =  50 * 256;									
	XAllocColor(display, default_cmap, &color[11]);									


//case 13
	color[12].red    =  255 * 256;									
	color[12].green  =  100 * 256;								
	color[12].blue   =  0;						
	XAllocColor(display, default_cmap, &color[12]);									


//case 14
	color[13].red    =  230 * 256;								
	color[13].green  =  0;									
	color[13].blue   =  0;											
	XAllocColor(display, default_cmap, &color[13]);										


//case 15
	color[14].red    =  150 * 256;								
	color[14].green  =  0;								
	color[14].blue   =  0;								
	XAllocColor(display, default_cmap, &color[14]);											


//case 16
	color[15].red    =  75 * 256;							
	color[15].green  =  0;										
	color[15].blue   =  0;							
	XAllocColor(display, default_cmap, &color[15]);										

}							



int temperature_to_color_pixel(int t){									
	int output;											

	if(t >= 100){							
		output = color[15].pixel;						
	}								
	

	else if(t < 20){									
		output = color[0].pixel;							
	}									


	else{							
		int temp;							
		temp = floor((t - 20) / 5);												
		output = color[temp].pixel;						
	}						

	return output;								
}									