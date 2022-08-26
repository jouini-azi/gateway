# gateway
this is an implementation of an gateway between that convert frames between two protocol IEC61850 and IEC61850.It is a python3 based gateway implementation that uses ctypes for the wrappers.

# Geting started

## IEC61850
- First of all we need to install the library iec 61850, we will download it  and install it  in directory .

-Get the library :

	git clone https://github.com/mz-automation/libiec61850.git

-cd into the directory :

	cd libiec61850

-compile the library :
	
	make dynlib
	
-install the library in the right place for the ctypes wrapper (you can modify this in lib61850.py if you prefer a different location):

	sudo cp build/libiec61850.so /usr/local/lib/

## IEC60870
- First of all we need to install the library iec 60870, we will download it  and install it  in directory .

-Get the library :

	git clone https://github.com/mz-automation/lib60870.git

-cd into the directory :

	cd lib60870/lib60870-C

-compile the library :
	
	make dynlib
	
-install the library in the right place for the ctypes wrapper (you can modify this in lib61850.py if you prefer a different location):

	sudo cp build/lib60870.so /usr/local/lib/

	
## Run gateway
-cd to the client project dir :

	cd ..
	cd ..
	cd ..
	
-then start the gateway:

	python3 gateway.py
	
### Warrning : this gateway will work if you have IEC61850 IED's runing.
### help : you can use   IED Simulator - Triangle MicroWorks
