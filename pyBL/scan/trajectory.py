'''
Created on Oct 9, 2013

@author: arkilic
'''
from commands import *

def genTraj(hCoordinates,kCoordinates,lCoordinates,resolution ):
    '''
    Returns [(motor positions for given hkl),{azimuthal angles}] and corresponding hkl values
    '''
    temp=list()
    lists=dict()
    hSteps=dict()
    kSteps=dict()
    lSteps=dict()
    maxStepSize=0
    if type(hCoordinates) is list:
        lists['h']=hCoordinates
    else:
        lists['h']=[hCoordinates]
    if type(kCoordinates) is list:
        lists['k']=kCoordinates
    else:
        lists['k']=[kCoordinates]
    if type(lCoordinates) is list:
        lists['l']=kCoordinates
    else:
        lists['l']=[lCoordinates]
    h=lists['h']
    k=lists['k']
    l=lists['l']
    maxStepSize=max((h[-1]-h[0])/resolution,
                (k[-1]-k[0])/resolution,
                (l[-1]-l[0])/resolution)
    if getUBFlag()==False:
        raise Warning('No UB Calculation in progress. Please use newub() or loadub()')
    else:
        print 'else',maxStepSize
        if getRefFlag()==True:
            if type(hCoordinates) is list:
                hSteps=detSingleInterval(coordinateName='h', initial=hCoordinates[0], final=hCoordinates[-1], step=resolution)
            else:
                h_temp=lists['h']*int((round(maxStepSize)+1))
                hSteps={'h':h_temp}            
            if type(kCoordinates) is list:
                kSteps=detSingleInterval(coordinateName='k', initial=kCoordinates[0], final=kCoordinates[-1], step=resolution)
            else:
                k_temp=lists['k']*int((round(maxStepSize)+1))
                kSteps={'k':k_temp}
            if type(lCoordinates) is list:
                lSteps=detSingleInterval(coordinateName='l', initial=lCoordinates[0], final=lCoordinates[-1], step=resolution)
            else:
                l_temp=lists['l']*int((round(maxStepSize)+1))
                lSteps={'l':l_temp}
            steps=dict(hSteps.items()+kSteps.items()+lSteps.items())
            i=0
            while i<len(steps['h']):
                temp.append(hkl_to_angles(h=steps['h'][i], k=steps['k'][i], l=steps['l'][i], energy=energy()))
                i+=1
                if len(steps['h'])!=len(steps['k']) or len(steps['k'])!=len(steps['l']):
                    raise Exception('Please enter identical intervals')
        else:
            raise Warning('No reflection added.Please use addref() to add a reflection for your crystal')
    return temp,steps

def detSingleInterval(coordinateName,initial,final,step):
    currentStep=float(initial)
    trajList={coordinateName:[]}
    trajList[coordinateName].append(currentStep)
    while currentStep<final:
        currentStep=float(currentStep)+float(step)
        trajList[coordinateName].append(currentStep)
    return trajList

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
genTraj(hCoordinates=[1,1.3],kCoordinates=0,lCoordinates=0,resolution=0.1)
ls
'''