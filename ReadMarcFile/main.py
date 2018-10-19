'''
Created on May 12, 2015

@author: pmackenz
'''
from readfile import *
import time

if __name__ == '__main__':
    pass

#outfile = "../data/WS100cm_job1.out"
#outfile = "../data/ws200b_job1.out"
#outfile = "../data/ws250b_job1.out"
#outfile = "../data/Demo.out"
outfile = "../data/ws150b_job1.out"
#outfile = "../data/ws500g_job3.out"
#outfile = "../data/Sphere_job1.out"
#outfile = "../data/Sphere_job2.out"
#outfile = "../data/Sphere_job3.out"

diameter   = 1.50
skin_depth = 0.1610

time0 = time.time()
clock0 = time.clock()

data = OutFile(outfile, diameter, skin_depth)
print "file opened in        {:.2f}s:{:.2f}s".format(time.time() - time0, time.clock() - clock0)

data.setParameters(sigma0=10., exponent_m=10., Vol0=1.0)
#data.setParameters(sigma0=30., exponent_m=10., Vol0=1.0)
#data.setParameters(sigma0=3., exponent_m=10., Vol0=1.0)

print "# of gauss points: {} resulting in volume = {}".format(data.countGaussPoints(), data.getVolume())

#inc = data.FindIncrement(2)
#print "skipped 2 increments {:.2f}s:{:.2f}s".format(time.time() - time0, time.clock() - clock0)


nskip = 48
nskip = 24
nskip = 0
#nskip = 120

if nskip > 0:
    inc = data.FindIncrement(nskip)
    print "skipped {} increments {:.2f}s:{:.2f}s".format(nskip, time.time() - time0, time.clock() - clock0)
else:
    inc = 0

while ( inc >= 0):
    if (inc > 48):
        #break
        pass
    
    inc = data.FindNextIncrement()
    WeibullData = data.GetWeibullData(inc)
    
    data.WipeIncrement(inc)
    print "increment parsed  {:.2f}s:{:.2f}s".format(time.time() - time0, time.clock() - clock0)
    #break
    pass

data.ReportClose()

#incData = data.GetIncrement(144)
#data.verifyIncrementData(48)
#data.verifyIncrementData(49)



incData = data.GetIncrement(400)
incData.Print()
print incData.getVolume()
print incData.getWeibullB()
incData.checkIntegrity()
print "integrity check       {:.2f}s:{:.2f}s".format(time.time() - time0, time.clock() - clock0)

data.Close()
