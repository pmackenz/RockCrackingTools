'''
Created on May 18, 2015

@author: pmackenz
'''
from numpy import *

class MyNode(object):
    '''
    classdocs
    
    variables:
        self.id  = id
        self.pos = pos
        self.attachedElem = []
    
    methods:
        def __init__(self, id=-1, pos=array([0.0,0.0,0.0])):
        def setPos(self, pos):
        def getPos(self):
        def setID(self,id):
        def getID(self):
        def addElem(self, elemID):
        def isAttached(self,elemID):
        def rmElem(self,elemID):
    '''

    def __init__(self, id=-1, pos=array([0.0,0.0,0.0])):
        '''
        Constructor
        '''
        self.id  = id
        self.pos = pos
        self.attachedElem = []
        
    def setPos(self, pos):
        self.pos = array(pos)
        
    def setID(self,id):
        self.id = id
        
    def getID(self):
        return self.id
    
    def getPos(self):
        return self.pos
    
    def addElem(self, elemID):
        if ( not elemID in self.attachedElem ):
            self.attachedElem.append(elemID)
            
    def isAttached(self,elemID):
        return (elemID in self.attachedElem)
    
    def rmElem(self,elemID):
        if ( elemID in self.attachedElem ):
            self.attachedElem.remove(elemID)
            
    
    
            
        