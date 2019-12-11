#ifndef __FARMHEADER__
#define __FARMHEADER__

typedef struct _farmCtl{
    int pin;
    int funcNum;
    //한번의 한개의 핀을 funcNum에 따라서 
    //Set하려는 의도.
}__attribute__((packed))farmCtl;


#define MY_IOC_MAGIC 'c'
//매직넘버는 c로 할것이다. 99?
#define MY_IOC_GPIO_SET _IOW(MY_IOC_MAGIC, 0,farmCtl)
#define MY_IOC_GPIO_SETFUNC _IO(MY_IOC_MAGIC, 1)
#define MY_IOC_GPIO_ACTIVE _IO(MY_IOC_MAGIC, 2)
#define MY_IOC_GPIO_INACTIVE _IO (MY_IOC_MAGIC,3)

#define MY_IOC_MAXNR 4

#endif
