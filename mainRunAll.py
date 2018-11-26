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
sys.path.append('./SunMotionTools')

import os
import time
import numpy as np

from ReadMarcFile import *
from Triangulation import *
import SunMotionTools as sun

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


all_skin_depth = 0.1610

tasks = [
    {'outfile':"./data/ws15cm.out",  'diameter':0.15,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws20cm.out",  'diameter':0.20,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws25cm.out",  'diameter':0.25,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws30cm.out",  'diameter':0.30,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws40cm.out",  'diameter':0.40,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws50cm.out",  'diameter':0.50,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws63cm.out",  'diameter':0.625, 'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws75cm.out",  'diameter':0.75,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws88cm.out",  'diameter':0.875, 'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws100cm.out", 'diameter':1.00,  'skindepth':all_skin_depth, 'startAtInc':48},
    {'outfile':"./data/ws125cm.out", 'diameter':1.25,  'skindepth':all_skin_depth, 'startAtInc':84},
    {'outfile':"./data/ws150cm.out", 'diameter':1.50,  'skindepth':all_skin_depth, 'startAtInc':84},
    {'outfile':"./data/ws200cm.out", 'diameter':2.00,  'skindepth':all_skin_depth, 'startAtInc':168},
    {'outfile':"./data/ws300cm.out", 'diameter':3.00,  'skindepth':all_skin_depth, 'startAtInc':252},
    {'outfile':"./data/ws500cm.out", 'diameter':5.00,  'skindepth':all_skin_depth, 'startAtInc':504}
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

theSun = sun.SunMotion()      # default to Earth
theSun.setLatitude(35.2271)   # Charlotte, NC

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
            ###continue
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

    stressHistory = []

    while ( inc >= 0):
        inc = theModel.FindNextIncrement()
        if (inc < 0):
            break

        WeibullData = theModel.GetWeibullData()

        hour = (inc-task['startAtInc'])//4
        mins = ((inc-task['startAtInc'])%4)*15

        incTime = '{:02d}:{:02d}h'.format(hour, mins)

        # directional analysis plot
        filename1 = os.path.join(imagefolder, 'sigma-dir-{:03d}cm_inc{:03d}_{:02d}{:02d}.png'.format(int(diameter*100), inc, hour, mins))
        filename2 = os.path.join(imagefolder, 'dev-dir-{:03d}cm_inc{:03d}_{:02d}{:02d}.png'.format(int(diameter * 100), inc, hour, mins))
        filename3 = os.path.join(imagefolder, 'DBLE-dev-mean-dir{:03d}cm_inc{:03d}_{:02d}{:02d}.png'.format(int(diameter * 100), inc, hour, mins))
        filename4 = os.path.join(imagefolder, 'DBLE-sdir-top10-dir{:03d}cm_inc{:03d}_{:02d}{:02d}.png'.format(int(diameter * 100), inc, hour, mins))

        dirs    = theMesh.getDirections()
        pltData = theModel.GetDirData(dirs, inc)

        # extract surface directional extrema
        maxSigmaN = max(pltData['stress'])
        minSigmaN = min(pltData['stress'])

        stressHistory.append((float(hour)+float(mins)/60., maxSigmaN, minSigmaN))

        # set up plot information
        theSun.setDate(0., hour, mins, 0.)
        theMesh.setSun(theSun.getDir())

        ## theMesh.setData(pltData['deviator'],pltData['mean'])
        ## theMesh.setLabels('Deviator', 'mean stress')
        ## theMesh.createPolarPlot(filename1, 'time: {}'.format(incTime), 'MPa')
        ## theMesh.createStereoPlot(filename2, 'time: {}'.format(incTime), 'MPa')
        ## theMesh.createDoubleStereoPlot(filename3, 'time: {}'.format(incTime), 'MPa')

        theMesh.setData(pltData['stress'], pltData['top10'])
        theMesh.setLabels('Max normal stress', 'top 10% normal stress')
        theMesh.createStereoPlot(filename1, 'time: {}'.format(incTime), 'MPa')
        #theMesh.createDoubleStereoPlot(filename4, 'time: {}'.format(incTime), 'MPa')

        # clean up before moving to the next increment
        theModel.WipeIncrement(inc)

        # log message
        print("increment parsed  {:.2f}s:{:.2f}s".format(time.time() - time0, time.clock() - clock0))

    # wrapping up
    theModel.ReportClose()
    theModel.Close()

    # write stress history to file
    reportfileName = outfile[:-4] + "-history.csv"
    f = open(reportfileName,'w')
    for pt in stressHistory:
        f.write('{}, {}, {},\n'.format(*pt))
    f.close()

    t = []
    mx = []
    mn = []
    for pt in stressHistory:
        t.append(pt[0])
        mx.append(pt[1])
        mn.append(pt[2])


    plt.rc('grid', c='0.5', ls='-', lw=0.25)
    plt.rc('lines', lw=2, color='g')

    plt.fill([0.0] + t + [24.], [0.0] + anisotropyRatio + [0.0], 'r', alpha=0.25)
    plt.plot(t, anisotropyRatio, '-.r')
    plt.plot(t, mx, '-b')
    plt.plot(t, mn, '--g')

    ax = list(plt.axis())
    ax[0] = 0.0
    ax[1] = 24.0
    ax[2] = 0.0
    plt.axis(ax)

    # plt.xticks(range(25), ['00:00', '', '', '', '', '', '06:00', '', '', '', '', '', '12:00', '', '', '', '', '', '18:00', '', '', '', '', '', '24:00'])
    plt.xticks([0, 6, 12, 18, 24], ['00:00', '06:00', '12:00', '18:00', '24:00'])
    plt.minorticks_on()

    ax = plt.gca()
    ax.xaxis.set_minor_locator(MultipleLocator(1))

    plt.legend(('anisotropy ratio [1]', 'max driving stress [MPa]', 'min driving stress [MPa]'))

    plt.grid(True, which='major', axis='x')
    plt.grid(True, which='minor', axis='x')
    plt.grid(True, which='major', axis='y')

    reportPlotName = outfile[:-4] + "-history.png"
    plt.savefig(reportPlotName, dpi=300)
    plt.close()

    # clear processed data to avoid memory overload
    del theModel

