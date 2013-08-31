'''
Commands
========
Python Beamline Scripting environment for NSLS2 beamlines provides users with routines handling hardware control, experimental logging, reciprocal space calculation and several other services that deals with image processing. The following commands are provided as of version 0.1.0 and are subject to change. Please use an up-to-date version of this code and documentation if you would like to benefit from full-capability.
'''
from Config import diff
from cothread.catools import caput
import logging

def setGeometry(Geometry):

    diff.setGeometry(Geometry)
    diff.setangleList(angleList=[])
    
def getGeometry():
    geoName=diff.getGeometry()
    return geoName.name

def getAngles():
    for angle in diff.getangleList():
        print angle.getName()

def setAngles(angles):
    if getGeometry()=='sixc':
        diff.setAnglesforHardware(angleList=angles, Geometry='sixcircle')
    elif getGeometry()=='fourc':
        diff.setAnglesforHardware(angleList=angles, Geometry='fourcircle')
    diff.setHardwareAdapter("DummyHardwareAdapter")
    diff.setDCInstance()

def getLogLevel():
    '''
        Returns the threshold of Python Logging Instances. User can set the level of detail
        for "diffractometer" log files:
            Level       When it is used
            DEBUG       Detailed information, typically of interest only when diagnosing problems.
            INFO        Confirmation that things are working as expected.
            WARNING     An indication that something unexpected happened, or indicative of some problem in the near future (e.g. disk space low). The software is still working as expected.
            ERROR       Due to a more serious problem, the software has not been able to perform some function.
            CRITICAL    A serious error, indicating that the program itself may be unable to continue running.
    '''
    levelDict=[{'level':logging.CRITICAL,'name':'Critical'},
               {'level':logging.DEBUG,'name':'Debug'},
               {'level':logging.INFO,'name':'Info'},
               {'level':logging.WARNING,'name':'Warning'},
               {'level':logging.ERROR,'name':'Error'}]
    for entry in levelDict:
        if entry['level']==diff.getLogLevel():
            print entry['name']

def setLogLevel(level):
    '''
        Sets the threshold of Python Logging Instances. User can set the level of detail
        for diffractometer log files:
            Level       When it is used
            DEBUG       Detailed information, typically of interest only when diagnosing problems.
            INFO        Confirmation that things are working as expected.
            WARNING     An indication that something unexpected happened, or indicative of some problem in the near future (e.g. disk space low). The software is still working as expected.
            ERROR       Due to a more serious problem, the software has not been able to perform some function.
            CRITICAL    A serious error, indicating that the program itself may be unable to continue running.
    '''
    levelDict=[{'level':logging.CRITICAL,'name':'Critical'},
               {'level':logging.DEBUG,'name':'Debug'},
               {'level':logging.INFO,'name':'Info'},
               {'level':logging.WARNING,'name':'Warning'},
               {'level':logging.ERROR,'name':'Error'}]
    setFlag=False
    for entry in levelDict:
        if entry['name']==level:
            diff.setLogLevel(entry['level'])
            setFlag=True
    if setFlag==False:
        diff.logger.info('Logging level '+str(level)+' not found')
        raise ValueError('Logging level '+str(level)+' not found')
    
    
    
def hardware():
    hw=diff.getHardwareInstance()
    hw.position=diff.getAngleValues()
    print hw

def getPV():
    for entry in diff.getangleList():
        print entry.getName()+str(':')+entry.getPV()


def get_low_limit(name):
    '''
    Usage: 
        get_low_limit(name=Angle)
    Returns the low limit for a specific angle.
    '''
    hw=diff.getHardwareInstance()
    print hw.get_lower_limit(name)

def set_low_limit(name,value):
    hw=diff.getHardwareInstance()
    hw.set_lower_limit(name, value)

def set_high_limit(name,value):
    hw=diff.getHardwareInstance()
    hw.set_upper_limit(name, value)

def get_high_limit(name):
    hw=diff.getHardwareInstance()
    hw.get_upper_limit(name)

def energy(value=None):
    hw=diff.getHardwareInstance()
    if value==None:
        en=hw.get_energy()
        print en
        return en
    else:
        hw.energy=value

def wavelength(value=None):
    '''wavelength(value=None)-- sets the wavelength for the reciprocal space calculations '''
    #need to link it to the hardware??????
    hw=diff.getHardwareInstance()
    if value==None:
        print hw.get_wavelength()
    else:
        hw.wavelength=value
def setu(U=None):
    """
    setu {((,,),(,,),(,,))} -- manually set u matrix
    """
    dc=diff.getDCInstance()
    dc.ub.setu(U)

def setub(UB=None):
    """setub {((,,),(,,),(,,))} -- manually set ub matrix"""
    dc=diff.getDCInstance()
    dc.ub.setub(UB)
    
def setName(name):
    '''setName--sets the diffractometer configuration name. '''
    diff.setName(name)

def getName():
    diffName=diff.getName()
    print diffName
    return diffName

def getEngine():
    print diff.getEngine()
    return diff.getEngine()

def setEngine(engine):
    diff.setEngine(engine)

def getAuthor():
    print diff.getAuthor()
    return diff.getAuthor()

def setAuthor(author):
    diff.setAuthor(str(author))
    
def position(**args):
    '''
    Users can define their own angle-value pair dictionaries.The motors will be moved to these positions 
    if the defined positions are within motors' hardware limits
    Usage:
        position({'angle#1':value1,'angle2':value2,...})
    '''
    hw=diff.getHardware()
    if len(args)==0:
        i=0
        while i<len(diff.getAngleNames()):
            print str(diff.getAngleNames()[i])+': '+str(diff.getAngleValues()[i])
            i+=1
    else:
        pvList=list()
        posList=list()
        print args
        for entry in diff.getangleList():
            if entry.getName() in args:
                pvList.append(entry.getPV())
                posList.append(args[entry.getName()])
        if len(posList)!=0:
            caput(pvList,posList)
        print diff.getAngleValues()
        print hw
        hw.position=diff.getAngleValues()
        
def move(angle,position):
    '''
    Move a single motor to a user designated location. For multiple motors, one can 
    write their own custom macros by utilizing position() or move().
    Position is suggested if user defined motion involves several motors moving 
    in a coherent fashion.Unlike mainstream beamline hardware motion control
    and XRay diffraction experiment software, this tool allows user to move 
    multiple motors simulatenously. Users can also use this python scripting environment
    in order to control other hardware alongside motors also simulatenously. 
    Usage:
        move(angle,position)
    '''
    hw=diff.getHardware()
    if angle in diff.getAngleNames():
        for entry in diff.getangleList():
            if entry.getName()==angle:
                entry.setValue(position)
    hw.position=diff.getAngleValues()

def newub(name=None):
    """newub {'name'} -- start a new ub calculation name
    """
    dc=diff.getDCInstance()
    dc.ub.newub(name)
       
def setlat(name=None, *args):
    """
        setlat  -- interactively enter lattice parameters (Angstroms and Deg)
        setlat name a -- assumes cubic
        setlat name a b -- assumes tetragonal
        setlat name a b c -- assumes ortho
        setlat name a b c gamma -- assumes mon/hex with gam not equal to 90
        setlat name a b c alpha beta gamma -- arbitrary
    """
    dc=diff.getDCInstance()
    dc.ub.setlat(name,*args)

def listub():  
    """listub -- list the ub calculations available to load.
    """      
    dc=diff.getDCInstance()
    dc.ub.listub()

def loadub(name_or_num):
    """loadub {'name'|num} -- load an existing ub calculation
    """
    dc=diff.getDCInstance()    
    dc.ub.loadub(name_or_num)

def c2th(hkl,en=None):
    """
    c2th [h k l]  -- calculate two-theta angle for reflection
    """
    dc=diff.getDCInstance()
    print dc.ub.c2th(hkl,en=None)

def showref():
    """showref -- shows full reflection list"""
    dc=diff.getDCInstance()
    dc.ub.showref()
    
def addref(*args):
    """
    addref -- add reflection interactively
    addref [h k l] {'tag'} -- add reflection with current position and energy
    addref [h k l] (p1,p2...pN) energy {'tag'} -- add arbitrary reflection
    """
    dc=diff.getDCInstance()
    dc.ub.addref(*args)
def ub():
    """ub -- show the complete state of the ub calculation
    """
    dc=diff.getDCInstance()
    dc.ub.ub()
    
def where():
    '''
    where()--Returns the all the motor positions and current hkl coordinates
    '''
    pos=diff.getangleList()
    print 'Motor Positions'
    for p in pos:
        temp=str(p.getName())+":"+str(p.getValue())+' degrees'
        print temp
    print 'HKL=',diff.getHKL()

def checkub():
    """checkub -- show calculated and entered hkl values for reflections.
    """
    dc=diff.getDCInstance()
    dc.checkub()

def con(*args):
    """
        con -- list available constraints and values
        con <name> {val} -- constrains and optionally sets one constraint
        con <name> {val} <name> {val} <name> {val} -- clears and then fully constrains

        Select three constraints using 'con' and 'uncon'. Choose up to one
        from each of the sample and detector columns and up to three from
        the sample column.

        Not all constraint combinations are currently available:

            1 x samp:              all 80 of 80
            2 x samp and 1 x ref:  chi & phi
                                   mu & eta
                                   chi=90 & mu=0 (2.5 of 6)
            2 x samp and 1 x det:  0 of 6
            3 x samp:              eta, chi & phi (1 of 4)

        See also 'uncon'
    """
    dc=diff.getDCInstance()
    dc.hkl.con(*args)

def angles_to_hkl(angleTuple, energy=None):
    """Converts a set of diffractometer angles to an hkl position
    Usage:
       ((h, k, l), paramDict)=angles_to_hkl(self, (a1, a2,aN), energy=None)
    """
    dc=diff.getDCInstance()
    print dc.angles_to_hkl(angleTuple,energy)
    
def hkl_to_angles(h,k,l,energy):
    """Convert a given hkl vector to a set of diffractometer angles"""
    dc=diff.getDCInstance()
    print dc.hkl_to_angles(h, k, l, energy)
    
def allhkl(hkl,wavelength=None):
    """allhkl [h k l] -- print all hkl solutions ignoring limits
    """
    dc=diff.getDCInstance()
    dc.hkl.allhkl(hkl,wavelength)

def saveubas(name):
    """saveubas 'name' -- save the ub calculation with a new name
    """
    dc=diff.getDCInstance()
    dc.ub.saveubas(name)
 
def sigtau(sigma=None,tau=None):
    dc=diff.getDCInstance()
    dc.ub.sigtau(sigma,tau)

def editref(num):
    """editref num -- interactively edit a reflection.
    """
    dc=diff.getDCInstance()
    dc.ub.editref(num)

def delref(num):
    """delref num -- deletes a reflection (numbered from 1)
    """
    dc=diff.getDCInstance()

def swapref(num1=None, num2=None):
    """swapref -- swaps first two reflections used for calulating U matrix
       swapref num1 num2 -- swaps two reflections (numbered from 1)
    """
    dc=diff.getDCInstance()
    dc.ub.swap_reflections(num1,num2)

def trialub():
    """trialub -- (re)calculate u matrix from ref1 only (check carefully).
    """
    dc=diff.getDCInstance()
    dc.ub.getDCInstance()

# 
# position()

# hardware()
# # setAngles(angles=['delta','eta','chi','mu','maldini','nedved'])
# # move('delta',0)
# # con('qaz',0)
# # con('a_eq_b')
# # con('mu',0)
# # hardware()
# allhkl([1,1,0])
