#include <stdio.h>    
#include <sys/types.h>    
#include <sys/stat.h>    
#include <sys/ioctl.h>    
#include <fcntl.h>    
#include <termios.h>
#include <unistd.h>    
#include "simple.h"
#include <string.h>

#define DEVICE_FILENAME  "/dev/Ex_06"    

#define LED1 26
#define LED2 19
#define LED3 21
#define LED4 20
#define LED5 16

int kbhit(void);

int ledControl(int pin, int order)    
{    
    int fd=0;
 
    int inputPit=pin;
    int inputOrder=order;
    printf("%d, %d 이게 인풋임", pin,order);
 
  
    ledHW ledhw;
    
   
    // init ledctl
    memset(&ledhw, 0, sizeof(ledhw));    
    int size = sizeof(ledhw);    
    ledhw.pin=pin;
    printf("%d 가 핀번호 입니다.",ledhw.pin);
    // init device driver
    fd = open( DEVICE_FILENAME, O_RDWR|O_NDELAY );    
    if( fd >= 0 ){  
        // ledctl 
//         memcpy(ledhw.pin, pins, sizeof(pins));
        if(order)ledhw.funcNum = 1;
        else ledhw.funcNum=0;

        printf("send ledctl to device driver\n");
        ioctl(fd, MY_IOC_SET, &ledhw);    
        ioctl(fd, MY_IOC_GPIO_SETFUNC);    
    }
  
    close(fd);    
    return 0;    
}

int kbhit(){
    struct termios oldt, newt;
    int ch;

    tcgetattr( STDIN_FILENO, &oldt );
    newt = oldt;
    newt.c_lflag &= ~( ICANON | ECHO );

    tcsetattr( STDIN_FILENO, TCSANOW, &newt );
    ch = getchar();
    tcsetattr( STDIN_FILENO, TCSANOW, &oldt );

    return ch;
}
