'''
Created on Oct 9, 2013

@author: arkilic
'''
#from Config import diff
from commands import *
def genTraj(hCoordinates,kCoordinates,lCoordinates,resolution ):
    temp=list()
    maximum=max((hCoordinates[-1]-hCoordinates[0])/resolution,
                (kCoordinates[-1]-kCoordinates[0])/resolution,
                (lCoordinates[-1]-lCoordinates[0])/resolution)
    if getUBFlag()==False:
        raise Warning('No UB Calculation in progress. Please use newub() or loadub()')
    else:
        if getRefFlag()==True:
            blankList=[0]*len(maximum)
            
            if hCoordinates!=0:
                hSteps=detSingleInterval(coordinateName='h', initial=hCoordinates[0], final=hCoordinates[-1], step=resolution)
            else:
                hSteps={'h':blankList}
                
            if kCoordinates!=0:
                kSteps=detSingleInterval(coordinateName='k', initial=kCoordinates[0], final=kCoordinates[-1], step=resolution)
            else:
                kSteps={'k':blankList}
                
            if lCoordinates!=0:
                lSteps=detSingleInterval(coordinateName='l', initial=lCoordinates[0], final=lCoordinates[-1], step=resolution)
            else:
                lSteps={'l':blankList}
            steps=dict(hSteps.items()+kSteps.items()+lSteps.items())
            print steps
            i=0
            while i<len(steps['h']):
                print steps['h'][i]
                temp.append(hkl_to_angles(h=steps['h'][i], k=steps['k'][i], l=steps['l'][i], energy=energy()))
                i+=1
        else:
            raise Warning('No reflection added.Please use addref() to add a reflection for your crystal')

def detSingleInterval(coordinateName,initial,final,step):
    currentStep=initial
    
    trajList={coordinateName:[]}
    while currentStep<=final:
        currentStep=float(currentStep)+float(step)
        trajList[coordinateName].append(currentStep)
    return trajList

def detMultTraj(coordinateNames):
    pass
def checkTraj(trajectoryList):
    pass

#genTraj(hCoordinates=[1,1.3],kCoordinates=0,lCoordinates=0,resolution=0.1)
'''
setAngles(['mu','delta','gam','eta','chi','phi'])
newub('test_')
setlat('cubic',1,1,1,90,90,90)
c2th([1,0,0])
position(mu=0,delta=60,=0,eta=30,chi=0,phi=0)
addref([1,0,0])
addref([0,1,0],[0,60,0,30,0,90],energy())
ub()
angles_to_hkl((0.,60.,0.,30.,0.,0.))
con('gam',0)
con('a_eq_b')
con('mu',0)
con()
set_low_limit('delta',0)
hkl_to_angles(1,0,0,energy())
ls
'''