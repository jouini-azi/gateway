SHELL := /bin/bash
install:
	git clone https://github.com/mz-automation/libiec61850.git
	cd libiec61850;	\
	make dynlib;	\
	sudo cp build/libiec61850.so /usr/local/lib/ ;	\
	cd ..;	\
	git clone https://github.com/mz-automation/lib60870.git;	\

	cd lib60870/lib60870-C;	\
	make dynlib; \
	sudo cp build/lib60870.so /usr/local/lib/;	\
	cd ..;	\
	cd ..;	\

run:
	cd gateway-main/src/;	\
	python3 gateway.py

