'''
Created on May 15, 2015

@author: pmackenz
'''

from numpy import *
from MyPoint import *


class MyElement(object):
    '''
    a list of up to 8 MyPoint objects
    
    variables:
        self.ID    = id
        self.nodes = connect
        self.gps   = {}
    
    methods:
        __init__(self, id=-1, connect=[0,0,0,0,0,0,0,0])
        __str__(self, *args, **kwargs)hasNode(self, nodeID)
        getID(self)
        getNodes(self)
        reset(self)
        addGaussPoint(self, id, pos)
        getGaussPoint(self, id)
        has_no_gpts(self)
        has_gpts(self)
        computeGPVolume(self, nodeList, x0)
        getVolume(self)
        getGPvolume(self, pt)
        setGPvolume(self, pt, vol)        
        getGPposition(self, pt)    
        setGPposition(self, pt, pos) 
        getGPdistance(self, pt)
        setGPdistance(self, pt, dist)       
        getGPinfo(self)
        setGPinfo(self, GPinfo)
        scanVolume(self, volArray, limits)
        scanDirData(self, directions, dirData)
        countGaussPoints(self)
    '''

    def __init__(self, id=-1, connect=[0,0,0,0,0,0,0,0]):
        '''
        Constructor
        '''
        self.ID = id
        self.nodes  = connect
        self.gps = {}
        for i in range(8):
            #self.gps[i+1] = MyPoint(i+1)
            pass
        
    def reset(self):
        self.ID = -1
        self.nodes  = [0,0,0,0,0,0,0,0]
             
    def __str__(self, *args, **kwargs):
        strg = "element {:d}: \n".format(self.ID)
        strg += "   nodes: "
        for nd in self.nodes:
            strg += "{} ".format(nd)
        strg += "\n"
        strg += "   gauss points:\n"
        for pt in self.gps:
            for key in self.gps[pt].keys():
                strg += "    " + key + ":" + str(self.gps[pt][key]) + "\n"
        return strg
    
    def getID(self):
        return self.ID
    
    def getNodes(self):
        return self.nodes
    
    def hasNode(self, nodeID):
        if (nodeID <= 0):
            return False
        return ( nodeID in self.nodes )
    
    def addGaussPoint(self, id, pos, dist=0.0):
        if (not id in self.gps):
            self.gps[id] = MyPoint(id, pos, dist)
            
    def getGaussPoint(self, id):
        if (id in self.gps):
            #print ".",
            return self.gps[id]
        else:
            print( "element {}: unknown gauss point id: {}".format(self.ID, id) )
            return (MyPoint(-1, array([0.0,0.0,0.0])))
        
    def has_gpts(self):
        if len(self.gps.keys()) == 8:
            return True
        else:
            return False
    
    def has_no_gpts(self):
        if len(self.gps.keys()) == 0:
            return True
        else:
            return False

    def computeGPVolume(self, nodelist=array([[0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0],
                                              [0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0]]),
                        centerPos=zeros(3)):
        
        gpts = array([-math.sqrt(1./3.),math.sqrt(1./3.)])
        
        pt = 1
        
        for u in gpts:
            um = 0.5*(1-u)
            up = 0.5*(1+u)
            for t in gpts:
                tm = 0.5*(1-t)
                tp = 0.5*(1+t)
                for s in gpts:
                    sm = 0.5*(1-s)
                    sp = 0.5*(1+s)
                    
                    shp = array([
                        sm*tm*um, sp*tm*um, sp*tp*um, sm*tp*um,
                        sm*tm*up, sp*tm*up, sp*tp*up, sm*tp*up
                        ])
                    
                    pos = dot(shp, nodelist)
                    
                    dshp = array([
                        [ -0.5*tm*um, 0.5*tm*um, 0.5*tp*um,-0.5*tp*um,
                          -0.5*tm*up, 0.5*tm*up, 0.5*tp*up,-0.5*tp*up ],
                        [ -sm*0.5*um,-sp*0.5*um, sp*0.5*um, sm*0.5*um,
                          -sm*0.5*up,-sp*0.5*up, sp*0.5*up, sm*0.5*up ],
                        [ -sm*tm*0.5,-sp*tm*0.5,-sp*tp*0.5,-sm*tp*0.5,
                           sm*tm*0.5, sp*tm*0.5, sp*tp*0.5, sm*tp*0.5 ]
                        ])
                    
                    vol = linalg.det( dot(dshp,nodelist) )
                    
                    self.gps[pt].setVol(vol)
                    self.gps[pt].setPos(pos)
                    self.gps[pt].setDist(linalg.norm(pos - centerPos))
                    
                    pt += 1
                    
        
    def getVolume(self, limit=1.0e16):
        elemVolume = 0.0
        for gp in self.gps:
            dist = self.gps[gp].getDist()
            if dist < limit:
                elemVolume += self.gps[gp].getVol()
            else:
                print(".", end='')
        return elemVolume
    
    def getGPvolume(self, pt):
        if ( (pt-1) in range(8) ):
            return self.gps[pt].getVol()
        else:
            return 0.0
    
    def setGPvolume(self, pt, vol):
        if not ( (pt-1) in range(8) ):
            raise
        if not self.gps.has_key(pt):
            self.gps[pt] = MyPoint(pt+1)
        self.gps[pt].setVol(vol)
            
    def getGPposition(self, pt):
        if ( (pt-1) in range(8) ):
            return self.gps[pt].getPos()
        else:
            return array([0.,0.,0.])
        
    def setGPposition(self, pt, pos):
        if not ( (pt-1) in range(8) ):
            raise
        if not self.gps.has_key(pt):
            self.gps[pt] = MyPoint(pt+1)
        self.gps[pt].setPos(pos)
            
    def getGPdistance(self, pt):
        if ( (pt-1) in range(8) ):
            return self.gps[pt].getDist()
        else:
            return 0.0
        
    def setGPdistance(self, pt, dist):
        if not ( (pt-1) in range(8) ):
            raise
        if not self.gps.has_key(pt):
            self.gps[pt] = MyPoint(pt+1)
        self.gps[pt].setDist(dist)
            
    def getGPinfo(self):
        GPinfo={}
        for i in range(8):
            pt = i+1
            GPinfo[pt] = {'volume':self.gps[pt].getVol(),
                          'position':self.gps[pt].getPos(),
                         'distance':self.gps[pt].getDist()}
        return GPinfo
    
    def setGPinfo(self, GPinfo):
        for pt in GPinfo:
            if (not pt in self.gps):
                self.gps[pt] = MyPoint(pt+1)
            if ('volume' in GPinfo[pt]):
                self.gps[pt].setVol(GPinfo[pt]['volume'])
            if ('position' in GPinfo[pt]):
                self.gps[pt].setPos(GPinfo[pt]['position'])
            if ('distance' in GPinfo[pt]):
                self.gps[pt].setDist(GPinfo[pt]['distance'])
                    
    def scanVolume(self, volArray, limits):
        for pt in self.gps:
            idx = len(limits) - 1
            dist = self.gps[pt].getDist()
            
            if len(volArray) > len(limits):
                volArray[-1] += 1
            
            # find proper segment
            while dist > limits[idx]:
                idx -= 1
                if idx<0:
                    idx = 0
                    break
                
            # add integrand
            if dist <= limits[0]:
                volArray[idx] += self.gps[pt].getVol()
            else:
                print("element {}: gauss point outside boulder!".format(self.ID) )

    def scanDirData(self, directions, dirData):
        for pt in self.gpts:
            for thisDir in directions:
                stress = pt.ge

    def getMaxDist(self):
        maxdist = -1.0e16
        for pt in self.gps:
            dist = self.gps[pt].getDist()
            
            if dist > maxdist:
                maxdist = dist
                
        return maxdist

    def countGaussPoints(self):
        return len(self.gps)
    
