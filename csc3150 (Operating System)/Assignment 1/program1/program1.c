#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <signal.h>
#include <string.h>


int main(int argc, char *argv[]){        

	pid_t	pid;
	char	signal[10] = ""; 
	int		exit_code;    

	printf("Process start to fork\n"); 
	printf("I'm the parent process, my pid = %i\n", getpid()); 
	 
	pid = fork();							 							/* fork a child process */
	
	switch(pid){														/* execute test program */ 
		case 0 :
			printf("I'm the child process, my pid = %i\n", getpid());       
			printf("Child process start to execute the program\n");     
			
			char * execv_str[] = {NULL}; 
			
			if (execv(argv[1], execv_str) == -1){ 
				printf("No such file\n"); 
				
				exit(0); 
			}
			
			break;
		
		case -1 :		   
			perror("Process creation failed\n");   
			
			exit(1);
		default :
			exit_code = 0;  
			
			break;    
	} 
	
	if (pid != 0){									   					/* wait for child process terminates */
		
		int status;
		pid_t child_pid;   
		
		child_pid = waitpid(pid, &status, WUNTRACED); 
		
		printf("Parent process receiving the SIGCHLD signal\n");    
		
			
		if (WIFEXITED(status)){											/* check child process'  termination status */	
			printf("Child termination with exit status = %d\n", WEXITSTATUS(status));   
		}
		
		if (WIFSIGNALED(status)){		 
			switch (WTERMSIG(status)) 
			{
				case 1 :
					strcat(signal, "SIGHUP");   
					break;
				case 2 :
					strcat(signal, "SIGINT");  
					break;
				case 3 :
					strcat(signal, "SIGQUIT"); 
					break;
				case 4 :
					strcat(signal, "SIGILL"); 
					break;
				case 5 :
					strcat(signal, "SIGTRAP");   
					break;
				case 6 :
					strcat(signal, "SIGABRT"); 
					break;
				case 7 :
					strcat(signal, "SIGBUS"); 
					break;
				case 8 :
					strcat(signal, "SIGFPE");  
					break;
				case 9 :
					strcat(signal, "SIGKILL"); 
					break;
				case 11 :
					strcat(signal, "SIGSEGV"); 
					break;
				case 13 :
					strcat(signal, "SIGPIPE"); 
					break;
				case 14 :
					strcat(signal, "SIGALRM"); 
					break;
				case 15 :
					strcat(signal, "SIGTERM");    
					break; 
				default :
					break;           
			}
			printf("child process get %s signal\n", signal);  
			printf("child process is terminated by %s signal\n", signal); 
			printf("CHILD EXECUTION FAILED!!\n"); 
		}
		
		if (WIFSTOPPED(status)){										//stop
			printf("child process stopped\n");      
			printf("CHILD PROXESS STOPPED\n");     
		}
	}
	
	return 0;
}	

		

