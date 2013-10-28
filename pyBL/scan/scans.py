'''
Created on Oct 18, 2013

@author: arkilic
'''
# import time
from trajectory import *
from commands import *


def scan_hkl(h, k, l, stepsize):
    """
    Given hkl coordinates and resolution, scan_hkl() performs scan in reciprocal space. h,k,l values can be single values(i.e. 0,1,1.3,..) as well as python Lists with start and end points [1,2]
    The resolution denotes the intervals scan is performed across. For given h=[1,2] and stepsize=0.2 scan will be performed across 1,1.2,1.4,...,2
    For each trajectory, a checkTrajectory(Trajectory=,Steps=) routine is called in order to make sure calculated values are valid.Users also have access to this function. Once generateTrajectory() is called, one can call checkTraj() in order to make sure calculations are correct. This is quite useful for complex coordinates and crystal orientations
    """
    trajectory = genTraj(hCoordinates=h, kCoordinates=k, lCoordinates=l, resolution=stepsize)
    trajList = trajectory[0]
    hklList = trajectory[1]
    motorDict = dict()
    angleNames = getAngleNames()
    i = 0
    while i < len(trajList):
        diff._hkl = [hklList['h'][i],
                     hklList['k'][i],
                     hklList['l'][i]]
        t = trajList[i][0]
        print hklList['h'][i],hklList['k'][i],hklList['l'][i]
        print t
        checkTraj(Trajectory=t,Steps=[hklList['h'][i],hklList['k'][i],hklList['l'][i]])
        j = 0
        while j < len(t):
            motorDict[angleNames[j]] = t[j]
            j += 1

        moveMultiple(motors=motorDict)
        i += 1

#TODO:implement go_to_hkl

def go_to_hkl(h,k,l):
    motorDict=dict()
    trajectory=genTraj(h,k,l,1)
    motors=trajectory[0]
    rcoordinates=trajectory[1]
    angleNames = getAngleNames()
    print motors[0][0]
    print angleNames
    j = 0
    while j <len(motors[0][0]):
        motorDict[angleNames[j]] = motors[0][0][j]
        j += 1
    print motorDict
    moveMultiple(motorDict)




