"""
Logging is handled by logInstances created using ExperimentalLog class. This allows developers to add beamline specific modules without the need of defining new logging objects. This also avoids the confusion that might occur due to multiple logging schemes
"""
from pyOlog._conf import _conf
from pyOlog import OlogClient
from pyOlog import Tag,Logbook,Property
import logging
from os import path
from pyOlog import LogEntry

class ExperimentalLog():
    
    
    def __init__(self):
        self.ologClient=None
        self.ologLogbook=None
        self.ologTag=None
        self.ologProperty=None
        self.existingProp=list()
        self.existingAttributes=dict()
        self.ologEntry=None
        self.name=None
        
    def setName(self,name):
        """
        Sets the Configuration Name for a given diffractometer configuration. Default value is set inside pyBL.conf.\n
        **name:** Name of the diffractometer logging configuration
        """
        self.name=name    
    
    def getName(self):
        """
        Returns the Configuration Name
        """
        return self.name
    
    def getologLogbook(self):
        """
        Returns Olog logbook. Refer to Olog documentation for more information.
        """
        return self.ologLogbook
    
    def getologTag(self):
        """
        Returns Olog Tag. Refer to Olog documentation for more information.
        """
        return self.ologTag
    
    def getologProperty(self):
        """
        Returns Olog Property. Refer to Olog documentation for more information.
        """
        return self.ologProperty.getName()

            
    def createLogger(self,name):
        """
        Used exclusively inside createLogInstance(). Sets the format of the log instances using native python logging class and handlers.
        **name:** Denotes the name of the logging instance created. This logging instance will be used throughout the software as an independent, universal way to keep track of experimental procedure\n
        **return Type:** None

        """
        self.setName(name)
        self.logger = logging.getLogger(name)
        hdlr = logging.FileHandler(path.expanduser('~/'+str(name)+'.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)

    def createClient(self,url,username,password):
        """
        Creates an Olog client for the given diffractometer session. Url,username, and password are places inside a .conf file located in user home directory. This is used while creating a logInstance if an Olog server will be used.Not necessary for solely local logging.\n
        **url:** Address of Olog server\n
        **username:** user name reserved for an olog client. This will be used to record, save and retrieve a user session\n
        **password:** Olog server access password\n
        **return type:** None\n
        """
        try:
            self.ologClient=OlogClient(url,username,password)
            self.logger.info('Olog client created. url:'+str(url)+' user name:'+str(username))
#             print 'Olog client created. url:'+str(url)+' user name:'+str(username)
        except:
#             print 'Could not create client'
            self.logger.warning('Unable to create Olog client')
            raise ValueError('Unable to create Olog Client')
        
    
    def createTag(self,newTagName,newTagState):
        """
        Creates tag for olog entries. Refer to Olog documentation for more information.
        """
        tagList=list()
        tagObjects=list()
        try:
            tagObjects=self.ologClient.listTags()
        except:
            self.logger.warning('Olog tags cannot be accessed')
            raise Exception('Olog tags cannot be accessed')
        for entry in tagObjects:
            tagList.append(entry.getName())
        if newTagName in tagList:
            self.logger.info('Olog Tag'+str(newTagName)+' has already been created')   
#             print 'Olog Tag '+str(newTagName)+' has already been created'             
        else:
            self.ologTag=Tag(name=newTagName, state=newTagState)
            try:
                self.ologClient.createTag(self.ologTag)
                self.logger.warning('Olog Tag can not be created')
            except:
                raise Exception('Olog Tag can not be created')
        self.ologTag=newTagName
            
    def createLogbook(self,newLogbook,Owner):
        """
        Creates logbook for olog entries. Refer to Olog documentation for more information.
        """
        logbookList=list()
        logbookObjects=list()
        self.logID=0
        try:
            logbookObjects=self.ologClient.listLogbooks()
        except:
            self.logger.warning('Olog logbooks cannot be accessed')
            raise Exception('Olog logbooks cannot be accessed')
        for entry in logbookObjects:
            logbookList.append(entry.getName())
        if newLogbook in logbookList:
            self.logger.info('Olog Logbook '+str(newLogbook)+' exists')
        else:
            self.ologLogbook=Logbook(name=newLogbook, owner=Owner)
            try:
                self.ologClient.createLogbook(self.ologLogbook)
            except:
                self.logger.warning('Olog Logbook cannot be created')
                raise Exception('Olog Logbook cannot be created')
        self.ologLogbook=newLogbook
            
        
    def createProperty(self,name,**kwargs):
        """
        Creates a property for Olog entries. Refer to Olog documentation for more information
        """
        propertyItems=['Description', 
                       'ID',
                       'Type',
                       'Location',
                       'Attachments']
        if self.getProperty(name)!=None:
            self.logger.warning('Property already exists and cannot be created')
            raise Exception('Property already exists and cannot be created')
        else:    
            for entry in kwargs:
                if entry in propertyItems:
                    self.existingAttributes[entry]=kwargs[entry]
                else:
                    self.logger.warning(str(entry)+' cannot be added as a property')
                    raise Exception(str(entry)+' cannot be added as a property')
            if len(self.existingAttributes)!=0:
                self.prop=Property(name, attributes=self.existingAttributes)
                try:
                    self.ologClient.createProperty(self.prop)
                except:
                    self.logger.warning('Olog Property can not be created')
                    raise Exception('Olog Property can not be created')
            else:
                self.logger.warning('No valid attribute is given for this property. Please refer to the documentation')
                raise ValueError('No valid attribute is given for this property. Please refer to the documentation')
        self.ologProperty=name
        
        
    def getProperty(self,name):
        """
        Returns: Property if it is already created. None otherwise
        """
        propertyObjects=self.ologClient.listProperties()
        for obj in propertyObjects:
            if obj.getName()==name:
#                 print obj.getName()
                return obj
            
         
    def getTag(self,name):
        """
        Return:Olog Tag if it has been created. None otherwise
        """
        tagObejcts=self.ologClient.listTags()
        for obj in tagObejcts:
            if obj.getName()==name:
                return obj
            else:
                return None
        
    def getLogbook(self,name):
        """
        Returns Logbook if it is already created. None otherwise
        """
        logbookObjects=self.ologClient.listLogbooks()
        for obj in logbookObjects:
            if obj.getName()==name:
                return obj
            else:
                return None
    
    def insertLog(self,Txt,Ownr,logbook,**args):
        """
        Creates a log entry with multiple attributes.
        This module is incomplete as Olog integration has not yet been implemented.
        """
        att=[]
        possibleKeys={'id':None,'createTime':None,'modifyTime':None,'attachments':None,'properties':None,'tags':None,'type':None}
        if self.getLogbook(logbook)==None:
            self.logger.warning('No logbook created for logging purposes.Please create a Logbook')
            raise Exception('No logbook created for logging purposes.Please create a Logbook')
        else:
            for key in args:
                if key not in possibleKeys:
                    self.logger.warning('The field cannot be added to the property')
                    raise Exception('The field '+str(key)+' cannot be added to the property')
                else:
                    possibleKeys[key]=args[key]
                if possibleKeys['attachments']==None:
                    att=[]
                else:
                    att=[possibleKeys['attachments']]
                if possibleKeys['tags']==None:
                    tgs=[]
                else:
                    tgs=[possibleKeys['tags']]
                    
#                 self.ologEntry=LogEntry(text=Text, 
#                                         owner=Owner, 
#                                         logbooks=[self.getLogbook(logbook)], 
#                                         tags=tgs,
#                                         attachments=att
#                                             #properties,
#                                             #id,
#                                             #createTime, 
#                                             #modifyTime
#                                         )
        try:
            self.ologClient.log(LogEntry(text=Txt, 
                                     owner=Ownr, 
                                     logbooks=[self.getLogbook(logbook)], 
                                     tags=tgs,
                                     properties=[self.getProperty('process')],
                                     #attachments=att
                                     ))
        except:
            self.logger.warning('Log entry could not be inserted!')
            raise Exception('Log entry could not be inserted')

            
                
    
     
#     def insertProperty(self,**kwargs):
#         if len(self.existingProps)==0:
#             self.logger.warning('No property is created. Please create a property before you attempt to insert one')
#             raise Exception('No property is created. Please create a property before you attempt to insert one')
#         else:
#             
