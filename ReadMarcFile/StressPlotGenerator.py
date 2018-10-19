'''
Created on Jun 20, 2017

@author: Smit
revised: Oct 17, 2018 by Peter Mackenzie-Helnwein
'''

from StressPlots import *

def InctoTime(inc):
    h   = inc * 0.25
    hr  = int(h)
    m   = (h-hr)*60
    min = int(m)
    
    hour    = '{:02d}'.format(hr)
    minutes = '{:02d}'.format(min)

    time1 = hour + minutes
    time2 = hour + ':' + minutes
    return [time1,time2]


if (__name__ == '__main__'):
    time1_array=[]
    time2_array=[]
    for i in range(0,97):
        [time1,time2]=InctoTime(i)
        time1_array.append(time1)
        time2_array.append(time2)

    boulder_dia=[30]

    for i in boulder_dia:
        k = 0
        for j in time1_array:
            filename="./data/{}_direction_.bak/{}_direction_{}.txt".format(i,i,j)
            StressPlots(filename,i,j,time2_array[k])

            print( i, time2_array[k] )
            k += 1






