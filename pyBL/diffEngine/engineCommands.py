'''
Created on Oct 1, 2013

@author: arkilic
'''
'''
Created on Oct 1, 2013

@author: arkilic
'''
from pyBL.commands import *
from logConfig import logInstance
from logConfig import NAME,URL

def currentLogConfig():
    '''
        To be implemented with a table in the future
    '''
    print 'Session Name: ',logInstance.getName()
    print 'Engine Name: ',getEngine()
    print '\n=Process Variable/Angle Relationships='
    getPV()
    print 'Local logging level: ',getLogLevel()
    print 'Diffractometer/Experiment Geometry',getGeometry()
    print 'Author:',getAuthor()
    listub()
    print '\n=OlogClient details='
    logInstance.getName()
    print 'url=',URL
    print 'Olog Logbooks:',logInstance.getologLogbook()
    print 'Olog Tag:',logInstance.getologTag()
    print '\n=Motor positions=\n',hardware()
    
def modifyLogConfig():   
    pass
    
    
    
    
def startup():
    currentLogConfig()
    