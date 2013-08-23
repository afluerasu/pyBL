'''
Created on Aug 23, 2013

@author: arkilic
'''
def __loadConfig():
    import os.path
    import ConfigParser
    cf=ConfigParser.SafeConfigParser()
    cf.read([
        '/etc/pyBL.conf',
        os.path.expanduser('~/pyBL.conf'),
        'pyBL.conf'
    ])
    return cf
_confBL=__loadConfig()
# print _confBL.sections()