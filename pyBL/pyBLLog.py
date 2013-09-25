'''
Created on Aug 26, 2013

@author: arkilic
'''
from pyOlog._conf import _conf
from pyOlog import OlogClient
from pyOlog import Tag,Logbook,Property
import logging
from os import path
from pyOlog import LogEntry

class ExperimentalLog():
    def __init__(self):
        self.ologLogbook='None'
        self.ologTag='None'
        self.ologProperty='None'
        self.existingProp=dict()

    def createLogger(self,name):
        self.logger = logging.getLogger(name)
        hdlr = logging.FileHandler(path.expanduser('~/'+str(name)+'.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)
        
    def createClient(self,url,username,password):
        try:
            self.ologClient=OlogClient(url,username,password)
            self.logger.info('Olog client created. url:'+str(url)+' user name:'+str(username))
            print 'Olog client created. url:'+str(url)+' user name:'+str(username)
        except:
            print 'Could not create client'
            self.logger.warning('Unable to create Olog client')
            raise ValueError('Unable to create Olog Client')
            
    
    def createTag(self,newTagName,newTagState):
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
            print 'Olog Tag '+str(newTagName)+' has already been created'             
        else:
            self.ologTag=Tag(name=newTagName, state=newTagState)
            try:
                self.ologClient.createTag(self.ologTag)
            except:
                self.logger.warning('Olog Tag can not be created')
                raise Exception('Olog Tag can not be created')
                
            
    def createLogbook(self,newLogbook,Owner):
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
            print 'Olog Logbook '+str(newLogbook)+' exists'
            self.logger.info('Olog Logbook '+str(newLogbook)+' exists')
        else:
            self.ologLogbook=Logbook(name=newLogbook, owner=Owner)
            try:
                self.ologClient.createLogbook(self.ologLogbook)
            except:
                self.logger.warning('Olog Logbook cannot be created')
                raise Exception('Olog Logbook cannot be created')
    
            
        
    def createProperty(self,name,**kwargs):
        propNames=list()
        self.existingPropObjects=self.ologClient.listProperties()
        for entry in self.existingPropObjects:
            propNames.append(entry.getName())
        propertyItems=['Name',
                       'Description', 
                       'ID',
                       'Type',
                       'Location',
                       'Attachments']
        if name in propNames:
            self.logger.warning('Property already exists and cannot be created')
            raise Exception('Property already exists and cannot be created')
        else:    
            for entry in kwargs:
                if entry in propertyItems:
                    self.existingProp[entry]=kwargs[entry]
                else:
                    self.logger.warning(str(entry)+' cannot be added as a property')
                    raise Exception(str(entry)+' cannot be added as a property')
            if len(self.existingProp)!=0:
                self.prop=Property(name, attributes=self.existingProp)
            else:
                self.logger.warning('No valid attribute is given for this property. Please refer to the documentation')
                raise ValueError('No valid attribute is given for this property. Please refer to the documentation')
        print self.existingProp
        
        
        
    def getProperty(self):
        raise NotImplementedError('to be implemented')
    
    
    def insertLog(self,text,owner,logbook,**kwargs):
        '''
            Creates a log entry with multiple attributes
        '''
	print kwargs
        logbookNames=list()
        keys=['id','createTime','modifyTime','attachments','properties','tags','type']
        composedLogEntry={}
        logbooks=self.ologClient.listLogbooks()
        for entry in logbooks:
            logbookNames.append(entry.getName())
            print entry.getName(),logbook
        if logbook not in logbookNames:
            self.logger.warning('No logbook created for logging purposes.Please create a Logbook')
            raise Exception('No logbook created for logging purposes.Please create a Logbook')
        else:
#             self.logID+=1
            for key in kwargs:
                if key in keys:
                    composedLogEntry[key]=kwargs[key]
                else:
                    self.logger.warning('The field cannot be added to the property')
                    raise Exception('The field '+str(key)+' cannot be added to the property')
            print composedLogEntry
                    
            
            
#             logEntry=LogEntry(text, owner, logbooks, tags, attachments, properties, id, createTime, modifyTime)
    
    
     
#     def insertProperty(self,**kwargs):
#         if len(self.existingProps)==0:
#             self.logger.warning('No property is created. Please create a property before you attempt to insert one')
#             raise Exception('No property is created. Please create a property before you attempt to insert one')
#         else:
#             
