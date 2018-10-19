'''
Created on May 15, 2015

@author: pmackenz
'''
from MyIncrement import * 

class MyData(object):
    '''
    variables:
        self.ID = id
        self.increments = {}
    
    methods:
        __init__(self, id=-1)
        __str__(self)
        setID(self, id)
        getID(self)
        getIncrement(self, ID)
        addIncrement(self, inc)
        report(self)
        quickreport(self)
    '''


    def __init__(self, id=-1):
        '''
        Constructor
        '''
        self.ID = id
        self.increments = {}
        
    def __str__(self):
        txt = "all increments ...\n"
        for inc in self.increments:
            txt += inc 
        return txt
        
    def setID(self, id):
        self.ID = id
        
    def getID(self):
        return self.ID
    
    def getIncrement(self, ID):
        return self.increments[ID]
    
    def addIncrement(self, inc):
        self.increments[inc.getID] = inc
        
    def report(self):
        print(self)
        
    def quickreport(self):
        print("Increments found: ",len(self.increments))
        pass
        
            
        