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
        self.ologClient=None
        self.ologLogbook=None
        self.ologTag=None
        self.ologProperty=None
        self.existingProp=list()
        self.existingAttributes=dict()
        self.ologEntry=None
        
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
#             print 'Could not create client'
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
#             print 'Olog Tag '+str(newTagName)+' has already been created'             
        else:
            self.ologTag=Tag(name=newTagName, state=newTagState)
            try:
                self.ologClient.createTag(self.ologTag)
                self.logger.warning('Olog Tag can not be created')
            except:
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

            self.logger.info('Olog Logbook '+str(newLogbook)+' exists')
        else:
            self.ologLogbook=Logbook(name=newLogbook, owner=Owner)
            try:
                self.ologClient.createLogbook(self.ologLogbook)
            except:
                self.logger.warning('Olog Logbook cannot be created')
                raise Exception('Olog Logbook cannot be created')
    
            
        
    def createProperty(self,name,**kwargs):
        
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
        
        
        
    def getProperty(self,name):
        '''
            Returns Property if it is already created. None otherwise
        '''
        propertyObjects=self.ologClient.listProperties()
        for obj in propertyObjects:
            print obj.getName()
            if obj.getName()==name:
                return obj
            
         
    def getTag(self,name):
        tagObejcts=self.ologClient.listTags()
        for obj in tagObejcts:
            if obj.getName()==name:
                return obj
            else:
                return None
        
    def getLogbook(self,name):
        '''
            Returns Logbook if it is already created. None otherwise
        '''
        logbookObjects=self.ologClient.listLogbooks()
        for obj in logbookObjects:
            if obj.getName()==name:
                return obj
            else:
                return None
    
    def insertLog(self,Txt,Ownr,logbook,**args):
        '''
            Creates a log entry with multiple attributes
        '''
        att=[]
        print args
        print args['attachments']
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
            print self.getProperty('process')
            self.ologClient.log(LogEntry(text=Txt, 
                                     owner=Ownr, 
                                     logbooks=[self.getLogbook(logbook)], 
                                     tags=tgs,
                                     properties=[self.getProperty('process')],
                                     attachments=att
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
