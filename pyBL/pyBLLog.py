'''
Created on Aug 26, 2013

@author: arkilic
'''
from pyOlog._conf import _conf
from pyOlog import OlogClient
from pyOlog import Tag,Logbook,Property
import logging
from os import path

class ExperimentalLog():

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
        tagObjects=self.ologClient.listTags()
        for entry in tagObjects:
            tagList.append(entry.getName())
        print tagList
        if newTagName in tagList:
            self.logger.info('Olog Tag'+str(newTagName)+' has already been created')   
            print 'Olog Tag '+str(newTagName)+' has already been created'             
        else:
            ologTag=Tag(name=newTagName, state=newTagState)
            try:
                self.ologClient.createTag(ologTag)
            except:
                self.logger.warning('Olog Tag can not be created')
                raise Exception('Olog Tag can not be created')
                
            
    def createLogbook(self,logBook):
        print self.getClient().find(logbook=logBook.getName())
        a=self.getClient().listLogbooks()
        for entry in a:
            if entry.getName()==logBook.getName():
                print 'yeah!'
