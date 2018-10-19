'''
Created on May 15, 2015

@author: pmackenz
'''

from numpy import *


class MyPoint(object):
    '''
    Gauss point object
    holds ID, coordinates, stress, total strain, thermal strain
    
    variables:
        self.id     = id
        self.pos    = pos
        self.volume = vol
        self.dist   = dist
        
    methods:
        __init__(self, id=-1, pos=array([0.0,0.0,0.0]), jac=0.0, dist=0.0)
        getID(self)
        setID(self, id)
        getPos(self)
        setPos(self, pos)
        getVol(self)
        setVol(self, vol)
        getDist(self)
        setDist(self, radius):
        __str__(self)
    '''
    
    def __init__(self, id=-1, pos=array([0.0,0.0,0.0]), jac=0.0, dist=0.0):
        '''
        Constructor
        '''
        self.id     = id
        self.pos    = pos
        self.volume = jac
        self.dist   = dist
        
    def getID(self):
        return self.id
    
    def setID(self, id):
        self.id = id
    
    def getPos(self):
        return self.pos
    
    def setPos(self, pos, dist=0.0):
        self.pos = pos
        if dist > 0.0:
            self.dist = dist
    
    def getVol(self):
        if self.volume < 1.0e-12:
            print(",", end='')
        return self.volume
    
    def setVol(self, vol):
        self.volume = vol
    
    def getDist(self):
        return self.dist
    
    def setDist(self, radius):
        self.dist = radius
        
    def __str__(self):
        str = "gauss point {:d} at {:f} {:f} {:f} with volume={:f}".format(self.id, self.pos[0], self.pos[1], self.pos[2], self.volume)
        return str
    
    