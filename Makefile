
install:
	TOP=$(shell pwd);
	ipython --version
	cp -rf $(shell pwd)/profile_arman  $(HOME)/.config/ipython/     
	export PYTHONPATH=$(HOME)/pyBL/diffcalc:$(HOME)/pyBL/pyOlog/:$(HOME)/pyBL/:$(PYTHONPATH)
	cp -rf $(shell pwd)/pyOlog.conf $(HOME)/
	cp -rf $(shell pwd)/pyBL.conf $(HOME)/
	python $(shell pwd)/setup.py install   
	
clean:
	rm -rf $(HOME)/.config/ipython/profile_arman
	rm -rf $(HOME)/pyBL/build
	rm -rf $(HOME)/pyOlog.conf
	rm -rf $(HOME)/pyBL.conf
	rm -rf $(HOME)/diffractometer.log
	rm -rf $(HOME)/angle.log
