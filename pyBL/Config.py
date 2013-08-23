'''
Created on Aug 9, 2013

@author: arkilic
'''
from pyBL._conf import _confBL

NAME=_confBL.get('diffractometer_config', 'name')
GEOMETRY=_confBL.get('diffractometer_config','geometry')
ENGINE=_confBL.get('diffractometer_config','engine')
TAG=_confBL.get('diffractometer_config','tag')
AUTHOR=_confBL.get('diffractometer_config','author')

def config(name,geometry,engine,tag,author):    
    from Diffractometer import Diffractometer    
    from os import environ
    from os.path import expanduser
    diff=Diffractometer(name, geometry, engine, tag, author)
    diff.dummySetup(name, geometry, engine, tag, author)
    return diff


diff=config(name=NAME, geometry=GEOMETRY, engine=ENGINE, tag=TAG, author=AUTHOR)

