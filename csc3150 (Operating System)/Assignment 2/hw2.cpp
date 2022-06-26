#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <curses.h>
#include <termios.h>
#include <fcntl.h>

#define ROW 10
#define COLUMN 50 
#define BRIDGE_TH 10


struct Node{
	int x , y; 
	Node( int _x , int _y ) : x( _x ) , y( _y ) {}; 
	Node(){} ; 
} frog ; 



struct ob_log{
	int direction;
	int length;
	int y;

	ob_log(int _direction, int _length, int _y) : direction(_direction), length(_length), y(_y){
	};
	ob_log(){
	};
};






char map[ROW+10][COLUMN] ; 
int G_Status = 0;
pthread_mutex_t mutex;
ob_log log[BRIDGE_TH + 1];








// Determine a keyboard is hit or not. If yes, return 1. If not, return 0. 
int kbhit(void){
	struct termios oldt, newt;
	int ch;
	int oldf;

	tcgetattr(STDIN_FILENO, &oldt);

	newt = oldt;
	newt.c_lflag &= ~(ICANON | ECHO);

	tcsetattr(STDIN_FILENO, TCSANOW, &newt);
	oldf = fcntl(STDIN_FILENO, F_GETFL, 0);

	fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

	ch = getchar();

	tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
	fcntl(STDIN_FILENO, F_SETFL, oldf);

	if(ch != EOF)
	{
		ungetc(ch, stdin);
		return 1;
	}
	return 0;
}


void renew(void){
	printf("\033[0;0H\033[2J");					//ASNI escape
	for(int i = 0; i <= ROW; ++i){
		puts(map[i]);
	}
}





void *logs_move( void *t ){
	/*  Move the logs  */
	int *L_ROW = (int *)t;
	int move = log[*L_ROW].direction;
	while(true){
		usleep(70000);
		int length = log[*L_ROW].length;
		int y = log[*L_ROW].y;						
		pthread_mutex_lock(&mutex);		

		for(int j = 0; j < COLUMN - 1; ++j){
			if(0 <= y && y <= COLUMN - 2 - length){
				if (y <= j && j < y + length){
					map[*L_ROW][j] = '=';
				}
				else{
					map[*L_ROW][j] = ' ';
				}
			}
			else{
				if((y <= j && j < COLUMN) || (0 <= j && j <= length - COLUMN + y - 1)){
					map[*L_ROW][j] = '=';
				}
				else{
					map[*L_ROW][j] = ' ';
				}
			}
			if (frog.x == *L_ROW){
				if (map[*L_ROW][frog.y] == ' '){
					G_Status = -1;
				}	
				if (j == frog.y){
					map[*L_ROW][j] = '0';							
				}
			}
		}

		renew();
		if(move){
			log[*L_ROW].y++;
			if(log[*L_ROW].y > COLUMN - 1){
				log[*L_ROW].y = 0;				
			}
			if(frog.x == *L_ROW){
				frog.y++;
			}
		}
		else{
			log[*L_ROW].y--;
			if(log[*L_ROW].y < 0){
				log[*L_ROW].y = COLUMN - 1;						
			}
			if(frog.x == *L_ROW){
				frog.y--;
			}
		}
		pthread_mutex_unlock(&mutex);						
		if (G_Status != 0){
			pthread_exit(NULL);			
		}
	}
}




	/*  Check keyboard hits, to change frog's position or quit the game. */

void *setting(void *t){
	char enter = 0;							
	while(true){
		if(kbhit()){
			pthread_mutex_lock(&mutex);								
			enter = getchar();				
			switch(enter){
				case 'a' :
					if(frog.x == ROW){
						map[ROW][frog.y] = '|';							
						frog.y--;
						map[ROW][frog.y] = '0';								
						renew();
					}
					else{
						frog.y--;
					}
					break;
				
				case 's' :
					if(frog.x < ROW){	
						frog.x++;					
						if (frog.x == ROW){	
							map[ROW][frog.y] = '0';									
							renew();		
						}
					}
					break;
				
				case 'd' :
					if(frog.x == ROW){	
						map[ROW][frog.y] = '|';													
						frog.y++;					
						map[ROW][frog.y] = '0';									
						renew();
					}
					else{
						frog.y++;
					}
					break;								
				
				case 'w' :
					if(frog.x == ROW){
						map[ROW][frog.y] = '|';									
					}
					if(frog.x == 0){	
						map[ROW][frog.y] = '0';										
					}
					frog.x--;
					break;
				
				case 'q' :
					G_Status = -2;								
					break;														
				
				default:
					break;									
			}
		}



		pthread_mutex_unlock(&mutex);						



		/*  Check game's status  */
		if(frog.x == 0){
			G_Status = 1;														
		}
		if(frog.y < 0 || frog.y > COLUMN - 1){
			G_Status = -1;										
		}
		if(G_Status != 0){
			pthread_exit(NULL);			
		}
	}
}











int main( int argc, char *argv[] ){


	// river map + frog start
	memset( map , 0, sizeof( map ) ) ;
	int i , j ; 
	for( i = 1; i < ROW; ++i ){	
		for( j = 0; j < COLUMN - 1; ++j )	
			map[i][j] = ' ' ;  		
	}	

	for( j = 0; j < COLUMN - 1; ++j )	
		map[ROW][j] = map[0][j] = '|' ;					

	for( j = 0; j < COLUMN - 1; ++j )	
		map[0][j] = map[0][j] = '|' ;				

	frog = Node( ROW, (COLUMN-1) / 2 ) ; 				
	map[frog.x][frog.y] = '0' ; 




	//Print map
	for( i = 0; i <= ROW; ++i)	
		puts( map[i] );
	
	for(i = 1; i <= BRIDGE_TH; i++){
		log[i] = ob_log(rand() % 2, 15, rand() % (COLUMN - 1));		
	}





	/*  Create pthreads for wood move and frog control.  */
	pthread_t threads[BRIDGE_TH];
	pthread_mutex_init(&mutex, NULL);

	
	int t_id[BRIDGE_TH - 1] = {1, 2, 3, 4, 5, 6, 7, 8, 9};					
	int temp;
	for(i = 0; i < BRIDGE_TH - 1; i++){
		temp = pthread_create(&threads[i], NULL, logs_move, (void *)&t_id[i]);		
	}
	pthread_create(&threads[10], NULL, setting, (void *)&t_id[10]);
	for(i = 0; i < BRIDGE_TH; i++){
		pthread_join(threads[i], NULL);			
	}










	/*  Display the output for user: win, lose or quit.  */
	if(G_Status == 1){
		printf("You WIN the game!!\n");									
	}
	else if(G_Status == -1){
		printf("You LOSE the game!!\n");						
	}
	else if(G_Status == -2){
		printf("You EXIT the game.\n");									
	}	
	pthread_mutex_destroy(&mutex);				
	pthread_exit(NULL);			
	


	return 0;

}
