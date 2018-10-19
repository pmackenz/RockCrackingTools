'''
Created on May 15, 2015

@author: pmackenz
'''
from MyElementData import *
from MyErrors      import *
from ExtremeValue  import *
from MyTensor      import *
from StressPlots   import *
from numpy         import array, inf

class MyIncrement(object):
    '''
    variables:
        self.ID        = id
        self.elements  = {}
        self.nodes     = {}
        self.volume    = array([0.,0.,0.,0.,0.,0.,0.])
        self.scannedVolume   = False
        self.scannedWeibullB = False
        self.nSegments = nSegments     # (int)
        self.diameter  = diameter      # (float)
        self.delta     = skin_depth    # (float)
        self.sigma0    = sigma0        # (float)
        self.m         = exponent_m    # (float)
        self.Vol0      = Vol0          # (float)
        self.volume    = zeros(nSegments)
        self.weibullB  = zeros(nSegments)
        self.radii     = array()
        self.nextline  = ""
        self.maxValues = {}
        self.minValues = {}
    
    methods:
        __init__(self, id=-1)
        __str__(self)
        Print(self,cnt=1)
        setParameters(self, diameter, skin_depth, sigma0, exponent_m, V0)
        setID(self, id)
        getID(self)
        getElement(self,id)
        addElement(self,elem)
        parse(self)
        scanThermalResults(self,file)scanNodalPointData(self, file)
        addNodeData(self, ndID, ndTemp)
        scanStructuralResults(self,file)
        ParseCauchy(self,line,gaussPoint)
        ParseLogstn(self,line,gaussPoint)
        ParseThermal(self,line,gaussPoint)
        checkIntegrity(self)
        checkElem(self, elemID, gaussPoints, keywords)
        updateElementInfo(self, elemInfo)
        scanVolume(self)
        getVolume(self)
        scanWeibullB(self)
        getWeibullB(self)
        getWeibullData(self)
        getProbabilities(self)
        printProbabilities(self)
        verifyElementData(self, refElements)
    '''

    def __init__(self, id=-1):
        '''
        Constructor
        '''
        
        self.ID        = id
        self.elements  = {}
        self.nodes     = {}
        self.scannedVolume   = False
        self.scannedWeibullB = False
        self.nextline  = ""
        self.maxValues = {'pos':array([0.0,0.0,0.0])}
        self.minValues = {'pos':array([0.0,0.0,0.0])}
        
        self.setParameters()    # set default parameters
        
        keywords = ['Cauchy','Logstn','thermal']
        for key in keywords:
            self.maxValues[key] = {'tensor':array([-inf,-inf,-inf,-inf,-inf,-inf]), 'princval':array([-inf,-inf,-inf])}
            self.minValues[key] = {'tensor':array([ inf, inf, inf, inf, inf, inf]), 'princval':array([ inf, inf, inf])}
        
    def __str__(self):
        txt = "increment {}:\n".format(self.ID)
        for elem in self.elements:
            txt += str(self.elements[elem]) + "\n"
            break
        return txt
    
    def setParameters(self, diameter=10000.0, skin_depth=100000.0, sigma0=1000000.0, exponent_m=1.0, Vol0=1.0):
        
        self.diameter = diameter
        self.delta    = skin_depth
        self.sigma0   = sigma0
        self.m        = exponent_m
        self.Vol0     = Vol0
        
        if diameter < 0.001:
            diameter = 0.001
        if skin_depth < 0.0005:
            skin_depth = 0.5*(diameter + 0.001)
        
        self.delta     = skin_depth
        nSegments = int(ceil(0.5*diameter/skin_depth))
        
        self.nSegments = nSegments
        
        self.volume    = zeros(nSegments+1) # the extra entry is for counting gauss points
        self.weibullB  = zeros(nSegments)
        self.radii     = 0.50*self.diameter - arange(nSegments)*self.delta  
        
        self.scannedWeibullB = False
        
    def Print(self,cnt=1):
        ecnt = 0
        print("increment {}:".format(self.ID))
        for elem in sorted(self.elements):
            # element identification
            id =  self.elements[elem].getID()
            print("- element {}:".format(id))
            
            # element data per gauss point
            for idx in range(8):
                print("--- GP {}:".format(idx+1))
                print("      position: {}, volume: {:.3g} at r: {}".format(self.elements[elem].getGPposition(idx),
                                                                           self.elements[elem].getGPvolume(idx),
                                                                           self.elements[elem].getGPdistance(idx)))
                data = self.elements[elem].getData(idx+1)
                for key in data.keys():
                    print("   {}:".format(key))
                    if type(data[key]) == dict:
                        for item in data[key].keys():
                            print("       {}: {}".format(item, data[key][item]))
                        continue
                    else:
                        print("       value is: {}".format(data[key]))
                
            ecnt += 1
            if (ecnt >= cnt):
                break
        
    def setID(self, id):
        self.ID = id 
        
    def getID(self):
        return self.ID
    
    def getElement(self,id):
        return self.elements[id]
    
    def addElement(self,elem):
        if (type(elem) != MyElement):
            print("element variable of wrong type: ", type(elem))
        self.elements[elem.getID()] = elem
        
    def parse(self, file):
        for self.line in file:
            if (self.line.find("                              Thermal Results") == 0):
                print("increment {}: found thermal data".format(self.ID))
                # scan thermal data"
                self.line = self.scanThermalResults(file)
                
            if (self.line.find("                              Structural Results") == 0):
                print("increment {}: found structural data".format(self.ID))
                # scan structural data"
                self.line = self.scanStructuralResults(file)
                
            if (self.line.find("n o d a l   p o i n t   d a t a") > 0):
                print("increment {}: found nodal point data".format(self.ID))
                # scan structural data"
                self.line = self.scanNodalPointData(file)
                
            if (self.line.find("e n d   o f   i n c r e m e n t") >= 0):
                break
            
        # done parsing, now do some post processing
       
    def scanThermalResults(self,file):
        for newline in file:
            self.line = newline
            break    
        return self.line
    
    def scanNodalPointData(self, file):
        self.line = ""
        
        for newline in file:
            if (newline.find("t o t a l   n o d a l   t e m p e r a t u r e s") > 0):
                break
            if (newline.find("e n d   o f   i n c r e m e n t") > 0):
                self.line = newline
                return self.line
            
        ignore_empty = True
            
        for newline in file:
            if (newline.strip() == "" and ignore_empty):
                continue
            if (newline.strip() == ""):
                break
            ignore_empty = False
            
            #print newline
            if (len(newline) >= 30):
                nodeID   = int(newline[0:17])
                nodeTemp = float(newline[17:30])
                #print '{}:{}'.format(nodeID, nodeTemp)
                self.addNodeData(nodeID, nodeTemp)
            if (len(newline) >= 60):
                nodeID   = int(newline[30:47])
                nodeTemp = float(newline[47:60])
                #print '{}:{}'.format(nodeID, nodeTemp)
                self.addNodeData(nodeID, nodeTemp)
            if (len(newline) >= 90):
                nodeID   = int(newline[60:77])
                nodeTemp = float(newline[77:90])
                #print '{}:{}'.format(nodeID, nodeTemp)
                self.addNodeData(nodeID, nodeTemp)
            if (len(newline) >= 120):
                nodeID   = int(newline[90:107])
                nodeTemp = float(newline[107:120])
                #print '{}:{}'.format(nodeID, nodeTemp)
                self.addNodeData(nodeID, nodeTemp)
            if (len(newline) >= 150):
                nodeID   = int(newline[120:137])
                nodeTemp = float(newline[137:150])
                #print '{}:{}'.format(nodeID, nodeTemp)
                self.addNodeData(nodeID, nodeTemp)
        
        self.line = newline
        return self.line
    
    def addNodeData(self, ndID, ndTemp):
        if (ndID in self.nodes):
            print("Node {} already exists".format(ndID))
        else:
            self.nodes[ndID] = {"id":ndID, "temp":ndTemp}
        pass
        
    def scanStructuralResults(self,file):
        '''
         element      13536  point   6       integration pt. coordinate=     0.441E-01    0.193E+00   -0.278E-01
        ----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|
         Cauchy  8.826E-02 8.317E-02-2.710E-02-8.216E-02-5.252E-03 6.106E-03-1.623E-02-5.756E-02-7.509E-03-3.271E-02 1.657E-02 1.569E-02
         Logstn  2.131E-06 2.599E-05 1.835E-05 1.702E-05 1.888E-05 1.916E-05 1.862E-05 1.762E-05 1.883E-05-1.580E-06 8.001E-07 7.576E-07
         thermal 0.000E+00 2.627E-05 1.858E-05 1.858E-05 1.858E-05 1.858E-05 1.858E-05 1.858E-05 1.858E-05 0.000E+00 0.000E+00 0.000E+00
        '''
        keywords = ['Cauchy','Logstn','thermal']
        
        for self.line in file:
            if (self.line.find('e n d   o f   i n c r e m e n t') > 0):
                break
            if (self.line.find('element') == 1):
                
                id = int(self.line[8:19])
                point = int(self.line[26:30])
                
                if id != 145:
                    continue
                
                if (id in self.elements):
                    self.newelement = self.elements[id]
                else:
                    self.newelement = MyElementData(id, data=[{},{},{},{},{},{},{},{}])
                    
                gaussPointData = {}
                gaussPointData['coord'] = array([float(self.line[65:78]),float(self.line[78:91]),float(self.line[91:104])])
                
                for nextline in file:
                    if nextline.strip() == "":
                        '''
                        this could be the end of this element entry, but also just a page break.
                        '''
                        continue
                    
                    if (nextline.find('element') == 1):
                        '''
                        we definitely found another element entry and need to restart the element block parsing
                        '''
                        #self.newelement.setData(point, gaussPointData.copy()) 
                        self.newelement.setData(point, gaussPointData) 
                        gaussPointData = {}
                        self.elements[id] = self.newelement
                
                        self.line = nextline
                        
                        id = int(self.line[8:19])
                        point = int(self.line[26:30])
                        
                        if id == 17899 and self.ID >48:
                            pass
                        
                        if (id in self.elements):
                            self.newelement = self.elements[id]
                        else:
                            self.newelement = MyElementData(id, data=[{},{},{},{},{},{},{},{}])
                            
                        gaussPointData['coord'] = array([float(self.line[65:78]), float(self.line[78:91]), float(self.line[91:104])])
                        continue
                    
                    if (nextline.find('e n d   o f   i n c r e m e n t') > 0):
                        self.line = nextline
                        break
                    
                    if (nextline.find("n o d a l   p o i n t   d a t a") > 0):
                        '''
                        reading past the last element.
                        we need to preserve this line for it is a keyword
                        '''
                        self.line = nextline
                        break
                    
                    if (nextline.find('Cauchy') == 1):
                        self.ParseCauchy(nextline,gaussPointData)
                        self.checkMinMax('Cauchy', self.newelement.getID(), gaussPointData)
                    if (nextline.find('Logstn') == 1):
                        self.ParseLogstn(nextline,gaussPointData)
                        self.checkMinMax('Logstn', self.newelement.getID(), gaussPointData)
                    if (nextline.find('thermal') == 1):
                        self.ParseThermal(nextline,gaussPointData)
                        self.checkMinMax('thermal', self.newelement.getID(), gaussPointData)
        
                self.newelement.setData(point, gaussPointData)
                gaussPointData = {}     # making sure
                self.elements[id] = self.newelement
                self.newelement = {}    # just to be safe
                
            if (self.line.find('e n d   o f   i n c r e m e n t') > 0):
                break
            if (self.line.find("n o d a l   p o i n t   d a t a") > 0):
                break
            
        return self.line
            
    def ParseCauchy(self,line,gaussPointData):
        '''
         Cauchy  8.826E-02 8.317E-02-2.710E-02-8.216E-02-5.252E-03 6.106E-03-1.623E-02-5.756E-02-7.509E-03-3.271E-02 1.657E-02 1.569E-02
        ----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|
        '''
        tresca = float(line[ 8:18])
        mises  = float(line[18:28])
        mean   = float(line[28:38])
        sig1   = float(line[38:48])
        sig2   = float(line[48:58])
        sig3   = float(line[58:68])
        sx     = float(line[68:78])
        sy     = float(line[78:88])
        sz     = float(line[88:98])
        txy    = float(line[98:108])
        tyz    = float(line[108:118])
        tzx    = float(line[118:128])
        
        gaussPointData['Cauchy'] = {'tensor':MyTensor([sx,sy,sz,txy,tyz,tzx]),'princvals':array([sig1,sig2,sig3])}
    
    def ParseLogstn(self,line,gaussPointData):
        '''
         Logstn  2.131E-06 2.599E-05 1.835E-05 1.702E-05 1.888E-05 1.916E-05 1.862E-05 1.762E-05 1.883E-05-1.580E-06 8.001E-07 7.576E-07
        ----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|
        '''
        tresca = float(line[ 8:18])
        mises  = float(line[18:28])
        mean   = float(line[28:38])
        eps1   = float(line[38:48])
        eps2   = float(line[48:58])
        eps3   = float(line[58:68])
        ex     = float(line[68:78])
        ey     = float(line[78:88])
        ez     = float(line[88:98])
        gxy    = float(line[98:108])
        gyz    = float(line[108:118])
        gzx    = float(line[118:128])
        
        gaussPointData['Logstn'] = {'tensor':array([ex,ey,ez,gxy,gyz,gzx]),'princvals':array([eps1,eps2,eps3])}
        
    def ParseThermal(self,line,gaussPointData):
        '''
         thermal 0.000E+00 2.627E-05 1.858E-05 1.858E-05 1.858E-05 1.858E-05 1.858E-05 1.858E-05 1.858E-05 0.000E+00 0.000E+00 0.000E+00
        ----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|----.----|
        '''
        tresca = float(line[ 8:18])
        mises  = float(line[18:28])
        mean   = float(line[28:38])
        eps1   = float(line[38:48])
        eps2   = float(line[48:58])
        eps3   = float(line[58:68])
        ex     = float(line[68:78])
        ey     = float(line[78:88])
        ez     = float(line[88:98])
        gxy    = float(line[98:108])
        gyz    = float(line[108:118])
        gzx    = float(line[118:128])
        
        gaussPointData['thermal'] = {'tensor':array([ex,ey,ez,gxy,gyz,gzx]),'princvals':array([eps1,eps2,eps3])}
         
    def checkIntegrity(self):
        
        keywords = ['Cauchy','Logstn','thermal']
        
        for elem in sorted(self.elements.keys()):
            if (self.elements[elem].has_data()):
                self.checkElem(self.elements[elem].getID(), self.elements[elem].getData(), keywords)
            else:
                msg = "warning: element {} is missing data".format(self.elements[elem].getID())
                raise DataIntegrityError(msg)
            
        # verify we have temperature data for every node
        cnt = 0
        for node in sorted(self.nodes.keys()):
            if node > 0:
                if (self.nodes[node].has_key('temp')):
                    cnt += 1
                else:
                    msg = "warning: node {} is missing data".format(self.nodes[node]['id'])
                    raise DataIntegrityError(msg)
        
        nNodes = len(self.nodes)
        if ( cnt != nNodes):
            msg = "Error: increment has {} nodes but only {} nodes have data".format(nNodes,cnt)
            raise DataIntegrityError(msg)
            
    def checkElem(self, elemID, gaussPoints, keywords):
        if (len(gaussPoints) != 8):
            msg = "warning: element {} has {} gauss points instead of 8".format(elemID, len(gaussPoints))
            raise DataIntegrityError(msg)
            
        for gp in range(len(gaussPoints)):
            data = gaussPoints[gp]
            for key in keywords:
                if ( not data.has_key(key)):
                    msg = "warning: element {} is missing data for {} at GP {}".format(elemID,key,gp+1)
                    print(msg)
                    #raise DataIntegrityError(msg)
                
    def checkMinMax(self, key, elemID, gaussPoint):
        pass
    
    def updateElementInfo(self, elemInfo):
        # elemInfo is a dictionary of MyElement objects carrying volume, 
        # position, and distance information.
        # this information was computed for increment 0 and needs to be copied into increment data
        #
        # DO NOT MODIFY elemInfo !
        for elem in elemInfo:
            if (elem in self.elements):
                GPinfo = elemInfo[elem].getGPinfo()
                self.elements[elem].setGPinfo(GPinfo)
                                
    def scanVolume(self):
        if not self.scannedVolume:
            for elem in self.elements:
                self.elements[elem].scanVolume(self.volume, self.radii)
            self.scannedVolume = True
        return sum(self.volume[:len(self.radii)])
    
    def getVolume(self):
        if not self.scannedVolume:
            self.scanVolume()
        return {'volume':sum(self.volume[:self.nSegments]), 'subvolume':self.volume, 'limits':self.radii}
    
    def scanWeibullB(self):
        if not self.scannedWeibullB:
            self.weibullB  = zeros(self.nSegments)
            for elem in self.elements:
                self.elements[elem].scanWeibullB(self.weibullB, self.radii, self.sigma0, self.m)
            self.scannedWeibullB = True
        return sum(self.weibullB)
    
    def getWeibullB(self):
        if not self.scannedWeibullB:
            self.scanWeibullB()
        return {'Weibull B':sum(self.weibullB), 'Weibull B for subvolume':self.weibullB, 'limits':self.radii}
    
    def ScanStress(self,filename):
        try:
            filename_dir = filename
            file_dir = open(filename_dir, 'w')
        except:
            print("cannot create stress file for writing")
            return
        
            
        s = "X\tY\tZ\tx_dir\ty_dir\tz_dir\tvalue\tincrement"
        s += "\n"
        file_dir.write(s)
        file_dir.close()
        file_dir=open(filename_dir, 'a')
        for elem in self.elements:
            values=self.elements[elem].scanGPstress(self.ID)
            for x in values:
                #word=str(x['pos_x'])+'\t'+str(x['pos_y'])+'\t'+str(x['pos_z'])+'\t'+str(x['dir_x'])+'\t'+str(x['dir_y'])+'\t'+str(x['dir_z'])+'\t'+str(x['value'])+'\t'+str(x['increment'])
                word="{pos_x:16.10f}\t{pos_y:16.10f}\t{pos_z:16.10f}\t{dir_x:16.10f}\t{dir_y:16.10f}\t{dir_z:16.10f}\t{value:16.10f}\n".format(**x)
                file_dir.write(word)
        file_dir.close()        
                    
    def PlotStressDirection(self,filename,dia,time1,time2):
        plts = StressPlots(filename,dia,time1,time2)
        del plts
        
    def getWeibullData(self):
        props = {}
        self.getProbabilities(props)
        return props
    
    def getProbabilities(self, props):
        if not self.scannedVolume:
            self.scanVolume()
        if not self.scannedWeibullB:
            self.scanWeibullB()
            
        props['nSegments'] = self.nSegments
        props['limits'] = self.radii
        props['volume'] = self.volume
        props['WeibullB'] = self.weibullB
        props['POSlayers'] = exp(-self.weibullB)
        props['POFlayers'] = 1.0 - exp(-self.weibullB)
        props['POS'] = exp(-sum(self.weibullB))
        props['POF'] = 1.0 - props['POS']
        
    def printProbabilities(self):
        props = {}
        self.getProbabilities(props)
        print("layer    max R   min R  volume          B             POS             POF")
        for i in range(len(props['limits'])):
            
            if i>=len(props['limits'])-2:
                lower = 0.0
            else:
                lower = props['limits'][i+1]
                
            print("{:3d}   {:8.3f}{:8.3f}{:8.4g}{:16.13f}{:16.13f}{:16.13f}".format(i,
                                                props['limits'][i],
                                                lower,
                                                props['volume'][i],
                                                props['WeibullB'][i],
                                                props['POSlayers'][i],
                                                props['POFlayers'][i]) )
            
        print("------------------------------------------------------------------------------")
        print("total {:8.3f}{:8.3f}{:8.4g}{:16.13f}{:16.13f}{:16.13f}".format(
                                                props['limits'][0],
                                                0.0,
                                                sum(props['volume']),
                                                sum(props['WeibullB']),
                                                props['POS'],
                                                props['POF']) )
    
    def verifyElementData(self, refElements):
        allElemIDs  = refElements.keys()
        wildElemIDs = []
        for elem in self.elements:
            if elem in allElemIDs:
                idx = allElemIDs.index(elem)
                del allElemIDs[idx]
            else:
                wildElemIDs.append(elem)
        
        if len(wildElemIDs) == 0 and len(allElemIDs) == 0:
            return True
        else:
            print("unused elements: {}".format(allElemIDs) )
            print("extra elements:  {}".format(wildElemIDs))
            return False
