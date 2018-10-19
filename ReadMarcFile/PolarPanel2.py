'''
Created on Jun 14, 2017

@author: pmackenz
'''

datapath = "../data/"

from PolarPanel import *
from math import asin, pi
import numpy as np

class PolarPanel2(PolarPanel):
    '''
    classdocs
    '''


    def __init__(self,ID=-1):
        '''
        Constructor
        '''
        PolarPanel.__init__(self,ID)
        
        
    def SetLimits(self):
        self.ax.set_xlim(-180, 180)
        self.ax.set_ylim(0, 100)
        
    def SetGrid(self):
        # major ticks every 20, minor ticks every 5   
                                           
        major_ticks = np.arange(0, 2*np.pi, np.pi/6.) 
        self.ax.set_xticks(major_ticks)              
                                                   
        major_ticks = np.arange(0, 91, 30) 
        self.ax.set_yticks(major_ticks)                                                       
        
        # and a corresponding grid  
        self.ax.grid(which='both')                                                                 
        
        # or if you want differnet settings for the grids:                               
        self.ax.grid(which='minor', alpha=0.2)                                                
        self.ax.grid(which='major', alpha=0.5) 
        
    def SetData(self, x, y, r, theta, val,dia,time, area=[]):
        r2 = [180.0/pi*s for s in map(asin, r)]
        PolarPanel.SetData(self, x, y, r2, theta,val,dia,time, area)
         
    def saveplot(self,dia,inc):
        self.fig.savefig('{}{}_P2_{}.pdf'.format(datapath,dia,inc))
        self.fig.savefig('{}{}_P2_{}.png'.format(datapath,dia,inc))

