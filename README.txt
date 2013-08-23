Installation
Step 1: 
Install EPICS base and recommended packages. See below link:
http://epics.nsls2.bnl.gov/debian/

Install Python 2.7: sudo apt-get install python-2.7

Install Ipython: sudo apt-get install ipython

Step 2:  
Clone pyBL git repository from: https://github.com/arkilic/pyBL/

Step 3:
 Inside pyBL/motorSim folder: 
$ make clean
$make install

Step 4: 
Confirm virtual motors are installed properly. Inside motorSim folder:
$./startSimMotorEdm.sh
$./startSimMotor.sh
Once both of these commands are performed, an edm window must show up displaying current motor positions. 

Step 5: 
Under home folder:
$cd ~/.ipyton
$cp -rf <path to cloned pyBL git repo>/profile_default/ <home folder of the user>/.ipython

Step 6: 
 Inside ~/pyBL:
$git clone https://github.com/DiamondLightSource/diffcalc.git
$git clone https://github.com/Olog/pyOlog.git
Configuration:
Step 1:
Add diffcalc repository to PYTHONPATH.Inside pyBL:
$vim pyBL/Config.py
environ['PYTHONPATH']='<path-to-diffcalc-repository>'
(alternatively, copy pyBL/diffcalc/setup.py and run $python setup.py install)

Step 2:
Inside Config.py modify configuration name and/or mode:
config(name,geometry,engine,tag)

Step 3:
$ ipython 
You will be ready to use PyBL with virtual motors


