#include <linux/module.h>
#include <linux/sched.h>
#include <linux/pid.h>
#include <linux/kthread.h>
#include <linux/kernel.h>
#include <linux/err.h>
#include <linux/slab.h>
#include <linux/printk.h>
#include <linux/jiffies.h>
#include <linux/kmod.h>
#include <linux/fs.h>
#include <linux/string.h>

MODULE_LICENSE("GPL");


static struct task_struct *tsk; 
long x;
pid_t pid; 
int my_exec(void); 
int my_fork(void *argc); 
void my_wait(pid_t pid);   
int result; 
int status;  
 
struct wait_opts{
	enum pid_type wo_type;
	int wo_flags;
	struct pid *wo_pid; 
	struct siginfo __user *wo_info;
	int __user *wo_stat;
	struct rusage __user *wo_rusage;
	wait_queue_t child_wait;
	int notask_error; 
};

extern long do_wait(struct wait_opts *wo); 
extern long _do_fork(unsigned long clone_flags,         
	unsigned long stack_start,      
	unsigned long stack_size, 
	int __user *parent_tidptr, 
	int __user *child_tidptr,
	unsigned long tls);    
extern int do_execve(struct filename *filename,
	const char __user *const __user *__argv,
	const char __user *const __user *__envp); 
extern struct filename * getname(const char __user * filename); 

int my_exec(void){
	printk("[Program2]: child process\n");   
	const char path[] = "/home/wklee610/Desktop/problem2/test";
	const char *const argv[] = {path, NULL, NULL};  
	const char *const envp[] = {"HOME=/", "PATH=/sbin:/user/sbin:/bin:/usr/bin", NULL }; 
	struct filename *my_filename = getname(path);  
	result = do_execve(my_filename, argv, envp);  
	if (!result){
		return 0; 
	}
	do_exit(result);
}

void my_wait(pid_t pid){
	struct wait_opts wo;  
	struct pid *wo_pid = NULL;
	enum pid_type type;
	type = PIDTYPE_PID;
	wo_pid = find_get_pid(pid);  

	wo.wo_type = type;
	wo.wo_pid = wo_pid;
	wo.wo_flags = WEXITED;
	wo.wo_info = NULL;
	wo.wo_stat = (int __user*)&status;
	wo.wo_rusage = NULL;  
	
	x = do_wait(&wo);   
	status = *wo.wo_stat; 
	switch (status){   
		case 1 :
			printk("[Program2] : get SIGHUP signal");   
			printk("[Program2] : child process has hungup error");   
			break;
		case 2 :
			printk("[Program2] : get SIGINT signal");   
			printk("[Program2] : child process has SIGINT error");  
			break;
		case 3 :
			printk("[Program2] : get SIGQUIT signal");   
			printk("[Program2] : child process has SIGQUIT error");   
			break;
		case 4 :
			printk("[Program2] : get SIGILL signal");      
			printk("[Program2] : child process has SIGILL error");   
			break;
		case 5 :
			printk("[Program2] : get SIGTRAP signal");   
			printk("[Program2] : child process has SIGTRAP error");  
			break;
		case 6 :
			printk("[Program2] : get SIGABRT signal");   
			printk("[Program2] : child process has hungup error");  
			break;
		case 7 :
			printk("[Program2] : get SIGBUS signal");
			printk("[Program2] : child process has bus error");
			break;
		case 8 :
			printk("[Program2] : get SIGFPE signal");  
			printk("[Program2] : child process has SIGFPE error");   
			break;
		case 9 :
			printk("[Program2] : get SIGKILL signal");   
			printk("[Program2] : child process has SIGKILL error");   
			break;
		case 11 :
			printk("[Program2] : get SIGSEGV signal");    
			printk("[Program2] : child process has hungup error");  
			break;
		case 13 :
			printk("[Program2] : get SIGPIPE signal");  
			printk("[Program2] : child process has hungup error");   
			break;
		case 14 :
			printk("[Program2] : get SIGALRM signal");
			printk("[Program2] : child process has alarm error");
			break;
		case 15 :
			printk("[Program2] : get SIGTERM signal");
			printk("[Program2] : child process has SIGTERM error");
			break;
		default :
			break;
	}
	printk("[Do_Fork] : The return signal is %d\n", (int)*wo.wo_stat);
	put_pid(wo_pid);
	return;
} 

//fork function
int my_fork(void *argc){

	int i;  
	struct k_sigaction *k_action = &current->sighand->action[0];
	for(i=0;i<_NSIG;i++){
		k_action->sa.sa_handler = SIG_DFL;  
		k_action->sa.sa_flags = 0;  
		k_action->sa.sa_restorer = NULL;  
		sigemptyset(&k_action->sa.sa_mask);  
		k_action++; 
	}
	 
	/* fork a process using do_fork */
	/* execute a test program in child process */ 

	pid	= _do_fork(SIGCHLD, (unsigned long)&my_exec, 0, NULL, NULL, 0);  
	printk("[program2]: The child process has pid = %ld\n", (long int)pid);  
	printk("[program2]: This is the parent process, pid = %d\n", (int)current->pid);  

	/* wait until child process terminates */
	my_wait(pid);  
	return 0;  
}

static int __init program2_init(void){   

	printk("[program2] : Module_init\n");  
	printk("[program2] : Module_init create kthread start\n");  

	/* create a kernel thread to run my_fork */
	tsk = kthread_run(my_fork, NULL, "mythread%d", 1);
	if (!IS_ERR(tsk)){
		printk("[program2]: kthread start\n");
	}
	else{
		printk("error\n");
	}
	return 0;
}

static void __exit program2_exit(void){
	printk("[program2] : Module_exit\n");
}

module_init(program2_init);
module_exit(program2_exit); 
