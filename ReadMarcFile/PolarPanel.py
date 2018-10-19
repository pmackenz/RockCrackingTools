'''
Created on Jun 14, 2017

@author: Smit
'''

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


class PolarPanel(object):
    '''
    classdocs
    '''


    def __init__(self,ID=-1):
        
        '''
        Constructor
        '''
        self.fig = plt.figure(figsize=(6.0,5.0), dpi=200)
        self.initAxes()
        self.Reset()
        
    def initAxes(self):
        self.fig.clf(keep_observers=False)
        self.ax = self.fig.add_subplot(111,projection='polar')
        self.ax.set_theta_zero_location("N")
        self.ax.set_theta_direction(-1)
        self.SetLimits()
        self.SetGrid()
    
    def SetLimits(self):
        # this will be overloaded in derived classes
        pass
    
    def SetGrid(self):
        # this will be overloaded in derived classes
        self.ax.grid(True)
  
    def SetData(self, x, y, r, theta, val,dia,time, area=[]):
        
        if area == []:
            area = val
        self.dataX   = x
        self.dataY   = y
        self.dataR   = r
        self.dataTh  = theta
        self.dataVal = val
        self.dataArea = [ 10.*k for k in area ]
        self.initAxes()
        self.c = self.ax.scatter(self.dataTh, self.dataR, c=self.dataVal, s=self.dataArea, linewidth=0,alpha=0.75)
        self.ax.set_title("{} cm diameter boulder at {} hours".format(dia,time),y=1.07)
        cbr = self.fig.colorbar(self.c,pad=0.1,shrink=0.8)
        cbr.set_label('    MPa')
        self.SetLimits()
        self.SetGrid()
        #plt.show()
        
    def Reset(self):
        self.dataR    = []
        self.dataTh   = []
        self.dataVal  = []
        self.dataArea = []   
    
    def Clear(self):
        self.ax.cla()
        self.ax.set_theta_zero_location("N")
        self.ax.set_theta_direction(-1)
        self.SetLimits()
        self.SetGrid()
        

        
    
