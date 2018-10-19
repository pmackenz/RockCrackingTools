'''
Created on Jun 14, 2017

@author: pmackenz
'''

datapath = "../data/"

from PolarPanel import *
class PolarPanel1(PolarPanel):
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
        self.ax.set_ylim(0, 1.1)
        
    def saveplot(self,dia,inc):
        self.fig.savefig('{}{}_P1_{}.pdf'.format(datapath,dia,inc))
        self.fig.savefig('{}{}_P1_{}.png'.format(datapath,dia,inc))
        
 
