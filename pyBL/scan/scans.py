'''
Created on Oct 18, 2013

@author: arkilic
'''
# import time
from trajectory import *
from commands import *
def scan_hkl(h,k,l,stepsize):
    trajectory=genTraj(hCoordinates=h, kCoordinates=k, lCoordinates=l, resolution=stepsize)
    trajList=trajectory[0]
    hklList=trajectory[1]
    motorDict=dict()
    angleNames=getAngleNames()
    i=0
    while i<len(trajList):
        diff._hkl=[hklList['h'][i],
                   hklList['k'][i],
                   hklList['l'][i]]
        t=trajList[i][0]
        j=0
        print t
        while j<len(t):
            motorDict[angleNames[j]]=t[j]
            j+=1   
        print motorDict
        moveMultiple(motors=motorDict)
        i+=1
