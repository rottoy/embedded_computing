#include <stdio.h>    
#include <sys/types.h>    
#include <sys/stat.h>    
#include <sys/ioctl.h>    
#include <fcntl.h>    
#include <termios.h>
#include <unistd.h>    
#include "simple.h"
#include <string.h>

#define DEVICE_FILENAME  "/dev/Farm"    

int kbhit(void);


int main(int argc, char* argv[])    
{    
    int fd=0;
    int i=0;
    int thermoPin=atoi(argv[1]); //온습도계핀, 온도핀, 습도핀 이 순서이다.
    int temperPin=atoi(argv[2]);
    int humidPin=atoi(argv[3]);
    int order = atoi(argv[4]);
    char ch = 0;
    farmCtl farmctl;
    
    // init ledctl
    memset(&farmctl, 0, sizeof(farmctl));    
    int size = sizeof(farmctl);    
    farmCtl.pin=temperPin;
    printf("%d 가 핀번호 입니다.",farmctl.pin);
    // init device driver
    fd = open( DEVICE_FILENAME, O_RDWR|O_NDELAY );    
    if( fd >= 0 ){  
        // ledctl 
//         memcpy(ledhw.pin, pins, sizeof(pins));
        if(order)farmctl.funcNum = 1;
        else farmctl.funcNum=0;

        printf("send ledctl to device driver\n");
        ioctl(fd, MY_IOC_SET, &farmctl);  
        if(farmctl.funcNum)
            ioctl(fd, MY_IOC_ACTIVE);    
        else
            ioctl(fd,MY_IOC_INACTIVE);
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

