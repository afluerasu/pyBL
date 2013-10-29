'''
Created on Aug 9, 2013
Brookhaven National Lab
National Synchrotron Light Source
Upton, NY
@author: arkilic
'''
# TODO: add HardwareAdapter update circle names after diffcalc hardware object construction!
# TODO: Implement SPEC's frozen mode where some angles are frozen and chi, phi is used to align a sample
#

from pyBL._conf import _confBL
from pyOlog._conf import _conf
from pyBL.Diffractometer import Diffractometer
from cothread.catools import connect,caget

URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')
NAME=_confBL.get('diffractometer_config', 'name')
GEOMETRY=_confBL.get('diffractometer_config','geometry')
ENGINE=_confBL.get('diffractometer_config','engine')
TAG=_confBL.get('diffractometer_config','tag')
AUTHOR=_confBL.get('diffractometer_config','author')
pv1=_confBL.get('diffractometer_config','pv1')
pv2=_confBL.get('diffractometer_config','pv2')
pv3=_confBL.get('diffractometer_config','pv3')
pv4=_confBL.get('diffractometer_config','pv4')
pv5=_confBL.get('diffractometer_config','pv5')
pv6=_confBL.get('diffractometer_config','pv6')
pvList=[pv1,pv2,pv3,pv4,pv5,pv6]

def config(name,geometry,engine,tag,author):    
    diff=Diffractometer(name, geometry, engine, tag, author)
    diff.pvList=pvList
    diff.dummySetup(name, geometry, engine, tag, author)
    i=0
    for angle in diff.getangleList():
        angle.setPV(pvList[i])
        try:
            caget(pvList[i],timeout=1.5)
        except:
            print 'Unable to connect'+pvList[i]
            diff.logger.warning('Unable to connect'+pvList[i])
            connect(pvList[i],wait=False,cainfo=True)
        i+=1
    return diff

diff=config(name=NAME, geometry=GEOMETRY, engine=ENGINE, tag=TAG, author=AUTHOR)
diff.pvList=pvList
