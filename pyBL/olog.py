'''
Created on Aug 26, 2013

@author: arkilic
'''
from pyOlog._conf import _conf
from pyOlog import OlogClient
from pyOlog import Tag,Logbook,Property



#search tag. if exists return that tag, if not create tag
def createClient(self,url,username,password):
    try:
        print 'Client created'
        self.ologClient=OlogClient(url,username,password)
        self.logger.info('Olog client created. url:'+str(url)+' user name:'+str(username))
    except:
        print 'Could not create client'
        self.logger.warning('Unable to create Olog client')
        raise ValueError('Unable to create Olog Client')
        

def createTag(self,Tag):
    if self.getClient().find(tag=Tag.getName())==[]:
        try:
            self.getClient().createTag(Tag)
            self.logger.info('Olog Tag'+' created')
        except:
            self.logger.warning('Olog Tag can not be created')
            raise Exception('Olog Tag can not be created')
    else:
        self.logger.info('Olog Tag'+str(Tag.getName())+' has already been created')
        
def createLogbook(self,logBook):
    print self.getClient().find(logbook=logBook.getName())
    a=self.getClient().listLogbooks()
    for entry in a:
        if entry.getName()==logBook.getName():
    
            print 'yeah!'
#     self.getClient().createLogbook(logBook)
        
#     ologTag=Tag(name='tagXXYYZZ', state='Active')
# # ologLogbook=Logbook('DiffractometerXXYYZZ', owner='Beamline Diffractometer'+str(self._name))
# # ologProp=Property(name='DiffractometerXXYYZ', 
# #                        attributes={'name':'Process',
# #                       'type':'diffractometer.setup',
# #                       'processId':1903,
# #                       'processAttachments':path.expanduser('~/pyOlog.conf')})
# #         #self.ologClient=OlogClient(url=URL, username=USR, password=PSWD)
# #     def setClient(self,url,username,password):
# #         self.ologClient=OlogClient(url,username,password)
# #         self.logger.info('Olog client details modified to url:'+str(url)+' user name:'+str(username)+' password:'+str(password))
# #     
# #     def getClient(self):
# #         return self.ologClient
# #         
# #     def setOlogTag(self,state):
# #         self.ologTag=Tag(self._tag,state)
# #         self.logger.info('Olog Tag details modified. Name:'+self.ologTag.getName()+' State:'+self.ologTag.getState())
# #     
# #     def getOlogTag(self):
# #     
# #     def setologLogbook(self,name,owner):
# #         self.ologLogbook=Logbook(name, owner)
# #         self.logger.info('Olog Logbook details modified. Name:'+self.ologLogbook.getName()+' Owner:'+self.ologLogbook.getOwner())
# #     
# #     def getologLogbook(self):
# #         return self.ologLogbook
# #     
# #     def setologProp(self,name,attributes):
# #         '''
# #             Attributes must be a dictionary.See default definition above for further instructions
# #         '''
# #         self.ologProp=Property(name, attributes)
# #         self.logger.info('Olog Property details modified. Name:'+str(self.ologProp.getName())+' Attribute Names:'+str(self.ologProp.getAttributeNames()))
# #     
# #     def getologProp(self):
# #         return self.ologProp
# #         
# #     def createOlogProp(self):
# #         try:
# #             self.ologClient.createProperty(self.ologProp)
# #             self.logger.info('Olog Property created'+ str(self.ologProp.getAttributeNames()))
# #         except:
# # #             self.logger.warning('an identical property has already been created.')
# # # #              ValueError('An identical property has already been created.')
# #    def createOlogTag(self):
# #         '''
# #             Olog tag is identical to logbook tag...
# #         '''
# #         self.ologClient.createTag(self.ologTag)
# #         self.logger.info('Olog Tag created. Name'+self.ologTag.getName())
# #     
# #     def createOlogLogbook(self):
# #         self.ologClient.createLogbook(self.ologLogbook)
# #         self.logger.info('Olog Logbook created. Name:'+self.ologLogbook.getName())
# #         