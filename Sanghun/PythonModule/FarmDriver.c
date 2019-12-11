#include <linux/module.h>    
#include <linux/kernel.h>    
#include <linux/cdev.h>    
#include <linux/device.h>    
#include <linux/fs.h>              
#include <linux/slab.h>    
#include <linux/delay.h>
#include <linux/uaccess.h>    
//#include <asm/uaccess.h>    
#include <asm/io.h>
#include "FarmHeader.h"
// timer header
#include <linux/timer.h>

typedef struct {
        unsigned long   GPFSEL[6];      ///< Function selection registers.
        unsigned long   Reserved_1;
        unsigned long   GPSET[2];
        unsigned long   Reserved_2;
        unsigned long   GPCLR[2];
        unsigned long   Reserved_3;
        unsigned long   GPLEV[2];
        unsigned long   Reserved_4;
        unsigned long   GPEDS[2];
        unsigned long   Reserved_5;
        unsigned long   GPREN[2];
        unsigned long   Reserved_6;
        unsigned long   GPFEN[2];
        unsigned long   Reserved_7;
        unsigned long   GPHEN[2];
        unsigned long   Reserved_8;
        unsigned long   GPLEN[2];
        unsigned long   Reserved_9;
        unsigned long   GPAREN[2];
        unsigned long   Reserved_A;
        unsigned long   GPAFEN[2];
        unsigned long   Reserved_B;
        unsigned long   GPPUD[1];
        unsigned long   GPPUDCLK[2];
        //Ignoring the reserved and test bytes
} BCM2837_GPIO_REGS;

#define BCM2837_GPIO_BASE 0x3F200000
#define BCM2837_GPIO_SIZE sizeof(BCM2837_GPIO_REGS)
#define DEVICE_NAME "Farm"    
void __iomem *mem = NULL;
volatile BCM2837_GPIO_REGS * pRegs = NULL; //전체 gpio핀들의 레지스터 정보를 담고있는 스트럭쳐
void pinSet(int pin);
void pinClr(int pin);

dev_t id;    
struct cdev cdev;    
struct class *class;    
struct device *dev;    

farmCtl farmctl;

int simple_open (struct inode *inode, struct file *filp)    
{    
    printk( "open\n" );    
    return 0;    
}    
    
int simple_close (struct inode *inode, struct file *filp)    
{    
    printk( "close\n" );  
    return 0;    
}    
        
ssize_t simple_read(struct file *filp, char *buf, size_t size, loff_t *offset)    
{    
    printk( "simple_read\n" );    
    return 0;    
}    
        
ssize_t simple_write (struct file *filp, const char *buf, size_t size, loff_t *offset)    
{    
    printk( "simple_write\n" );    
    return 0;    
}    

long simple_ioctl ( struct file *filp, unsigned int cmd, unsigned long arg)    
{ 
    //cmd를 받아와서 그 cmd의 IOC TYPE과 IOC NR을 계산한다.
    if(_IOC_TYPE(cmd) != MY_IOC_MAGIC)
        return -EINVAL;
    if(_IOC_NR(cmd) >= MY_IOC_MAXNR)
        return -EINVAL;

    switch(cmd){
        case MY_IOC_GPIO_SET:
        {
            printk("MY_IOC_SET\n");
            copy_from_user((void *)&farmctl, (void *)arg, sizeof(farmctl));
            //farmCtl, 의 값을 가져와서 저장한다.
            printk("%d 포트, 오더는 %d 입니다. \n",farmctl.pin,farmctl.funcNum);
            break;
        }
        case MY_IOC_GPIO_ACTIVE:
        {
            //farmCtl, 구조체의 들어있는 pin에 해당하는 GPFSEL레지스터의 공간에 001을 써준다.
            //그렇게 아웃풋 모드로 만들어 주고, pinSet으로 전기신호를 내보낸다.
            int  i=0;
            printk("%d 번 핀의 output을 ACTIVE 합니다.\n",farmctl.pin);
            unsigned long offset = farmctl.pin/10;
            unsigned long val = (u32)ioread32(&(pRegs->GPFSEL[offset]));
            int item = farmctl.pin % 10;
            val &= ~(0x7 << (item*3));
            val |= ((farmctl.funcNum & 0x7) << (item*3));
            iowrite32((u32)val, &(pRegs->GPFSEL[offset]));
            pinSet(farmctl.pin);
            break;
        }
        case MY_IOC_GPIO_INACTIVE:
        {
            //farmCtl, 구조체의 들어있는 pin에 해당하는 GPFSEL레지스터의 공간에 000을 써준다.???
            ///릴레이의 경우 GPCLR의 pin의 공간에 1을 써넣는것만으로는 꺼지지 않아 고민하고 이것저것
            ///시도해 보다가 그냥 Function 을 읽기로 바꿔버렸더니 꺼졌다...
            int  i=0;
            printk("%d 번 핀의 output을 INACTIVE 합니다.\n",farmctl.pin);
            unsigned long offset = farmctl.pin/10;
            unsigned long val = (u32)ioread32(&(pRegs->GPFSEL[offset]));
            int item = farmctl.pin % 10;
            val &= ~(0x7 << (item*3));
            val |= ((farmctl.funcNum & 0x7) << (item*3));   
            iowrite32((u32)val, &(pRegs->GPFSEL[offset]));
            pinClr(farmctl.pin);
            break;
        }        
    }    
    return 0;    
}    

struct file_operations simple_fops =    
{    
    .owner           = THIS_MODULE,    
    .read            = simple_read,         
    .write           = simple_write,        
    .unlocked_ioctl  = simple_ioctl,        
    .open            = simple_open,         
    .release         = simple_close,      
};    
        
int simple_init(void)    
{    
    int ret;    
        
    ret = alloc_chrdev_region( &id, 0, 1, DEVICE_NAME );    
    if ( ret ){    
        printk( "alloc_chrdev_region error %d\n", ret );    
        return ret;    
    }    
        
    cdev_init( &cdev, &simple_fops );    
    cdev.owner = THIS_MODULE;    
        
    ret = cdev_add( &cdev, id, 1 );    
    if (ret){    
        printk( "cdev_add error %d\n", ret );    
        unregister_chrdev_region( id, 1 );    
        return ret;    
    }    
        
    class = class_create( THIS_MODULE, DEVICE_NAME );    
    if ( IS_ERR(class)){    
        ret = PTR_ERR( class );    
        printk( "class_create error %d\n", ret );    
        
        cdev_del( &cdev );    
        unregister_chrdev_region( id, 1 );    
        return ret;    
    }    
        
    dev = device_create( class, NULL, id, NULL, DEVICE_NAME );    
    if ( IS_ERR(dev) ){    
        ret = PTR_ERR(dev);    
        printk( "device_create error %d\n", ret );    
        
        class_destroy(class);    
        cdev_del( &cdev );    
        unregister_chrdev_region( id, 1 );    
        return ret;    
    }
    // gpio memory mapping
    mem = ioremap(BCM2837_GPIO_BASE, BCM2837_GPIO_SIZE);
    pRegs = mem;
    return 0;    
}    
        
    
void simple_exit(void)    
{    
    iounmap(mem);
    device_destroy(class, id );    
    class_destroy(class);    
    cdev_del( &cdev );    
    unregister_chrdev_region( id, 1 );    
}    

        


void pinSet(int pin){
    unsigned long offset = farmctl.pin/32;
    //GPSET같은 경우 하나의 비트만 사용하니 
    //몇번째 레지스터인지 알아볼 수있따 32로 나눈 몫을 통하여
    unsigned long mask = (1<<(farmctl.pin%32));
    //이번엔 32개중에 몇번째에 써야하는지를 알아야 하니 32로 나눈 나머지만큼 1을 쉬프트 해서 마스크를
    //만든다.
    iowrite32((u32)mask, &(pRegs->GPSET[offset]));
    //offset번째의 GPSET레지스터에 mask를 쓴다. 
    //이건그냥 1을쓰면 알았어하고 초기화 되기 때문에 GPFSEL처럼 레지스터내의 다른값들을 보존하고
    //하는 과정이필요가 없다.
    printk("%d에 %d 값을 썼습니다.",farmctl.pin,farmctl.funcNum);
}


void pinClr(int pin){
    unsigned long offset = farmctl.pin/32;
    unsigned long mask = (1<<(farmctl.pin%32));
    iowrite32((u32)mask, &(pRegs->GPCLR[offset]));
    printk("%d에 %d 값을 썼습니다.",farmctl.pin,farmctl.funcNum);
}

module_init(simple_init);    
module_exit(simple_exit);  

MODULE_LICENSE("Dual BSD/GPL");





