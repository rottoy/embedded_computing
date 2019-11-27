#ifndef __SIMPLE__
#define __SIMPLE__

typedef struct _ledCtl{
    int pin[5];
    int funcNum;
}__attribute__((packed))ledCtl;

typedef struct _ledHW{
    int pin;
    int funcNum;
}__attribute__((packed))ledHW;

#define MY_IOC_MAGIC 'c'

#define MY_IOC_SET _IOW(MY_IOC_MAGIC, 0, ledCtl)
#define MY_IOC_GPIO_SETFUNC _IO(MY_IOC_MAGIC, 1)
#define MY_IOC_GPIO_ACTIVE _IO(MY_IOC_MAGIC, 2)
#define MY_IOC_N _IO(MY_IOC_MAGIC, 3)
#define MY_IOC_P _IO(MY_IOC_MAGIC, 4)
#define MY_IOC_S _IO(MY_IOC_MAGIC, 5)
#define MY_IOC_C _IO(MY_IOC_MAGIC, 6)

#define MY_IOC_MAXNR 7

#endif
