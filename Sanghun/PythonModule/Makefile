obj-m+=FarmDriver.o

ARCH :=arm

PWD := $(shell pwd)

all:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) ARCH=$(ARCH) modules
demo:
	gcc -o FarmDriverApp FarmDriverApp.c

clean:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) ARCH=$(ARCH) clean
	rm -rf FarmDriverApp
	rm -rf ledModule.o ledModule.so



ledModule.so : ledModule.o
	$(CC) -shared -o $@ $^ $(LDLIBS)
ledModule.o : ledModule.c
	$(CC) -c -fPIC $^ -I/usr/include/python3.7

clean:


