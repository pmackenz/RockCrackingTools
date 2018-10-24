'''
Created on May 10, 2017

@author: pmackenz
'''

from numpy import array, zeros
from MyElement import *

class MyElementData(MyElement):
    '''
    classdocs: 
        all of MyElement plus the following
    
    variable:
        self.data
        
    methods:
        __init__(self, id=-1, connect=[0,0,0,0,0,0,0,0], data=[{},{},{},{},{},{},{},{}])
        getData(self, gp)
        setData(self, gp, gpData)
        has_data(self)
        scanWeibullB(self, weibullBArray, limits, sigma0=1.0, m=1.0)
        scanDirData(self, directions)
    '''

    def __init__(self, id=-1, connect=[0,0,0,0,0,0,0,0], data=[{},{},{},{},{},{},{},{}]):
        '''
        Constructor
        '''
        super(MyElementData, self).__init__(id, connect)
        self.data = data
               
    def getData(self, gp=0):
        if (gp-1) in range(8):
            return self.data[gp-1]
        else:
            return self.data
    
    def setData(self, gp, gpData):
        if (gp-1) in range(8):
            self.data[gp-1] = gpData
               
    def has_data(self):
        if len(self.data) != 8:
            return False
        
        for item in self.data:
            if len(item) == 0:
                return False
        
        return True
    
    def scanWeibullB(self, weibullBArray, limits, sigma0=1.0, m=1.0):
        for pt in self.gps:
            idx = len(limits) - 1
            dist = self.gps[pt].getDist()
            
            # find proper segment
            while dist > limits[idx]:
                idx -= 1
                if idx<0:
                    idx = 0
                    break
                
            # add integrand
            if dist <= limits[0]:
                val = self.data[pt-1]['Cauchy']['tensor'].getWeibullB(sigma0, m)
                weibullBArray[idx] += val * self.gps[pt].getVol()
            else:
                print("element {}: gauss point outside boulder!".format(self.ID) )
                
    def scanGPstress(self,inc):
        
        GP_values=[]
        
        for pt in self.gps:
            position = self.gps[pt].getPos()
            
            val = self.data[pt-1]['Cauchy']['tensor'].getMaxVal()
            if val > 0.0:
                dir = self.data[pt-1]['Cauchy']['tensor'].getMaxDir()
                GP_values.append({'pos_x':position[0],'pos_y':position[1],'pos_z':position[2], 'dir_x':dir[0], 'dir_y':dir[1], 'dir_z':dir[2],'value':val,'increment':inc})
            
            val = self.data[pt-1]['Cauchy']['tensor'].getMedVal()
            if val > 0.0:
                dir = self.data[pt-1]['Cauchy']['tensor'].getMedDir()
                GP_values.append({'pos_x':position[0],'pos_y':position[1],'pos_z':position[2], 'dir_x':dir[0], 'dir_y':dir[1], 'dir_z':dir[2],'value':val,'increment':inc})
            
            val = self.data[pt-1]['Cauchy']['tensor'].getMinVal()
            if val > 0.0:
                dir = self.data[pt-1]['Cauchy']['tensor'].getMinDir()
                GP_values.append({'pos_x':position[0],'pos_y':position[1],'pos_z':position[2], 'dir_x':dir[0], 'dir_y':dir[1], 'dir_z':dir[2],'value':val,'increment':inc})
        
        return GP_values
            
            
    def scanDirData(self, directions, dirData):

        for pt in self.gps:
            for i in range( len(directions) ):
                #(sigma, tau) = self.data[pt-1]['Cauchy']['tensor'].getSigmaTau(directions[i])
                (sigma, tau) = self.data[pt-1]['Cauchy']['deviator'].getSigmaTau(directions[i])

                # target function
                f = sigma

                # use max-value criterion
                if ( f > dirData[i] ):
                    dirData[i] = f

        