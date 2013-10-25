'''
Diffractometer and hardware used for XRAY Diffraction experiments are treated as objects with multiple attributes by this code.As a result, diffractometer objects are customizable for each beamline/user. DiffCalc (by Rob Walton-Diamond Light Source) is the heart of the reciprocal space calculation engine and in order to perform reciprocal space calculations, this software creates custom diffractometer and hardware-dependent instances and maps the attributes of these instances (axis names, motor positions, limits, etc...) to DiffCalc objects. In other words, this code uses DiffCalc API without wrapping DiffCalc code, leaving DiffCalc standalone for future updates.

**As of v0.1:**

As Diffcalc documentation also states, DiffCalc core calculation code works with a six-circle geometry.It supports four-circle modes, where two circles are fixed @ zero, five-circle modes, where one circle is fixed and the last is used to keep surface normal in the horizontal lab plane,and six-circle modes where the surface normal is kept parallel to the omega (theta) axis.For each of these there are five variants: the angle of the incoming or outgoing beam to the crystal surface can be fixed the incoming and outgoing angles can be made equal, phi can be fixed,or the azimuthal angle about the momentum-transfer vector can be fixed.The azimuthal variants still need some testing and likely development.                                       
DiffCalc does not directly move motors. It is only a reciprocal space calculator. Hardware motion is provided through this software(via EPICS services). Angles stand for the axes(circles) of the diffractometer.EPICS Process Variables(PVs) are assigned to angle instances.These PVs are provided by EPICS IOC and EPICS asyn driver.For more details on this, please check EPICS motor record documentation(http://www.aps.anl.gov/bcda/synApps/motor/). Flexible nature of EPICS applications allows users to add custom hardware on their own,making this software a multi-hardware-platform application.
'''
from diffcalc.hkl.you.geometry import SixCircle, FourCircle
from diffcalc.hardware import DummyHardwareAdapter, HardwareAdapter
from diffcalc.diffcalc_ import create_diffcalc
from cothread.catools import caput, caget, connect
from logConfig import logInstance


class Diffractometer(object):
    '''
    Constructor-Name, tag, author, angle list(axes names) are chosen by the user based on their preferences or standards. Diffractometer expects to get either FourCircle or SixCircle options as geometry. There are 3 engines supported by this software: 'you', 'vlieg', 'willmott'. The latest and fastest of the three is 'you', however, users can choose one engine over another based on their application. Hardware attribute is a placeholder for DiffCalc Hardware Adapter. As of this version, this software utilizes DummyHardwareAdapter. However, in the future versions, this will be replaced with a custom HardwareAdapter instance as we will determine preferences and standards in NSLS2 XRay Diffraction Beamline
    '''

    def __init__(self, name, geometry, engine, tag, author):
        self._name = name
        self._geometry = geometry
        self._engine = engine
        self._tag = tag
        self._author = author
        self._angleList = list()
        self._diffractometer = None
        self._hardware = None
        self._hkl = [0, 0, 0]
        self._calcFlag = False
        self._refFlag = False
        self._ubFlag = False
        print 'i am at const'
        self.pvList = ['test:mtr1',
                       'test:mtr2',
                       'test:mtr3',
                       'test:mtr4',
                       'test:mtr5',
                       'test:mtr6']
        self.defaultAngleParam = {'value': 0,
                                  'geometry': SixCircle(),
                                  'positiveLimit': 180,
                                  'negativeLimit': -180}

    def setUBFlag(self):
        self._ubFlag = True

    def getUBFlag(self):
        return self._ubFlag

    def setRefFlag(self):
        self._refFlag = True

    def getRefFlag(self):
        return self._refFlag

    def getName(self):
        '''
        Returns the diffractometer configuration name. This can be used to identify a specific configuration of a diffractometer as this attribute is accessed directly through the configuration file
        '''
        return self._name

    def getGeometry(self):
        '''
         Returns diffractometer geometry in string format. The reason behind this is to simplify geometry selection for the user through configuration file. For a custom reciprocal space calculation or geometry, a developer should create custom geometries inside DiffCalc(see DiffCalc Developer Manual) and call these geometries via Diffractometer.setGeometry(). Developer also needs to assure that proper number of motors(Angle instances) are created via Config.py. 
        '''
        return self._geometry

    def getEngine(self):
        '''
        Returns DiffCalc calculation engine used in order to notify the user. This makes it possible to write applications that use different calculation engines based on different papers(you,vlieg,willmott) and compare recirporcal space/motor positions.
        '''
        return self._engine

    def getDCInstance(self):
        '''
            Returns the DiffCalc instance that a a specific Diffractometer is mapped onto. By using this DiffCalc object, developers can write custom applications that deal directly with DiffCalc objects. This is useful once a custom diffcalc functionality is written inside diffcalc, as it is done under commands.py, developer can create a function under this API that is directly linked to the custom diffcalc function.
        '''
        return self._diffractometer

    def getTag(self):
        '''
        Returns Diffractometer Tag. This should not be confused with Olog Tags. This can be identical to Olog tag, however, this tag does not directly map onto Olog tag of pyOlog.conf.
        '''
        return self._tag

    def getAuthor(self):
        '''
        Returns the author of the Diffractometer configuration.
        '''
        return self._author

    def getCalcFlag(self):
        return self._calcFlag

    def getangleList(self):
        '''
        Returns a list of Angle Instances that refer to the circles of the diffractometer. These objects also map onto DiffCalc "scannables". 
        '''
        return self._angleList

    def setLogLevel(self, level):
        logInstance.logger.setLevel(level)

    def getLogLevel(self):
        return logInstance.logger.getEffectiveLevel()

    def getPVList(self):
        return self.pvList

    def getHKL(self):
        return self._hkl

    def setHKL(self, hkl):
        if len(hkl) == 3:
            self._hkl = hkl
            logInstance.logger.info("New HKL coordinates are set: " + str(hkl))
        else:
            logInstance.logger.warning('Invalid HKL coordinates:' + str(hkl))
            raise ValueError('Invalid HKL coordinates')

    def setName(self, name):
        self._name = name
        logInstance.logger.info('Diffractometer Name set:' + str(self._name))

    def setEngine(self, engine):
        '''
        Sets the engine used in diffraction experiment. This engine is used in reciprocal space
        calculations through diffcalc.
        Supported engines: YOU, WILLMOTT,VLIEG
        '''
        engineList = ['you', 'willmott', 'vlieg']
        if engine in engineList:
            self._engine = engine
            logInstance.logger.info('Reciprocal space calculation engine selected:' + self._engine)
        else:
            logInstance.logger.info('Invalid engine name')
            raise ValueError('Invalid engine name')

    def setTag(self, tag):
        self._tag = tag

    def setAuthor(self, author):
        self._author = author

    def setangleList(self, angleList):
        self._angleList = angleList

    def getAngleNames(self):
        '''
            Returns a list of Angle instances that includes all the angles associated with a given diffractometer
            angleList is updated after every operation that changes motor positions. 
        '''
        temp = list()
        for angle in self._angleList:
            temp.append(angle.getName())
        return temp

    def getAngleValues(self):
        '''
            Returns a list of Angle values. These values are read from the EPICS motor record
            and always refer to actual motor position readings.
        '''
        temp = list()
        for angle in self._angleList:
            temp.append(angle.getValue())
        return temp

    def getAngleSetPoints(self):

        temp = list()
        for angle in self._angleList:
            temp.append(angle.getSetPoint())
        return temp

    def getHardware(self):
        '''
            Returns the hardware used for reciprocal space calculations. This is strictly for diffcalc,
            however,Angle names and Angle values are completely in coherence with userAPI. 
        '''
        return self._hardware

    def setGeometry(self, geometry):
        '''
            Sets a diffractometer's geometry. This geometry is used for both motor control and
            and reciprocal space calculations. 
        '''
        geometryList = {'SixCircle': SixCircle(),
                        'sixcircle': SixCircle(),
                        'fourcircle': FourCircle(),
                        'FourCircle': FourCircle()
        }
        if geometry in geometryList:
            self._geometry = geometryList[geometry]
            logInstance.logger.info("Diffractometer geometry selected: " + geometry)
        else:
            self.logger.info('Geometry not Supported:' + geometry)
            raise ValueError('Geometry not Supported: ' + geometry)

    def setHardwareAdapter(self, hardwareAdapter):
        '''
        Sets up a hardware adapter for DiffCalc calculations.
        Available adapters:
            DummyHardwareAdapter(diffractometerAngleNames)
            
            HardwareAdapter(diffractometerAngleNames, 
                          defaultCuts={}, 
                          energyScannableMultiplierToGetKeV=1)
        '''
        adapterList = {'DummyHardwareAdapter', "HardwareAdapter"}
        if hardwareAdapter in adapterList:
            self._hardwareAdapter = hardwareAdapter
            logInstance.logger.info('DiffCalc Hardware Adapter Selected:' + hardwareAdapter)
            if self._hardwareAdapter == "DummyHardwareAdapter":
                self._hardware = DummyHardwareAdapter(self.getAngleNames())
                logInstance.logger.info('DiffCalc Hardware Adapter Selected:' + hardwareAdapter)
            elif self._hardwareAdapter == "HardwareAdapter":
                self._hardware = HardwareAdapter(diffractometer=self,
                                                 defaultCuts={},
                                                 energyScannableMultiplierToGetKeV=1.5)
                self.logger.info('DiffCalc Hardware Adapter Selected:' + hardwareAdapter)
        else:
            logInstance.logger.info('Error defining the hardware adapter for object' + str(self._name))
            raise ValueError("The hardware adapter not defined. Please see diffcalc documentation.")
        self._hardware.position = self.getAngleValues()

    def getHardwareAdapter(self):
        return self._hardware

    def createAngles(self, angle, Geometry):
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
        logInstance.logger.info('Diffractometer Angle Instances created with defeault values')

    def setAnglesforHardware(self, angleList, Geometry):
        '''
            Creates Angle instances for a user defined diffractometer. These angles are going to be used fo setting up 
            reciprocal space calculations as well as hardware motion control. 
            Each angle instance is assigned to a motor, which provides a coherent structure making it simple to generate 
            custom geometries for beamline scientists. This also makes it possible to construct a hardware independent
            configuration that is easy to maintain. Default values are:
        sixAngleList=['mu','delta','nu','eta','chi','phi']   
        fourAngleList=['mu','theta','nu','delta']                          
        geometryList=['SixCircle','FourCircle','sixcircle','fourcircle']
            If a developer would like to add a custom geometry or angle list, this portion of the code must be modified. 
            In case of a user, users can initialize their angle lists by using passing a list of angles to setAngles() method through the API.
        '''
        sixAngleList = ['mu', 'delta', 'nu', 'eta', 'chi', 'phi']
        fourAngleList = ['mu', 'theta', 'nu', 'delta']
        geometryList = ['SixCircle', 'FourCircle', 'sixcircle', 'fourcircle']
        if len(self._angleList) == 0:
            if Geometry in geometryList:
                if len(angleList) == 6 or len(angleList) == 4:
                    for entry in angleList:
                        self._angleList.append(Angle(name=entry,
                                                     value=self.defaultAngleParam['value'],
                                                     geometry=Geometry,
                                                     positiveLimit=self.defaultAngleParam['positiveLimit'],
                                                     negativeLimit=self.defaultAngleParam['negativeLimit'],
                                                     author=self._author))
                elif len(angleList) == 0:
                    if Geometry == 'SixCircle' or Geometry == 'sixcircle':
                        for angle in sixAngleList:
                            self._angleList.append(Angle(name=angle,
                                                         value=self.defaultAngleParam['value'],
                                                         geometry=Geometry,
                                                         positiveLimit=self.defaultAngleParam['positiveLimit'],
                                                         negativeLimit=self.defaultAngleParam['negativeLimit'],
                                                         author=self._author))
                    elif Geometry == 'FourCircle' or Geometry == 'fourcircle':
                        for angle in fourAngleList:
                            self._angleList.append(Angle(name=angle,
                                                         value=self.defaultAngleParam['value'],
                                                         geometry=Geometry,
                                                         positiveLimit=self.defaultAngleParam['positiveLimit'],
                                                         negativeLimit=self.defaultAngleParam['negativeLimit'],
                                                         author=self._author))
                else:
                    logInstance.logger.info("Enter the correct number of angles for the given geometry")
                    raise ValueError("Enter the correct number of angles for the given geometry")
            else:
                logInstance.logger.info("Not a valid geometry: " + str(Geometry))
                raise ValueError('Not a valid geometry ' + str(Geometry))
            i = 0
            for entry in self._angleList:
                entry.setPV(self.pvList[i])
                i += 1
            logInstance.logger.info('PVs assigned to Angle instances')
        else:
            #self._angleList=list()
            if self._geometry.name == 'sixc':
                if len(angleList) == 6:
                    i = 0
                    for item in angleList:
                        self._angleList[i].setName(item)
                        i += 1
                        #self.createAngles(item,self._geometry.name)
                else:
                    logInstance.logger.info('Invalid number of circles.Given ' + str(len(angleList)) + ' required 6')
                    raise ValueError('Invalid number of circles.Given ' + str(len(angleList)) + ' required 6')
            elif self._geometry.name == 'fourc':
                if len(angleList) == 4:
                    for item in angleList:
                        self._angleList[i].setName(item)
                        i += 1
                        #self.createAngles(item,self._geometry.name)
                else:
                    logInstance.logger.info('Invalid number of circles.Given ' + str(len(angleList)) + ' required 4')
                    raise ValueError('Invalid number of circles.Given ' + str(len(angleList)) + ' required 4')

                #         i=0
                #         for entry in self._angleList:
                #             entry.setPV(self.pvList[i])
                #             i+=1
                #         logInstance.logger.info('PVs assigned to Angle instances')

    def basicSetup(self, hardwareAdapter, **params):

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
        self._tag = 'Basic diffractometer configuration'
        parameterList = {'angles', 'geometry'}
        self.defaultAngleParam = {'value': 0,
                                  'geometry': SixCircle(),
                                  'positiveLimit': 180,
                                  'negativeLimit': -180}
        for param in params:
            if param not in parameterList:
                logInstance.logger.info('Parameter "' + str(param) + '" not supported by reciprocalSetup()')
                raise ValueError('Parameter "' + str(param) + '" not supported by reciprocalSetup()')

        if 'angles' not in params:
            if self._geometry == 'SixCircle':
                angleList = {'mu', 'delta', 'nu', 'eta', 'chi', 'phi'}
            else:
                angleList = {'mu', 'delta', 'nu', 'eta'}
        else:
            angleList = params['angles']
        if 'geometry' in params:
            self._geometry = params['geometry']
        if self._geometry == 'SixCircle' or self._geometry == 'FourCircle':
            if self._geometry == 'SixCircle':
                self._geometry = SixCircle()
            else:
                self._geometry = FourCircle()
        else:
            logInstance.logger.info('Please enter a valid geometry')
            raise ValueError('Please enter a valid geometry')

        self.setAnglesforHardware(angleList)
        self.setHardwareAdapter(hardwareAdapter)
        self._diffractometer = create_diffcalc(engine_name=self._engine, geometry=self._geometry,
                                               hardware=self._hardware)

    def returnInstanceList(self):
        return list(self.instances)

    def setDCInstance(self):
        '''
        To be modified as the hardware adapter is initiated
        '''
        self._diffractometer = create_diffcalc(str(self._engine), geometry=self._geometry, hardware=self._hardware)
        logInstance.logger.info('DiffCalc diffractometer instance created')

    def getHardwareInstance(self):
        return self._hardware

    def dummySetup(self, name, geometry, engine, tag, author):
        self.setName(name)
        self.setEngine(engine=engine)
        self.setGeometry(geometry)
        self.setTag(tag)
        self.setAuthor(author)
        self.setAnglesforHardware(angleList=self.getangleList(), Geometry=geometry)
        self.setHardwareAdapter(hardwareAdapter='DummyHardwareAdapter')
        self._diffractometer = create_diffcalc(engine, geometry=self._geometry, hardware=self._hardware)


class Angle(Diffractometer):
    """
    Each angle of the diffractometer is treated as an independent instance. This allows better controlled diffractometer circles. Each angle has an EPICS process variable that is required for motor motion.Angles also have attributes such as value and positive/negative limits.These are used as ways to capture unexpected events such as moving a circle out of limits.
    """

    def __init__(self, name, value, geometry, positiveLimit, negativeLimit, author):
        self._name = name
        self._value = value
        self._geometry = geometry
        self._positiveLimit = positiveLimit
        self._negativeLimit = negativeLimit
        self._author = author
        self._pv = ' '

    def setPV(self, PV):
        self._pv = PV
        try:
            connect(PV, wait=True, cainfo=True)
        except:
            logInstance.logger.error('Process Variable ' + str(PV) + ' not connected')
            raise Exception('Process Variable ' + str(PV) + ' not connected')

    def getPV(self):
        try:
            caget(str(self._pv))
            return self._pv
        except:
            logInstance.logger.error(
                'Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')
            raise Exception(
                'Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')

    def getSetPoint(self):
        try:
            self._value = caget(self._pv)
            return self._value
        except:
            logInstance.logger.error('Process Variable ' + str(self._pv) + ' not connected')
            raise Exception('Process Variable ' + str(self._pv) + ' not connected')


    def getValue(self):
        try:
            self._value = caget(self._pv + '.RBV')
            return self._value
        except:
            logInstance.logger.error('Process Variable ' + str(self._pv) + ' not connected')
            raise Exception('Process Variable ' + str(self._pv) + ' not connected')

    def setValue(self, value):
        try:
            self._value = value
            caput(self._pv, value)
        except:
            logInstance.logger.error(
                'Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')
            raise Exception(
                'Connection with IOC failed. Make sure EPICS motor record PVs are accessible under this subnet')


def setup(name, geometry, engine, tag, author, *params):
    diff = Diffractometer(name, geometry, engine, tag, author)
    if 'hardwareAdapter' in params:
        if 'angles' in params:
            diff.basicSetup(hardwareAdapter=params['hardwareAdapter'], angles=params['angles'])
        else:
            diff.basicSetup(hardwareAdapter=params['hardwareAdapter'])
    else:
        diff.basicSetup('HardwareAdapter')



