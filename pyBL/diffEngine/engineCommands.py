'''
Created on Oct 1, 2013
Brookhaven National Lab
National Synchrotron Light Source II

@author: arkilic
'''
#from commands import getAngleNames
from pyBL.commands import *
from logConfig import logInstance
from logConfig import NAME, URL

"""
This module serves as a library for the logic to be implemented in diffEngine. It will include required
"""
def currentLogConfig():
    '''
        To be implemented with a table in the future
    '''
    print '\n==Diffraction Experiment Parameters='
    print 'Session Name: ', logInstance.getName()
    print 'Engine Name: ', getEngine()
    print 'Author Name:', getAuthor()
    print 'Diffractometer/Experiment Geometry', getGeometry()
    print '\n=Process Variable/Angle Relationships='
    getPV()
    print '\n=Motor Names/Positions='
    print hardware()
    print '\n=Remote and Local Logging Details='
    logInstance.getName()
    print 'Local logging level: ', getLogLevel()
    print 'url=', URL
    print 'Olog Logbooks:', logInstance.getologLogbook()
    print 'Olog Tag:', logInstance.getologTag()
# TODO:Implement Characteristics for modes as in SPEC: omega zero(so that 2theta can reach this mode),omega fixed(pg 169 four circle reference of SPEC)


def modifyLogConfig():
    usrResponse = 'y'
    engineList = ['you', 'vlieg', 'willmott']
    while usrResponse == 'y':
        usrResponse = raw_input('Would you like to modify session configuration [y/n]')
        if usrResponse == 'n':
            break
        else:
            sessionName = raw_input('Session Name: ')
            while len(sessionName) == 0:
                print 'Blank name is not a valid entry '
                sessionName = raw_input('Session Name: ')
            logInstance.setName(sessionName)
            setName(name=sessionName)
            engineName = raw_input('Engine Name:')
            while len(engineName) == 0 or (engineName not in engineList):
                print 'Not a valid entry '
                engineName = raw_input('EngineName[you,willmott,vlieg]:')
            print engineName, engineList
            setEngine(engine=engineName)
            print getEngine()
    pvResponse = 'y'
    while pvResponse == 'y':
        pvResponse = raw_input('Would you like to modify Process Variable configuration [y/n]')
        if pvResponse == 'n':
            break
        else:
            getPV()
            print '\n'
            angNames = getAngleNames()
            for entry in angNames:
                pvName = raw_input(entry + '->')
                assignPV(name=entry, pv=pvName)
            getPV()
    logResponse = 'y'

#     while logResponse=='y':
#         logResponse=raw_input('Would you like to modify logging details?[y/n]')
#         if logResponse=='n':
#             break
#         else:
#             clientFlag=raw_input('Modify Olog Client?[y/n')
#             if clientFlag=='y':
#                 print "=Olog Client=\n"
#                 URL=raw_input('Url:')
#                 USR=raw_input('User:')
#                 PSWD=raw_input('Password:')
#                 logInstance.createClient(url=URL, username=USR, password=PSWD)
#             logbookFlag=raw_input('Modify the logbook?[y/n]')
#             if logbookFlag=='y':
#                 print '=Olog Logbook=\n'
#                 name=raw_input('Logbook Name:')
#                 ownr=raw_input('Logbook Owner:')
#                 logInstance.createLogbook(newLogbook=name, Owner=ownr)
#             tagFlag=raw_input('')
#             if tagFlag=='y':
#                 print '=Olog Tag=\n'
#                 tagName=raw_input('Tag Name:')
#                 tagState=raw_input('Tag State[Active/Inactive]:')
#                 logInstance.createTag(tagName,tagState)
#                 
#             
def startup():
    currentLogConfig()
    modifyLogConfig()
