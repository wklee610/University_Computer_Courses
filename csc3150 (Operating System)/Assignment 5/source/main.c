#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/stat.h>
#include <linux/fs.h>
#include <linux/workqueue.h>
#include <linux/sched.h>
#include <linux/interrupt.h>
#include <linux/slab.h>
#include <linux/cdev.h>
#include <linux/delay.h>
#include <asm/uaccess.h>
#include "ioc_hw5.h"



MODULE_LICENSE("GPL");



#define PREFIX_TITLE "OS_AS5"




// DMA
#define DMA_BUFSIZE 64
#define DMASTUIDADDR 0x0        // Student ID
#define DMARWOKADDR 0x4         // RW function complete
#define DMAIOCOKADDR 0x8        // ioctl function complete
#define DMAIRQOKADDR 0xc        // ISR function complete
#define DMACOUNTADDR 0x10       // interrupt count function complete
#define DMAANSADDR 0x14         // Computation answer
#define DMAREADABLEADDR 0x18    // READABLE variable for synchronize
#define DMABLOCKADDR 0x1c       // Blocking or non-blocking IO
#define DMAOPCODEADDR 0x20      // data.a opcode
#define DMAOPERANDBADDR 0x21    // data.b operand1
#define DMAOPERANDCADDR 0x25    // data.c operand2



#define IRQ_NUM 1 				//define IRQ_NUM at head of code				




void *dma_buf;				

//variables list 

dev_t dev_major;				
dev_t dev_minor;						
dev_t dev_num;						

struct cdev * cdev;						


unsigned int block_cd; //block_cd? code...  boolean type? 뭐지

int ret;									
int cnt;						
int begin;							
int rc;									
int id;				//
int interrupt;									
int answer;									

char a;												
int b;									
short c;						

//////////////////////////////////////////////////////////////////








// Declaration for file operations
static ssize_t drv_read(struct file *filp, char __user *buffer, size_t, loff_t*);
static int drv_open(struct inode*, struct file*);
static ssize_t drv_write(struct file *filp, const char __user *buffer, size_t, loff_t*);
static int drv_release(struct inode*, struct file*);
static long drv_ioctl(struct file *, unsigned int , unsigned long );







// cdev file_operations
static struct file_operations fops = {
      owner: THIS_MODULE,
      read: drv_read,
      write: drv_write,
      unlocked_ioctl: drv_ioctl,
      open: drv_open,
      release: drv_release,
};






// in and out function
void myoutc(unsigned char data,unsigned short int port);								
void myouts(unsigned short data,unsigned short int port);					
void myouti(unsigned int data,unsigned short int port);				
unsigned char myinc(unsigned short int port);					
unsigned short myins(unsigned short int port);				
unsigned int myini(unsigned short int port);				




// Work routine
static struct work_struct *work_routine;						




// For input data structure
struct DataIn {
    char a;			
    int b;		
    short c;					
} *dataIn;







// Arithmetic funciton
static void drv_arithmetic_routine(struct work_struct* ws);					







// Input and output data from/to DMA
void myoutc(unsigned char data,unsigned short int port) {
    *(volatile unsigned char*)(dma_buf+port) = data;
}
void myouts(unsigned short data,unsigned short int port) {
    *(volatile unsigned short*)(dma_buf+port) = data;
}
void myouti(unsigned int data,unsigned short int port) {
    *(volatile unsigned int*)(dma_buf+port) = data;
}
unsigned char myinc(unsigned short int port) {
    return *(volatile unsigned char*)(dma_buf+port);
}
unsigned short myins(unsigned short int port) {
    return *(volatile unsigned short*)(dma_buf+port);
}
unsigned int myini(unsigned short int port) {
    return *(volatile unsigned int*)(dma_buf+port);
}









static int drv_open(struct inode* ii, struct file* ff) {
	try_module_get(THIS_MODULE);			
    	printk("%s:%s(): device open\n", PREFIX_TITLE, __func__);			
	return 0;								
}








static int drv_release(struct inode* ii, struct file* ff) {
	module_put(THIS_MODULE);					
    	printk("%s:%s(): device close\n", PREFIX_TITLE, __func__);							
	return 0;									
}








static ssize_t drv_read(struct file *filp, char __user *buffer, size_t ss, loff_t* lo) {
	
	answer = myini(DMAANSADDR);						
	put_user(answer, (int *)buffer);			
	myouti(0, DMAANSADDR);				
    myouti(0, DMAREADABLEADDR);							
	printk("%s:%s(): ans = %d\n", PREFIX_TITLE, __func__, answer);								
    

	return 0;
}







static ssize_t drv_write(struct file *filp, const char __user *buffer, size_t ss, loff_t* lo) {
	char a;	
	int b;					
	short c;					
	// 임시 필요
	int temp;					
	
	
	get_user(a, (char *)buffer);									
	get_user(b, (int *)buffer + 1);									
	get_user(temp, (int*)buffer + 2);											
	
	c = (short)temp;						
	
	myoutc(a, DMAOPCODEADDR);								
	myouti(b, DMAOPERANDBADDR);							
	myouts(c, DMAOPERANDCADDR);						
	
	
	block_cd = myini(DMABLOCKADDR);					
	INIT_WORK(work_routine, drv_arithmetic_routine);					
	printk("%s:%s(): queue work\n", PREFIX_TITLE, __func__);						
	

	//IO block			
	if(block_cd){							
		printk("%s:%s(): block\n", PREFIX_TITLE, __func__);				
		schedule_work(work_routine);						
		flush_scheduled_work();											
	}			
	
	//IO non-block							
	else{										
		printk("%s:%s(): non-block IO\n", PREFIX_TITLE, __func__);						
		myouti(0, DMAREADABLEADDR);						
		schedule_work(work_routine);				
	}				


	return 0;			
}				







static long drv_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
	
	int word;					
	get_user(word, (int *)arg);				
	
	if(cmd == HW5_IOCSETSTUID){				
		printk("%s:%s(): My STUID is = %i\n", PREFIX_TITLE, __func__, word);									
		myouti(word, DMASTUIDADDR);								
	}
	
	else if(cmd == HW5_IOCSETRWOK){						
        myouti(0, DMAREADABLEADDR);							
		printk("%s:%s(): RW is OK\n", PREFIX_TITLE, __func__);									
	}
	
	else if(cmd == HW5_IOCSETIOCOK){							
		printk("%s:%s(): IOC is OK\n", PREFIX_TITLE, __func__);									
	}
	
	else if(cmd == HW5_IOCSETIRQOK){							
		myouti(0, DMACOUNTADDR);									
		printk("%s:%s(): IRQ is OK\n", PREFIX_TITLE, __func__);									
	}		

	else if(cmd == HW5_IOCSETBLOCK){						
		if(word == 0){									
			myouti(word, DMABLOCKADDR);										
			printk("%s:%s(): Non-Blocking IO\n", PREFIX_TITLE, __func__);						
		}
		
		else{									
			myouti(word, DMABLOCKADDR);									
			printk("%s:%s(): Blocking IO\n", PREFIX_TITLE, __func__);						
		}						
	}
	else if(cmd == HW5_IOCWAITREADABLE){						
		while(myini(DMAREADABLEADDR) != 1){								
			msleep(100);							
		}

		printk("%s:%s(): wait readable\n", PREFIX_TITLE, __func__);							
		put_user(1, (int *)arg);					
	}

	else{					
		printk("undefined operation.");				
	}		
	
	
	return 0;			
}		






static void drv_arithmetic_routine(struct work_struct* ws) {
	a = myinc(DMAOPCODEADDR);					
	b = myini(DMAOPERANDBADDR);				
	c = myins(DMAOPERANDCADDR);						
	//계산
	switch(a){							
		case '+':				
			answer = c + b;						
			break;								
		
		case '-':						
			answer = b - c;					
			break;						
		
		case '*':							
			answer = b * c;					
			break;						
		
		case '/':						
			answer = b / c;						
			break;							
		
		case 'p':						
			if(c < 0){													
				printk("invalid operentd c\n");								
				return;							
			}		
			
			cnt = 0;							
			begin = b;						
			
			while(cnt < c){				
				int i;				
				bool isCode;						
				
				
				isCode = true;						
				begin++;							
				
				for(i = 2; i <= begin / 2; i++){				
					if(begin % i == 0){					
						isCode = false;					
						break;				
					}	
				}					
				
				if(isCode){		
					cnt++;	
				}				
			}						
			
			
			answer = begin;		
			break;					
		
		default:				
			answer = 0;		
			break;								
	}							



	printk("%s:%s(): %d  %c  %hd  = %d\n", PREFIX_TITLE, __func__, b, a, c, answer);						
	myouti(answer, DMAANSADDR);				
	myouti(1, DMAREADABLEADDR);							
}



static irqreturn_t irq_handle(int irq, void* id){					
	printk("%s:%s(): enter irq_handle count\n", PREFIX_TITLE, __FUNCTION__);			
	interrupt += 1;							
	return IRQ_HANDLED;							
}




static int __init init_modules(void) {
	//변수 설정
	ret = -1;	
	interrupt = 0;	


	printk("%s:%s():...............Start...............\n", PREFIX_TITLE, __func__);			




	//요청
	rc = request_irq(IRQ_NUM, irq_handle, IRQF_SHARED, "interrupt", (void*)id);				
	printk("%s:%s(): irq request %i\n", PREFIX_TITLE, __FUNCTION__, IRQ_NUM);				



	ret = alloc_chrdev_region(&dev_num, 0, 1, "mydev");					
	
	if(ret < 0){					
		printk("%s:%s(): cannot alloc_chrdev\n", PREFIX_TITLE, __func__);						
		return 0;				
	}				
	
	
	dev_major = MAJOR(dev_num);				
	dev_minor = MINOR(dev_num);				
	
	
	printk("%s:%s(): register chrdev(%i, %i)\n", PREFIX_TITLE, __func__, dev_major, dev_minor);								


	//init cdev
	cdev = cdev_alloc();					
	cdev_init(cdev, &fops);										
	cdev -> owner = THIS_MODULE;							
	cdev_add(cdev, MKDEV(dev_major, dev_minor), 1);				
	ret = cdev_add(cdev, dev_num, 1);							
	
	
	if(ret < 0){						
		printk("cdev_add failed\n");				
		return ret;						
	}

	printk("%s:%s(): allocate dma buffer\n", PREFIX_TITLE, __func__);						
	
	dma_buf = kmalloc(DMA_BUFSIZE, GFP_KERNEL);											
	work_routine = kmalloc(sizeof(*work_routine), GFP_KERNEL);												
	return 0;								
}






static void __exit exit_modules(void) {				

	printk("%s:%s(): interrupt count = %i\n", PREFIX_TITLE, __FUNCTION__, interrupt);					

	kfree(dma_buf);										
	printk("%s:%s(): free dma buffer\n", PREFIX_TITLE, __FUNCTION__);						

	unregister_chrdev_region(MKDEV(dev_major, dev_minor), 1);									
	cdev_del(cdev);				

	kfree(work_routine);							
	free_irq(IRQ_NUM, (void *)id);					


	printk("%s:%s(): unregister chrdev\n", PREFIX_TITLE, __FUNCTION__);					
	printk("%s:%s():..............End..............\n", PREFIX_TITLE, __func__);			
}

module_init(init_modules);
module_exit(exit_modules);			
