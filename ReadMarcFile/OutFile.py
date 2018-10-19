'''
Created on Feb 11, 2015

@author: pmackenz
'''
from numpy import * 
from MyData import *
from MyIncrement import *
from MyElement import *
from MyNode import *

class OutFile(object):
    '''
    variables:
        self.filename = ""
        self.file
        self.file_open = False
        self.data       = MyData()
        self.increments = {}
        self.elements   = {}
        self.nodes      = {}
        self.line = ""
        self.MinMaxData = {}
        self.nSegments = nSegments     # (int)
        self.diameter  = diameter      # (float)
        self.delta     = skin_depth    # (float)
        self.sigma0    = sigma0        # (float)
        self.m         = exponent_m    # (float)
        self.Vol0      = Vol0          # (float)
        self.volume    = zeros(nSegments)
        self.radii     = array()
    
    methods:
        __init__(self, filename, diameter, skin_depth)
        __del__(self)
        setParameters(self, diameter, skin_depth, sigma0, exponent_m, V0)
        GetNodes(self, nodes)
        GetElements(self, elements)
        GetGaussPoints(self, gpts)
        ReadIncrement(self, data)
        GetIncrement(self,id=0)
        WipeIncrement(self,id=0)
        ClearIncrements(self):
        FindNextIncrement(self)
        FindIncrement(self,n)
        FindAllIncrements(self)
        copyLines(self,check)
        scanIncrementZero(self)
        Close(self)
        getNodeInfo(self)
        getElementInfo(self)
        getGPinfo(self)
        Report(self)
        setMinMaxContainer(self)
        getVolume(self)
        countGaussPoints(self)
        verifyIncrementData(self, inc=-1)
        GetWeibullData(self,inc=-1)
        ReportOpen(self)
        ReportClose(self)
    '''

    def __init__(self, filename, diameter=10000.0, skin_depth=100000.0):
        '''
        Constructor
        '''
        if diameter < 0.001:
            diameter = 0.001
        if skin_depth < 0.0005:
            skin_depth = 0.5*(diameter + 0.001)
        
        self.delta     = skin_depth
        nSegments = int(ceil(0.5*diameter/skin_depth))
        
        self.nSegments = nSegments
        self.diameter  = diameter
        self.dia_cm=int(self.diameter*100)
        self.delta     = skin_depth  
        
        self.volume    = zeros(nSegments)
        self.radii     = 0.50*self.diameter - arange(nSegments)*self.delta 
        
        self.x0        = array([0.0, 0.5*diameter, 0.0])
        
        self.filename  = filename
        try:
            self.file = open(filename, 'r')
            self.file_open = True
        except:
            print('cannot open file',filename)
            self.file_open = False
        # results container
        self.data       = MyData()
        # parsed increments container
        self.increments = {}
        # parsed element connectivity data
        self.elements   = {}
        # parsed nodal coordinates data
        self.nodes      = {}
        # line buffer
        self.line = ""
        
        self.setParameters()
        
        self.ReportOpen()
        
        
        self.scanIncrementZero()
        self.stressdata=[]
        # clean up elements without results at gauss points
        elemKeys = list(self.elements.keys())
        for elemID in elemKeys:
            
            if self.elements[elemID].has_no_gpts():
                del self.elements[elemID]
                continue
            
            # create cross referencing information for nodes
            nodelist  = []
            centerPos = zeros(3)
            for nodeID in self.elements[elemID].getNodes():
                self.nodes[nodeID].addElem(elemID)
                nodelist.append(self.nodes[nodeID].getPos())
                centerPos += self.nodes[nodeID].getPos()
            # compute center point position and distance from center
            centerPos *= 0.125
            meanDist = linalg.norm(centerPos - self.x0)
            
            if meanDist > 0.5*self.diameter:
                del self.elements[elemID]
                #print "element {} has dist={} > {}".format(elemID, meanDist, 0.5*self.diameter)
                continue
                
            if not(self.elements[elemID].has_no_gpts() or self.elements[elemID].has_gpts()):    
                print("data error in element {}:", elemID)
                print(self.elements[elemID])
                raise
            
            if self.elements[elemID].has_no_gpts():
                # check against mean distance: center point is average of nodal coordinates
                print("*** element within boulder missing data ***")
                raise
            
            # compute gauss-point position, volume, and distance from center   
            self.elements[elemID].computeGPVolume(array(nodelist), self.x0)
        
        #print self.elements[11514]
        
        self.setMinMaxContainer()
        
    def __del__(self):
        if self.file_open:
            self.file.close()
            self.file_open = False
            
    def setParameters(self, sigma0=1000000.0, exponent_m=10, Vol0=1.0):
        
        self.sigma0   = sigma0
        self.m        = exponent_m
        self.Vol0     = Vol0
        
            
    def GetNodes(self, nodes):
        if self.file_open:
            for self.line in self.file:
                if (self.line.find('s t a r t   o f   i n c r e m e n t') > 0):
                    self.elements.append(MyElement())
                    return self.line.strip()
            self.Close()
        else:
            return "no more increments"
        pass
    
    def GetElements(self, elements):
        pass
    
    def GetGaussPoints(self, gpts):
        pass
    
    def ReadIncrement(self, data):
        pass
    
    def GetIncrement(self,id=0):
        if (id in self.increments):
            return self.increments[id]
        else:
            return MyIncrement(id)
        
    def WipeIncrement(self,id=0):
        if (id in self.increments):
            del self.increments[id]
        
    def ClearIncrements(self):
        self.increments = {}
        
    def FindNextIncrement(self):
        if self.file_open:
            for self.line in self.file:
                if (self.line.find('s t a r t   o f   i n c r e m e n t') > 0):
                    print(self.line.strip())
                    nInc = int(self.line[50:56])
                    thisInc = MyIncrement(nInc)
                    thisInc.parse(self.file)
                    thisInc.updateElementInfo(self.elements)
                    
                    volume = thisInc.scanVolume()
                    print("volume = " + str(volume))
                    thisInc.setParameters(self.diameter, self.delta, self.sigma0, self.m, self.Vol0)
                    thisInc.printProbabilities()
                    [time1,time2] = self.InctoTime(thisInc.ID)
                    filename_dir  = "./data/{:03d}cm_{}.txt".format(self.dia_cm,time1)
                    thisInc.ScanStress(filename_dir)
                    #thisInc.PlotStressDirection(filename_dir,self.dia_cm,time1,time2)
                    if (nInc in self.increments):
                        print("warning: overwriting already existing increment {} !".format(nInc))
                    self.increments[nInc] = thisInc
                    return nInc
            self.Close()
            return -1
        else:
            return -1
    
    def FindIncrement(self,n):
        if self.file_open:
            for self.line in self.file:
                if (self.line.find('s t a r t   o f   i n c r e m e n t') > 0):
                    print(self.line.strip())
                    nInc = int(self.line[50:56])
                    if (nInc < n):
                        continue
                    thisInc = MyIncrement(nInc)
                    thisInc.parse(self.file)
                    thisInc.updateElementInfo(self.elements)
                    thisInc.setParameters(self.diameter, self.delta, self.sigma0, self.m, self.Vol0)
                    thisInc.printProbabilities()
                    volume = thisInc.scanVolume()
                    [time1,time2]=self.InctoTime(thisInc.ID)
                    filename_dir="../data/{}_direction_{}.txt".format(self.dia_cm,time1)
                    thisInc.ScanStress(filename_dir)
                    #thisInc.PlotStressDirection(filename_dir,self.dia_cm,time1,time2)
                    print("volume = " + str(volume))
                    
                    if (nInc in self.increments):
                        print("warning: overwriting already existing increment {} !".format(nInc))
                    self.increments[nInc] = thisInc
                    return nInc
            self.Close()
            return -1
        else:
            return -1
    
    def FindAllIncrements(self):
        cnt = 0
        txt = self.FindNextIncrement()
        while ( txt != ""  and self.file_open ) :
            cnt += 1
            print (txt)
            if txt.find('144') > 0:
                self.copyLines("e n d   o f   i n c r e m e n t")
            txt = self.FindNextIncrement()
        return cnt
    
    def copyLines(self,check):
        for self.line in self.file:
            if self.line.find(check) > 0:
                break
            if self.line.strip() == "":
                continue
            print(self.line.rstrip())
            
    def scanIncrementZero(self):
        keywords = ('coordinates','connectivity','e n d   o f   i n c r e m e n t')
        
        if self.file_open:
            for self.line in self.file:
                if (self.line.find('e n d   o f   i n c r e m e n t') >= 0):
                    return 0
                if (self.line.find('coordinates') == 13):
                    self.getNodeInfo()
                if (self.line.find('connectivity') == 13):
                    self.getElementInfo()
                if (self.line.find('element') == 1):
                    self.getGPinfo()
                    
            self.Close()
        
        return -1
    
    def Close(self):
        if self.file_open:
            self.file.close()
            self.file_open = False
            
    def getNodeInfo(self):
        cnt = 0
        print(self.line.rstrip())
        for self.line in self.file:
            print(self.line.rstrip())
            cnt += 1
            if (cnt >= 5):
                break
        
        # time to read nodal information
        for self.line in self.file:
            
            if (self.line.strip() == ""):
                break
            
            id = int(self.line[16:23])
            pos = array([0.0,0.0,0.0])
            pos[0] = float(self.line[23:37])
            pos[1] = float(self.line[37:51])
            pos[2] = float(self.line[51:65])
                
            node = MyNode(id, pos)
            
            if (id in self.nodes):
                print("Node {} already exists".format(id))
            else:
                self.nodes[id] = node
    
    def getElementInfo(self):
        cnt = 0
        print(self.line.rstrip())
        for self.line in self.file:
            print(self.line.rstrip())
            cnt += 1
            if (cnt >= 5):
                break
         
        # time to read element information
        for self.line in self.file:
            
            if (self.line.strip() == ""):
                break
            
            id = int(self.line[16:23])
            type = int(self.line[23:30])
            conn = [0,0,0,0,0,0,0,0]
            if (type == 7):
                conn[0] = int(self.line[35:45])
                conn[1] = int(self.line[45:55])
                conn[2] = int(self.line[55:65])
                conn[3] = int(self.line[65:75])
                conn[4] = int(self.line[75:85])
                conn[5] = int(self.line[85:95])
                conn[6] = int(self.line[95:105])
                conn[7] = int(self.line[105:115])
                
            elem = MyElement(id, conn)
            
            if (not id in self.elements):
                self.elements[id] = elem
            else:
                print("Element already defined: " + str(id))
            
    def getGPinfo(self):
        elmtId  = int(self.line[10:19])
        pointId = int(self.line[26:30])
        
        pos = array([0.0,0.0,0.0])
        pos[0] = float(self.line[65:78])
        pos[1] = float(self.line[78:91])
        pos[2] = float(self.line[91:104])
        
        dist = linalg.norm(pos - self.x0)
        
        if (elmtId in self.elements):
            self.elements[elmtId].addGaussPoint(pointId, pos, dist) 
            #print "{:d}.{:d}:{} at {} from center".format(elmtId,pointId,pos, dist)
        else:
            print("missing element " + str(elmtId))
            
    def Report(self):
        print("analysis of " + self.filename + ":\n")
        print("Number of nodes:      " + str(len(self.nodes)))
        print("Number of elements:   " + str(len(self.elements)))
        print("Number of increments: " + str(len(self.increments)))
        
        for elmt in sorted(self.elements.keys()):
            print(self.elements[elmt])
            break
    
    def setMinMaxContainer(self):
        self.MinMaxData = {}
        for elem in self.elements.keys():
            self.MinMaxData[elem] = {}
            for gpt in range(8):
                self.MinMaxData[elem][str(gpt+1)] = ExtremeValue(pos = self.elements[elem].getGaussPoint(gpt+1).getPos(), 
                                                                 elemID = self.elements[elem].getID(), 
                                                                 gp = gpt+1)
        
    def getVolume(self):
        maxdist = -1.0e16
        vol = 0.0
        for elem in self.elements:
            vol += self.elements[elem].getVolume(limit=0.5*self.diameter)
            dist = self.elements[elem].getMaxDist()
            if dist > maxdist:
                maxdist = dist
                
        print(maxdist)
        
        return vol
    
    def countGaussPoints(self):
        count = 0
        for elem in self.elements:
            count += self.elements[elem].countGaussPoints()
        return count
    
    def verifyIncrementData(self, inc=-1):
        if inc < 0:
            for thisinc in self.increments:
                if not self.increments[thisinc].verifyElementData(self.elements):
                    print("*** increment {} failed element data verification ***".format(thisinc))
        else:
            if (inc in self.increments):
                if not self.increments[inc].verifyElementData(self.elements):
                    print("*** increment {} failed element data verification ***".format(inc))
                
    def GetWeibullData(self,inc=-1):
        if inc<0:
            if len(self.increments.keys()) > 0:
                inc = max(self.increments.keys())
            else:
                print("No increment data available")
                return {}
            
        if (inc in self.increments):
            WeibullData = self.increments[inc].getWeibullData()
    
            s = "{},{nSegments},{POS},{POF},".format(inc,**WeibullData)
            for x in WeibullData['limits']:
                s += "{},".format(x)
            for x in WeibullData['WeibullB']:
                s += "{},".format(x)
            for x in WeibullData['POSlayers']:
                s += "{},".format(x)
            for x in WeibullData['POFlayers']:
                s += "{},".format(x)
            s += "\n"
            self.reportfile.write(s)
            self.reportfile.flush()
            
            return WeibullData
        else:
            raise DataIntegrityError     
        
    def ReportOpen(self):
        try:
            self.reportfileName = self.filename[:-3] + "csv"
            self.reportfile = open(self.reportfileName, 'w')
        except:
            print("cannot create report file for writing")
            raise IOError
        # form header line
        s = "Inc,nSegments,POS,POF,"
        for i in range(self.nSegments):
            s += "R{},".format(i+1)
        for i in range(self.nSegments):
            s += "B{},".format(i+1)
        for i in range(self.nSegments):
            s += "POS{},".format(i+1)
        for i in range(self.nSegments):
            s += "POF{},".format(i+1)
        s += "\n"
        self.reportfile.write(s)
        self.reportfile.flush()


    def ReportClose(self):
        if self.reportfile:
            self.reportfile.close()
            
            
    def Setnskip(self,nskip):
        self.nskip=nskip
        
    def InctoTime(self,inc):
        h=(inc-(self.nskip+1))*0.25
        hr=int(h)
        m=(h-hr)*60
        min=int(m)
    
        if hr>=10:
            hour=str(hr)
        elif hr==0:
            hour='00'
        else:
            hour='0'+str(hr)

      
        if min>=10:
            minutes=str(min)
        elif min==0:
            minutes='00'
        else:
            minutes='0'+str(min)
    
        time1=hour+minutes
        time2=hour+':'+minutes
        return [time1,time2]
        
