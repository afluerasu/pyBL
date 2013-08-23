TOP=.
#my trial script

install:
	cd $(HOME)/.config/ipython
	cp -rf $(HOME)/pyBL/profile_arman  $(HOME)/.config/ipython/
	cd $(HOME)/pyBL
	export PYTHONPATH=$(HOME)/pyBL/diffcalc:$(HOME)/pyBL/pyOlog/:$(HOME)/pyBL/:$(PYTHONPATH)
	python setup.py install
	cd $(HOME)/pyBL/diffcalc
	python setup.py install
	cd $(HOME)/pyBL/
	git clone https://github.com/Olog/pyOlog.git
	cd $(HOME)/pyBL/pyOlog
	python setup.py install
	cp -rf $(HOME)/pyBL/pyOlog.conf $(HOME)/

