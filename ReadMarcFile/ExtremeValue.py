'''
Created on Apr 1, 2016

@author: pmackenz
'''
from numpy import array, inf

class ExtremeValue(object):
    '''
    variables:
        self.maxVal = -inf
        self.minVal =  inf
        self.pos    = pos
        self.elemID = elemID
        self.GP     = gp
    
    methods:
        __init__(self, pos=array([0., 0., 0.]), elemID=-1, gp=0)
        testValue(self, val)
        getValue(self)
        setPosition(self, pos)
        getPosition(self)
        setElemID(self, elemID)
        getElemID(self)
        setGP(self, gp)
        getGP(self)
    '''


    def __init__(self, pos=array([0., 0., 0.]), elemID=-1, gp=0):
        '''
        Constructor
        '''
        self.maxVal = -inf
        self.minVal =  inf
        self.pos    = pos
        self.elemID = elemID
        self.GP     = gp
        
        
    def testValue(self, val):
        if (val > self.maxVal):
            self.maxVal = val
        if (val < self.minVal):
            self.minVal = val
    
    def getMax(self):
        return self.maxValue
        
    def getMin(self):
        return self.maxValue
        
    def setPosition(self, pos):
        self.pos = pos
        
    def getPosition(self):
        return self.pos
        
    def setElemID(self, elemID):
        self.elemID = elemID
    
    def getElemID(self):
        return self.elemID
        
    def setGP(self, gp):
        self.GP = gp
        
    def getGP(self):
        return self.GP
    
        