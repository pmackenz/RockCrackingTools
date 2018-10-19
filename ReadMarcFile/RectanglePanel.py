'''
Created on Dec 19, 2016

@author: Smit Kamal & Peter Mackenzie-Helnwein
'''

datapath = "../data/"

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from math import asin, pi
import numpy as np

        
class RectanglePanel(object):
    
    def __init__(self,ID=-1):
        
        
        self.Reset()
        
        self.fig = plt.figure(figsize=(10.0,5.0), dpi=200)
        
        self.initAxes()
        self.SetLimits()
        self.SetGrid()
        
    def initAxes(self):
        self.fig.clf(keep_observers=False)
        self.ax = self.fig.add_subplot(111, axisbg='#FFFFFF')
        self.SetLimits()
        self.SetGrid()
       

    def Clear(self):
        self.ax.cla()
        self.SetLimits()
        self.SetGrid()
        
    def SetLimits(self):
        self.ax.set_xlim(-10, 370)
        #self.ax.set_ylim(-95, 95)
        self.ax.set_ylim(-5, 95)
        
    def SetGrid(self):
        # major ticks every 20, minor ticks every 5   
                                           
        major_ticks = np.arange(0, 361, 45)                                              
        minor_ticks = np.arange(0, 361, 15)                                               
        
        self.ax.set_xticks(major_ticks)                                                       
        self.ax.set_xticks(minor_ticks, minor=True)
                                                   
        #major_ticks = np.arange(-90, 91, 30)                                              
        #minor_ticks = np.arange(-90, 91, 10)                                               
        
        major_ticks = np.arange(-0, 91, 30)                                              
        minor_ticks = np.arange( 0, 91, 10)                                               
        
        self.ax.set_yticks(major_ticks)                                                       
        self.ax.set_yticks(minor_ticks, minor=True)                                           
        
        # and a corresponding grid  
        self.ax.grid(which='both')                                                            
        
        # or if you want differnet settings for the grids:                               
        self.ax.grid(which='minor', alpha=0.2)                                                
        self.ax.grid(which='major', alpha=0.5)                                                

        
    def SetData(self, x, y, r, theta, val,dia,time, area=[]):
        if area == []:
            area = val
        self.dataX   = x
        self.dataY   = y
        self.dataR   = r
        self.dataTh  = theta
        self.dataArea = [ 10. * i for i in area ]
        self.dataVal = val
        self.initAxes()
        self.c = self.ax.scatter(self.dataX, self.dataY, c=self.dataVal, s=self.dataArea, linewidth=0,alpha=0.75)
        self.ax.set_title('{} cm diameter boulder at {} hours'.format(dia,time),y=1.07)
        cbr = self.fig.colorbar(self.c, pad=0.1, shrink=0.8)
        cbr.set_label('    MPa')
        plt.xlabel('longitude (degrees from north)')
        plt.ylabel('latitude (degrees)')
        self.SetLimits()
        self.SetGrid()
        #plt.show()
        
    def GetData(self):
        return (self.dataX[:], self.dataY[:], self.dataR[:], self.dataTh[:], self.dataVal[:], self.dataArea[:])
    
    def Reset(self):
        self.dataR    = []
        self.dataTh   = []
        self.dataVal  = []
        self.dataArea = []
        
    def saveplot(self,dia,inc):
        self.fig.savefig('{}{}_R_{}.pdf'.format(datapath,dia,inc))
        self.fig.savefig('{}{}_R_{}.png'.format(datapath,dia,inc))

        
