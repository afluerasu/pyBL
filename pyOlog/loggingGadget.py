from pyOlog import OlogClient,Tag,Logbook,Property,LogEntry


client=OlogClient(url='https://webdev.cs.nsls2.local:8181/Olog',username='arkilic',password=1234)
tag=Tag(name='trial', state='Active')
client.createTag(tag)
logbook=Logbook(name='trialsLogbook', owner='trial owner')
client.createLogbook(logbook)
atts={'name':'trial',
            'description':'trial attributes for pyOlog logging trial',
            'type':'None'
            }
prop=Property(name='process', attributes=atts)
# client.createProperty(prop)
client.log(LogEntry(text='trial',
                    owner='trial owner',
                    logbooks=[logbook],
                    tags=[tag], 
                    #attachments, 
                    properties=[prop], 
                    #id, 
                    #createTime, 
                    #modifyTime
                    ))
atts1={'name':'trial',
            'description':'trial attributes for pyOlog logging trial',
            'type':'Automatic'
            }
newprop=Property(name='process',attributes=atts1)
client.log(LogEntry(text='trial',
                    owner='trial owner',
                    logbooks=[logbook],
                    tags=[tag], 
                    #attachments, 
                    properties=[newprop], 
                    #id, 
                    #createTime, 
                    #modifyTime
                    ))
