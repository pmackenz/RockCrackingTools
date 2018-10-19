'''
Created on Jun 14, 2017

@author: Smit
'''
import numpy as np
from math import asin, cos, atan2, sqrt, pi
from PolarPanel import *
from PolarPanel1 import *
from PolarPanel2 import *
from RectanglePanel import *

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


class StressPlots(object):
    '''
    classdocs
    '''


    def __init__(self, file, dia, time1, time2):
        '''
        Constructor
        '''
        # this function needs to load a file and initialize data for the plot panels.
        x = []
        y = []
        r = []
        th = []
        val = []
        
        f = open(file,'r')
                
        hdr = f.readline()
                
        for line in f:
            items = line.rstrip('\n').split('\t')
            vals = map(float, items)
            pos = np.array(vals[0:3])
            dir = np.array(vals[3:6])
            if dir[1] < 0:
                dir = -dir
            mag = vals[6]
                # x is North
                # y is UP
                # Z is East
            radius = sqrt(dir[0]*dir[0] + dir[2]*dir[2])

            if r > 1.000:
                ln = np.linalg.norm(dir)
                dir /= ln
                radius /= ln
            theta = atan2(-dir[0], dir[2])
            if theta < 0.0:
                theta += 2.*pi
                    
            x.append(theta*180./pi)
            y.append(atan2(dir[1],radius)*180./pi)
            r.append(radius)
            th.append(theta)
            val.append(mag)
            
        f.close()
                
        maxVal = np.max(val)
        m = 5.
        area = [ ((1.+1./m)*v/maxVal)**m for v in val ]  
        
        b = PolarPanel2()
        b.SetData(x, y, r, th, val, dia, time2, area)
        b.saveplot(dia, time1)
        b.Clear()
        del b

        c = RectanglePanel()
        c.SetData(x, y, r, th, val, dia, time2, area)
        c.saveplot(dia, time1)
        c.Clear()
        del c
        

        
#StressPlots('75_direction_1130.txt',75,'1130','11:30')

    
