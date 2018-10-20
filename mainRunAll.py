#
# Created on May 12, 2015
# updated on May 22, 2017 by pmackenz
# updated on October 15, 2018 by pmackenz
#    adding integrated directional plot using triangulation mesh
#
# @author: pmackenz
#

import sys
sys.path.append('./Triangulation')
sys.path.append('./ReadMarcFile')

import os
import time
import numpy as np

from ReadMarcFile import *
from Triangulation import *

# for testing only: delete any csv file if it exists
os.system('rm -f ./data/ws50cm.csv')


all_skin_depth = 0.1610

tasks = [
    {'outfile':"./data/ws15cm.out",  'diameter':0.15,  'skindepth':all_skin_depth, 'startAtInc':1},
    {'outfile':"./data/ws20cm.out",  'diameter':0.20,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws25cm.out",  'diameter':0.25,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws30cm.out",  'diameter':0.30,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws40cm.out",  'diameter':0.40,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws50cm.out",  'diameter':0.50,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws63cm.out",  'diameter':0.625, 'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws75cm.out",  'diameter':0.75,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws88cm.out",  'diameter':0.875, 'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws100cm.out", 'diameter':1.00,  'skindepth':all_skin_depth, 'startAtInc':5},
    {'outfile':"./data/ws125cm.out", 'diameter':1.25,  'skindepth':all_skin_depth, 'startAtInc':84},
    {'outfile':"./data/ws150cm.out", 'diameter':1.50,  'skindepth':all_skin_depth, 'startAtInc':84},
    {'outfile':"./data/ws200cm.out", 'diameter':2.00,  'skindepth':all_skin_depth, 'startAtInc':168},
    {'outfile':"./data/ws300cm.out", 'diameter':3.00,  'skindepth':all_skin_depth, 'startAtInc':252},
    {'outfile':"./data/ws500cm.out", 'diameter':5.00,  'skindepth':all_skin_depth, 'startAtInc':336}
    ]

# make sure image folder exists

imagefolder = os.path.join('.','images')
if ( not os.path.exists(imagefolder) ):
    os.mkdir(imagefolder)
else:
    if ( not os.path.isdir(imagefolder) ):
        raise FileExistsError

# create triangulation for directional data visualization

theMesh = mesh.Mesh()
theMesh.createmesh(3)

# extract and process incremental stress data from MSC.marc output files

for task in tasks:

    outfile    = task['outfile']
    diameter   = task['diameter']
    skin_depth = task['skindepth']
    nskip      = task['startAtInc'] - 1

    if not os.path.exists(outfile):
        print("file: {} does not exist -- skipped".format(outfile))
        continue
    else:
        csvfile = "{}.csv".format(outfile[:-4])
        if os.path.exists(csvfile):
            print("file: {} already exists -- skipped".format(csvfile))
            continue
        else:
            print("file: {} does exist -- processing".format(outfile))

    # start processing the the output file
    time0  = time.time()
    clock0 = time.clock()

    theModel = OutFile.OutFile(outfile, diameter, skin_depth)
    print("file opened in        {:.2f}s:{:.2f}s".format(time.time() - time0, time.clock() - clock0))

    # set parameters for the Weibull analysis
    theModel.setParameters(sigma0=10., exponent_m=10., Vol0=1.0)

    theModel.setNskip(nskip)
    print("# of gauss points: {} resulting in volume = {}".format(theModel.countGaussPoints(), theModel.getVolume()))

    if nskip > 0:
        inc = theModel.FindIncrement(nskip)
        print("skipped {} increments {:.2f}s:{:.2f}s".format(nskip, time.time() - time0, time.clock() - clock0))
    else:
        inc = 0

    while ( inc >= 0):
        inc         = theModel.FindNextIncrement()
        WeibullData = theModel.GetWeibullData()

        incTime = '{:02d}:{:02d}h'.format((inc-task['startAtInc'])//4, 15*(inc-task['startAtInc'])%4)

        # directional analysis plot
        filename = os.path.join('.', 'images', 'dir{:03d}cm_inc{:03d}_{:02d}{:02d}.png'.format(int(diameter*100), inc,
                                                                                               (inc-task['startAtInc'])//4,
                                                                                               15*(inc-task['startAtInc'])%4))

        dirs = theMesh.getDirections()
        pltData = theModel.GetDirData(dirs)

        theMesh.setData(pltData)
        theMesh.createPolarPlot(filename, 'time: {}'.format(incTime))

        # clean up before moving to the next increment
        theModel.WipeIncrement(inc)

        # log message
        print("increment parsed  {:.2f}s:{:.2f}s".format(time.time() - time0, time.clock() - clock0))

    # wrapping up
    theModel.ReportClose()
    theModel.Close()
    
    # clear processed data to avoid memory overload
    del theMesh

