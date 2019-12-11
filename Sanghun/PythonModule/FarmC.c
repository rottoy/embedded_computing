#include <Python.h>
#include <wiringPi.h>
#include <stdio.h>    
#include <sys/types.h>    
#include <sys/stat.h>    
#include <sys/ioctl.h>    
#include <fcntl.h>    
#include <termios.h>
#include <unistd.h>   
#define DEVICE_FILENAME  "/dev/Farm"
#include "FarmHeader.h"

static PyObject *pinSet(PyObject *self, PyObject *args)
{
    int fd=0;
    int order = 0, pin= 0;
    int i = 0; // for
    farmCtl farmctl;
    
    
    if(!PyArg_ParseTuple(args, "ii", &pin,&order))
        return NULL;
    memset(&farmctl, 0, sizeof(farmctl));    
    int size = sizeof(farmctl);    
    farmctl.pin=pin;
    farmctl.funcNum=order;
    fd = open( DEVICE_FILENAME, O_RDWR|O_NDELAY );    
    if( fd >= 0 ){  

        if(order)farmctl.funcNum = 1;
        else farmctl.funcNum=0;

        printf("send ledctl to device driver\n");
        ioctl(fd, MY_IOC_GPIO_SET, &farmctl);  
        if(farmctl.funcNum)
            ioctl(fd, MY_IOC_GPIO_ACTIVE);    
        else
            ioctl(fd,MY_IOC_GPIO_INACTIVE);
    }
    close(fd);    
    Py_RETURN_NONE;
}

static PyObject *thermoSet(PyObject *self,PyObject *args)
{
    int ledPin = 0, pinNum = 0;
    int i = 0; // for
    
    if(!PyArg_ParseTuple(args, "i", &pinNum))
        return NULL;
    Py_RETURN_NONE;
}

static PyMethodDef keywdarg_methods[] = {
    {"pinSet", (PyCFunction)pinSet, METH_VARARGS, NULL},//첫번째 인자가 파이썬이 어떻게 호출할지, 두번째는여기서의 이름.
    {"thermoSet",(PyCFunction)thermoSet, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}   /* sentinel */
};

static struct PyModuleDef keywdargmodule = {
    PyModuleDef_HEAD_INIT,
    "blink",
    NULL,
    -1,
    keywdarg_methods
};

PyMODINIT_FUNC PyInit_FarmC(void)
{
    return PyModule_Create(&keywdargmodule);
}

