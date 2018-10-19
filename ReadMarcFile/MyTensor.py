'''
Created on May 18, 2015

@author: pmackenz
'''

from numpy import *

class MyTensor(object):
    '''
    classdocs
    
    variables:
        self.vals  = array(vals)             # sx, sy, sz, sxy, syz, szx
        self.pvals = array([vmn,vmd,vmx])    # principal values
        self.dirs  = dir                     # list of unit vectors indicating direction of pvals
    
    methods:
        __init__(self, vals=[0.,0.,0.,0.,0.,0.])
        __str__(self)
        __repr__(self)
        asMatrix(self)
        analyze(self)
        getMaxVal(self)
        getMinVal(self)
        getMedVal(self)
        getMaxDir(self)
        getMinDir(self)
        getMedDir(self)
        getVals(self)
        getMean(self)
        getDeviator(self)
        Identity(self)
        Norm(self)
        getWeibullB(self, sigma0=1.0, m=1.0)
        vonMises(self)
        Tresca(self)
    '''

    def __init__(self, vals=[0.,0.,0.,0.,0.,0.]):
        '''
        Constructor
        '''
        self.vals = array(vals)
        self.analyze()
        
    def __str__(self):
        return str(self.vals)
    
    def __repr__(self):
        return "MyTensor({})".format(self.vals)
    
    def asMatrix(self):
        ten = array([
                     [self.vals[0],self.vals[3],self.vals[5]],
                     [self.vals[3],self.vals[1],self.vals[4]],
                     [self.vals[5],self.vals[4],self.vals[2]]
                     ])
        return ten
    
    def analyze(self):
        ten = self.asMatrix()
        pvals, eigvecs = linalg.eigh(ten)
        dir = eigvecs.T
        vmx, vmd, vmn = pvals
        if vmd < vmn:
            vmd, vmn = vmn, vmd
            sd     = dir[1]
            dir[1] = dir[0]
            dir[0] = sd
        if vmd > vmx:
            vmd, vmx = vmx, vmd
            sd     = dir[1]
            dir[1] = dir[2]
            dir[2] = sd
        if vmd < vmn:
            vmd, vmn = vmn, vmd
            sd     = dir[1]
            dir[1] = dir[0]
            dir[0] = sd
        self.pvals = array([vmn,vmd,vmx])
        self.dirs  = dir            
        
    def getMaxVal(self):
        return self.pvals[2]
    
    def getMinVal(self):
        return self.pvals[0]
    
    def getMedVal(self):
        return self.pvals[1]         
        
    def getMaxDir(self):
        return self.dirs[2]
    
    def getMinDir(self):
        return self.dirs[0]
    
    def getMedDir(self):
        return self.dirs[1]
    
    def getVals(self):
        return self.vals
    
    def getMean(self):
        return sum(self.pvals)/3.0
    
    def getDeviator(self):
        return self.vals - self.getMean()*self.Identity()
    
    def Identity(self):
        return array([1,1,1,0,0,0])
    
    def Norm(self):
        return linalg.norm(self.pvals)
    
    def getWeibullB(self, sigma0=1.0, m=1.0):
        val = 0.0
        trival = 1.0
        for s in self.pvals:
            if s > 0.0:
                sb = s/sigma0
                val += sb**m
                trival *= sb
            else:
                trival *= 0.0
        if trival > 0.0:
            val += 3.0*trival**(m/3.0)
        return val
        
    def vonMises(self):
        val  = self.vals[0]*self.vals[0]
        val += self.vals[1]*self.vals[1]
        val += self.vals[2]*self.vals[2]
        val -= self.vals[0]*self.vals[1]
        val -= self.vals[1]*self.vals[2]
        val -= self.vals[2]*self.vals[0]
        val += 3.0*self.vals[3]*self.vals[3]
        val += 3.0*self.vals[4]*self.vals[4]
        val += 3.0*self.vals[5]*self.vals[5]
        return sqrt(val)
    
    def Tresca(self):
        val = max(self.pvals) - min(self.pvals)
        return val
    


        