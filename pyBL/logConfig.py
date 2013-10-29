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

def createLogInstance(name,tagName,tagState):
    logInst=ExperimentalLog()
    logInst.createLogger(name)
    '''
    The following modules belong to a trial where logging into pyOlog was attempted.
    Logging will be handled into a Catalog (similar to pyOlog but instead of operational, main focus is on experimental procedures).
    Catalog entries will be generated after logging experimental steps into a local db OR text file for a given user session
    '''
#    logInst.createClient(url=URL, username=USR, password=PSWD)
#    logInst.createTag(tagName,tagState)
#    logInst.createLogbook(newLogbook='DiffractionLogbookv01', Owner='pyBL')
    return logInst

logInstance=createLogInstance(name=NAME,
                              tagName='DiffractometerTagv01',
                              tagState='Active')
#
#can read the logInstance parameters from the Olog.conf file
# logInstance.createProperty(name='trial',Type='random',Attachments=['a.txt'])
#logInstance.insertLog(Txt='Attempted first log', 
#                      Ownr='pybl', 
#                      logbook='DiffractionLogbookv01',
#                      type='randomv01',
                      #attachments='/usr/lib/b.txt'
#                      )
