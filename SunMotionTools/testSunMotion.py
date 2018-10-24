from sunmotion import *
import pylab

theSun = SunMotion(distance=150)            # default to Earth
theSun.setLatitude(35.2271)     # Charlotte, NC
#theSun.setLatitude(30.00)     # Charlotte, NC

time = []
x = []
y = []
z = []

f = open('sun.csv','w')

for i in range(24*4):
    hour = i // 4
    mins = (i % 4) * 15

    incTime = '{:02d}:{:02d}h'.format(hour, mins)

    theSun.setDate(0., hour, mins, 0.)

    d = theSun.getDir()

    data = '{},{},{},{},{}\n'.format(incTime, hour+mins/60., d[0], d[1], d[2])
    f.write(data)

    time.append(hour+mins/60.)
    x.append(-d[0])
    y.append(d[1])
    z.append(d[2])

f.close()

pylab.plot(time,x,'-',color='red',  label='West')
pylab.plot(time,y,'-',color='green',label='North')
pylab.plot(time,z,'-',color='blue', label='Up')
pylab.grid(True)
pylab.legend(loc='upper left')
pylab.show()


