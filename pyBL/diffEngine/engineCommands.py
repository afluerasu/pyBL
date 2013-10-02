'''
Created on Oct 1, 2013

@author: arkilic
'''
'''
Created on Oct 1, 2013

@author: arkilic
'''

def currentLogConfig():
    '''
        To be implemented with a table in the future
    '''
    from pyBL.commands import *
    from logConfig import logInstance
    print 'Diffractometer Configuration Session Name: ',logInstance.getName()
    hardware()
    getPV()
    getLogLevel()
