'''
Created on Sep 18, 2013

@author: arkilic
'''
from pyBL._conf import _confBL
from pyOlog._conf import _conf
from pyBLLog import ExperimentalLog


URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')
NAME=_confBL.get('diffractometer_config', 'name')
GEOMETRY=_confBL.get('diffractometer_config','geometry')
ENGINE=_confBL.get('diffractometer_config','engine')
TAG=_confBL.get('diffractometer_config','tag')
AUTHOR=_confBL.get('diffractometer_config','author')

def createLogInstance(name):
    logInst=ExperimentalLog()
    logInst.createLogger(name='Diffractometer')
    logInst.createClient(url=URL, username=USR, password=PSWD)
    print logInst.ologClient.listTags()[0].getName()
    return logInst

logInstance=createLogInstance(name=NAME)

