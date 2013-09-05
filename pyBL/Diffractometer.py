'''
#Created on Aug 9, 2013
# @author: Arman Arkilic                                                                                                       #
#          Brookhaven National Laboratory                                                                                      #
#          Upton, NY 11973                                                                                                     #
#                                                                                                                              #              
#     Diffractometer and hardware used for XRAY Diffraction experiments are treated                                            #
#     as objects as each beam line hardware has different configuration and needs.                                             #
#     DiffEpics allows beamline scientists/users to make changes on existing                                                   #
#     configuration or come up with new configurations based on their needs using this scheme.                                 #
#                                                                                                                              #
#     DiffCalc (by Rob Walton-Diamond Light Source) is the heart of the reciprocal space                                       #
#     calculation engine. In this application, it is completely stripped off from OpenGDA based on user input                  #
#     and programmer preference most importantly for better hardware control.                                                  #
#                                                                                                                              #  
#     As of DiffEpics v0.1:                                                                                                    #
#         Diffcalc core calculation code works with a six-circle geometry.                                                     #
#         It supports four-circle modes, where two circles are fixed, five-circle modes, where                                 #
#         one circle is fixed and the last is used to keep the surface normal in the horizontal lab plane,                     #    
#         and six-circle modes where the surface normal is kept parallel to the omega (theta) axis.                            # 
#         For each of these there are five variants: the angle of the incoming or outgoing beam to the                         #
#         crystal surface can be fixed the incoming and outgoing angles can be made equal, phi can be fixed,                   #  
#         or the azimuthal angle about the momentum-transfer vector can be fixed.                                              #       
#          The azimuthal variants still need some testing and likely development.                                              #
#                                                                                                                              # 
#     DiffCalc does not directly move motors. It is only a reciprocal space calculator.                                        #         
#     For motor motion, see DiffScan. DiffScan allows DiffEpics to communicate with the hardware                               #
#     using EPICS IOC and EPICS asyn driver. Flexible nature of EPICS applications allows users to add                         #
#     custom hardware on their own.                                                                                            #        
#                                                                                                                              #            
#     EPICS also allows complete control of beamline hardware(such as power supplies,                                          #
#     monochromators, etc...) through Python scripts(as this hardware can also be controlled using EPICS IOC and asyn).        #
#                                                                                                                              #
#     For more information on DiffCalc, EPICS IOC and asynDriver:                                                              #  
#                                                                                                                              #
#         http://www.opengda.org/downloads/gda/v8.4/DiffcalcGuide_html/user/manual.html                                        #
#                                                                                                                              #
#         http://www.aps.anl.gov/epics/base/R3-14/7-docs/AppDevGuide.pdf                                                       #
#                                                                                                                              #      
#         http://www.aps.anl.gov/epics/modules/soft/asyn/                                                                      #          
'''
from diffcalc.hkl.you.geometry import SixCircle,FourCircle
from diffcalc.hardware import DummyHardwareAdapter,HardwareAdapter
from diffcalc.diffcalc_ import create_diffcalc
from cothread.catools import caput,caget,connect
import logging
from distutils import errors
from os import path
# from pyBL.olog import ologTag

class Diffractometer(object):
    
    def __init__(self,name,geometry,engine,tag,author):
        
        self._name=name
        self._geometry=geometry
        self._engine=engine
        self._tag=tag
        self._author=author
        self._angleList=list()
        self._diffractometer=None
        self._hardware=None
        self._hkl=[0,0,0]
        self.pvList=['test:mtr1',
                    'test:mtr2',
                    'test:mtr3',
                    'test:mtr4',
                    'test:mtr5',
                    'test:mtr6']
        self.defaultAngleParam={'value':0,
                           'geometry':SixCircle(),
                           'positiveLimit':180,
                           'negativeLimit':-180}  
        self.logger = logging.getLogger('Diffractometer')
        hdlr = logging.FileHandler(path.expanduser('~/diffractometer.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)
        self.ologClient='default'     
#         self.ologTag=ologTag
#         self.ologLogbook='default logbook'
#         self.ologProp='empty prop'
        
    def setClient(self,client):
        self.ologClient=client
    
    def getClient(self):
        return self.ologClient
    
    def getName(self):
        return self._name
    
    def getGeometry(self):
        return self._geometry
    
    def getEngine(self):
        return self._engine
    
    def getDCInstance(self): 
        return self._diffractometer
    
    def getTag(self):
        return self._tag
    
    def getAuthor(self):
        return self._author
    
    def getangleList(self):
        return self._angleList 
    
    def setLogLevel(self,level):
        self.logger.setLevel(level)
    
    def getLogLevel(self):
        return self.logger.getEffectiveLevel()
    
    def getPVList(self):
        return self.pvList
       
    def getHKL(self):
        return self._hkl
    
    def setHKL(self,hkl):
        if len(hkl)==3:
            self._hkl=hkl
            self.logger.info("New HKL coordinates are set: "+str(hkl))
        else:
            self.logger.warning('Invalid HKL coordinates:'+str(hkl))
            raise ValueError('Invalid HKL coordinates')
        
    def setName(self,name):
        self._name=name 
        self.logger.info('Diffractometer Name set:'+str(self._name))
        
    def setEngine(self,engine):
        '''
        Sets the engine used in diffraction experiment. This engine is used in reciprocal space
        calculations through diffcalc. 
        Supported engines: YOU, WILLMOTT,VLIEG
        '''
        engineList=['you','willmott','vlieg']
        if engine in engineList:
            self._engine=engine
            self.logger.info('Reciprocal space calculation engine selected:'+self._engine)
        else:
            self.logger.info('Invalid engine name')
            raise ValueError('Invalid engine name')
        
    def setTag(self,tag):
        self._tag=tag
        
    def setAuthor(self,author):
        self._author=author
    
    def setangleList(self,angleList):
        self._angleList=angleList
    
    def getAngleNames(self):
        '''
            Returns a list of Angle instances that includes all the angles associated with a given diffractometer
            angleList is updated after every operation that changes motor positions. 
        '''
        temp=list()
        for angle in self._angleList:
            temp.append(angle.getName())
        return temp
    
    def getAngleValues(self):
        '''
            Returns a list of Angle values. These values are read from the EPICS motor record
            and always refer to actual motor position readings.
        '''
        temp=list()
        for angle in self._angleList:
            temp.append(angle.getValue())
        return temp
    
    def getHardware(self):
        '''
            Returns the hardware used for reciprocal space calculations. This is strictly for diffcalc,
            however,Angle names and Angle values are completely in coherence with userAPI. 
        '''
        return self._hardware   
    
    def setGeometry(self,geometry):
        '''
            Sets a diffractometer's geometry. This geometry is used for both motor control and
            and reciprocal space calculations. 
        '''
        geometryList={'SixCircle':SixCircle(),
                      'sixcircle':SixCircle(),
                      'fourcircle':FourCircle(),
                      'FourCircle':FourCircle()
                      }
        if geometry in geometryList:
            self._geometry=geometryList[geometry]
            self.logger.info("Diffractometer geometry selected: "+geometry) 
        else:
            self.logger.info('Geometry not Supported:'+geometry)
            raise ValueError('Geometry not Supported: '+geometry)
        
    def setHardwareAdapter(self,hardwareAdapter):
        '''
        Sets up a hardware adapter for DiffCalc calculations.
        Available adapters:
            DummyHardwareAdapter(diffractometerAngleNames)
            
            HardwareAdapter(diffractometerAngleNames, 
                          defaultCuts={}, 
                          energyScannableMultiplierToGetKeV=1)
        '''
        adapterList={'DummyHardwareAdapter',"HardwareAdapter"}
        if hardwareAdapter in adapterList:
            self._hardwareAdapter=hardwareAdapter
            self.logger.info('DiffCalc Hardware Adapter Selected:'+hardwareAdapter)
            if self._hardwareAdapter=="DummyHardwareAdapter":
                self._hardware=DummyHardwareAdapter(self.getAngleNames())
                self.logger.info('DiffCalc Hardware Adapter Selected:'+hardwareAdapter)
            elif self._hardwareAdapter=="HardwareAdapter":
                self._hardware=HardwareAdapter(diffractometer=self,
                                              defaultCuts={}, 
                                              energyScannableMultiplierToGetKeV=1.5)
                self.logger.info('DiffCalc Hardware Adapter Selected:'+hardwareAdapter)
        else:
            self.logger.info('Error defining the hardware adapter for object'+str(self._name))
            raise ValueError("The hardware adapter not defined. Please see diffcalc documentation.")
        self._hardware.position=self.getAngleValues()
        
    def getHardwareAdapter(self):
        return self._hardware
    
    def createAngles(self,angle,Geometry):
        '''
            Creates Angle instances for a hardware.Each angle instance is created and manipulated
            separately. The user has complete control of each circle of a diffractometer. 
        '''
        self._angleList.append(Angle(name=angle,
                                     value=self.defaultAngleParam['value'],
                                     geometry=Geometry,
                                     positiveLimit=self.defaultAngleParam['positiveLimit'],
                                     negativeLimit=self.defaultAngleParam['negativeLimit'],
                                     author=self._author))
        self.logger.info('Diffractometer Angle Instances created with defeault values')
        
    def setAnglesforHardware(self,angleList,Geometry):
        '''
            Creates Angle instances for a user defined diffractometer. These angles are going to be used while setting up 
            a diffractometer as well as during hardware motion control. 
            Each angle instance is assigned to a motor, which provides a coherent structure making it simple to generate 
            custom geometries for beamline scientists. This also makes it possible to construct a hardware independent
            configuration that is easy to maintain.
        '''
        sixAngleList=['mu','theta','gam','delta','chi','phi']   
        fourAngleList=['mu','theta','gam','delta']                          
        geometryList=['SixCircle','FourCircle','sixcircle','fourcircle']
        if len(self._angleList)==0:
            if Geometry in geometryList:
                if len(angleList)==6 or len(angleList)==4 :
                    for entry in angleList:
                        self._angleList.append(Angle(name=entry,
                                               value=self.defaultAngleParam['value'],
                                               geometry=Geometry,
                                               positiveLimit=self.defaultAngleParam['positiveLimit'],
                                               negativeLimit=self.defaultAngleParam['negativeLimit'],
                                               author=self._author))
                elif len(angleList)==0:
                    if Geometry=='SixCircle' or Geometry=='sixcircle':
                        for angle in sixAngleList:
                            self._angleList.append(Angle(name=angle,
                                                   value=self.defaultAngleParam['value'],
                                                   geometry=Geometry,
                                                   positiveLimit=self.defaultAngleParam['positiveLimit'],
                                                   negativeLimit=self.defaultAngleParam['negativeLimit'],
                                                   author=self._author))
                    elif Geometry=='FourCircle' or Geometry=='fourcircle':
                        for angle in fourAngleList:
                            self._angleList.append(Angle(name=angle,
                                                        value=self.defaultAngleParam['value'],
                                                        geometry=Geometry,
                                                        positiveLimit=self.defaultAngleParam['positiveLimit'],
                                                        negativeLimit=self.defaultAngleParam['negativeLimit'],
                                                        author=self._author))
                else:
                    self.logger.info("Enter the correct number of angles for the given geometry")
                    raise ValueError("Enter the correct number of angles for the given geometry")
            else:
                self.logger.info("Not a valid geometry: "+str(Geometry))
                raise ValueError('Not a valid geometry '+str(Geometry))
        else:
            self._angleList=list()
            if self._geometry.name=='sixc':
                if len(angleList)==6:
                    for item in angleList:
                        self.createAngles(item,self._geometry.name)
                else:
                    self.logger.info('Invalid number of circles.Given '+str(len(angleList))+' required 6')
                    raise ValueError('Invalid number of circles.Given '+str(len(angleList))+' required 6')
            elif self._geometry.name=='fourc':
                if len(angleList)==4:
                    for item in angleList:
                        self.createAngles(item,self._geometry.name)
                else:
                    self.logger.info('Invalid number of circles.Given '+str(len(angleList))+' required 4')
                    raise ValueError('Invalid number of circles.Given '+str(len(angleList))+' required 4')
                    
        i=0         
        for entry in self._angleList:
            entry.setPV(self.pvList[i])
            i+=1
        self.logger.info('PVs assigned to Angle instances')    
    
    def basicSetup(self,hardwareAdapter,**params):
        
        '''
        Sets up a basic diffractometer with default values. These values can be changed by using native functions such as
        someAngle.setName(),someAngle.setpositive () can be used. If this is not the preference as this requires setting up too many parameters,
        diffcalc.config.advancedSetup() provides a cleaner/more organized way to set up a custom diffractometer by utilizing dictionaries.
        self.engine=engine   
        self.tag='Basic diffractometer configuration'
        self.author='default'
        self.defaultAngleParam={'value':0,
                           'geometry':SixCircle(),
                           'positiveLimit':180,
                           'negativeLimit':-180}    
        parameterList={'angles','geometry'}
        
        '''
        self._tag='Basic diffractometer configuration'
        parameterList={'angles','geometry'}
        self.defaultAngleParam={'value':0,
                           'geometry':SixCircle(),
                           'positiveLimit':180,
                           'negativeLimit':-180}    
        for param in params:          
            if param not in parameterList:
                self.logger.info('Parameter "'+ str(param)+'" not supported by reciprocalSetup()')
                raise ValueError('Parameter "'+ str(param)+'" not supported by reciprocalSetup()')
            
        if 'angles' not in params:
            if self._geometry=='SixCircle':
                angleList={'mu','theta','gam','delta','chi','phi'}
            else:
                angleList={'mu','theta','gam','delta'}
        else:
            angleList=params['angles']
        if 'geometry' in params:
            self._geometry=params['geometry']
        if self._geometry=='SixCircle' or self._geometry=='FourCircle':
            if self._geometry=='SixCircle':
                self._geometry=SixCircle()
            else:
                self._geometry=FourCircle()
        else:
            self.logger.info('Please enter a valid geometry')
            raise ValueError('Please enter a valid geometry')
        
        
        self.setAnglesforHardware(angleList)
        self.setHardwareAdapter(hardwareAdapter)
        self._diffractometer=create_diffcalc(engine_name=self._engine, geometry=self._geometry, hardware=self._hardware)

    def returnInstanceList(self):
            return list(self.instances)
    
    def setDCInstance(self):
        '''
        To be modified as the hardware adapter is initiated
        '''
        self._diffractometer=create_diffcalc(str(self._engine), geometry=self._geometry,hardware=self._hardware) 
        self.logger.info('DiffCalc diffractometer instance created')
        
    def getHardwareInstance(self):
        return self._hardware
        
    def dummySetup(self,name,geometry,engine,tag,author):
        self.setName(name)
        self.setEngine(engine=engine)
        self.setGeometry(geometry)
        self.setTag(tag)
        self.setAuthor(author)
        self.setAnglesforHardware(angleList=self.getangleList(),Geometry=geometry)
        self.setHardwareAdapter(hardwareAdapter='DummyHardwareAdapter')
        self._diffractometer=create_diffcalc(engine, geometry=self._geometry,hardware=self._hardware) 
        
class Angle(Diffractometer):
    
    def __init__(self,name,value,geometry,positiveLimit,negativeLimit,author):
        self._name=name
        self._value=value
        self._geometry=geometry
        self._positiveLimit=positiveLimit
        self._negativeLimit=negativeLimit
        self._author=author
        self._pv=' '
        self.logger = logging.getLogger('Angle')
        ahdlr = logging.FileHandler(path.expanduser('~/angle.log'))
        aformatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        ahdlr.setFormatter(aformatter)
        self.logger.addHandler(ahdlr) 
        self.logger.setLevel(logging.INFO)
        
    def setPV(self,PV):
           
        if connect(PV,wait=False,cainfo=True).state==2:
            self._pv=PV
        else:
            self._pv='dummy'

    def getPV(self):
        if self._pv=='dummy':
            return self._pv
        else:
            try:
                caget(str(self._pv))
                return self._pv
            except:
                self.logger.error('Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')
                raise Warning('Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')
        
    def getValue(self):
        if self._pv=='dummy':
            self._value='Disconnect'
            return self._value
        else:
            self._value=caget(self._pv)
            return self._value
# 
#                 self.logger.error('Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')
#                 raise Warning('Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')
            
    def setValue(self,value):
        if self._pv=='dummy':
            self._value='Disconnect'
        else:
            self._value=value
            caput(self._pv,value)
#             except:
#                 self.logger.error('Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')
#                 raise Warning('Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')
#             
def setup(name,geometry,engine,tag,author,*params):
    diff=Diffractometer(name, geometry, engine, tag, author)
    if 'hardwareAdapter' in params:
        if 'angles' in params:
            diff.basicSetup(hardwareAdapter=params['hardwareAdapter'],angles=params['angles'])
        else:
            diff.basicSetup(hardwareAdapter=params['hardwareAdapter'])
    else:
        diff.basicSetup('HardwareAdapter')
        



