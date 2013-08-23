'''
Created on Aug 9, 2013

@author: arkilic
'''

def config(name,geometry,engine,tag,author):
    from Diffractometer import Diffractometer    
    from os import environ
    from os.path import expanduser
    diff=Diffractometer(name='default', geometry=' ', engine=' ', tag=' ', author=' ')
    diff.dummySetup(name, geometry, engine, tag, author)
    return diff
def _loadConfig(conf):
    return conf




diff=config(name='x11', geometry='SixCircle', engine='you', tag='tag', author='a')

