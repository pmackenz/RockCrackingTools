#
# author: Peter Mackenzie-Helnwein
#
# date: Oct 23, 2018
#

from numpy import array, dot, sqrt, pi, sin, cos, deg2rad

class SunMotion(object):
    '''
    :class: SunMotion

    variables:
        self.d = distance           # distance planet to sun in km
        self.year = year*day        # days per year; self.year is hours per year
        self.day  = day             # hours per day
        self.Omega = 1./self.year   # angular velocity for orbit around the sun
        self.om    = 1./day         # angular velocity axis spin
        self.time                   # current time in hours from winter solstice
        self.latitude = 0.0         # latitude of point of interest in degrees north

    methods:
        def __init__(self, distance=149597500., year=365.25, day=24., tilt=23.5)
        def __str__(self)
        def __repr__(self)
        def setLatitude(self, lat)
        def setDate(self, day, hour, minutes, seconds)
        def getUp(self)
        def getEast(self)
        def getWest(self)
        def getNorth(self)
        def getSouth(self)
        def getDir(self)
    '''

    def __init__(self, distance=150000., year=365.25, day=24., tilt=23.43685):
        # default values are set for Earth
        self.d        = distance
        self.year     = year*day
        self.day      = day
        self.om       = 2.*pi/self.year
        self.Omega    = 2.*pi/day
        self.time     = 0.0
        self.psi      = deg2rad(tilt)
        self.latitude = 0.0

    def __str__(self):
        return "SunMotion({},year={},day={})".format(self.d, self.year / self.day, self.day)

    def __repr__(self):
        return "SunMotion({},year={},day={})".format(self.d, self.year/self.day, self.day)

    def setLatitude(self, lat):
        self.latitude = deg2rad(lat)

    def setDate(self, day, hour, minutes, seconds):
        self.time = day*self.day + hour + (minutes + seconds/60.)/60.

    def getWest(self):
        x = cos(self.time * (self.om + self.Omega)) * sin(self.time * self.om)
        x -= cos(self.psi) * cos(self.time * self.om) * sin(self.time * (self.om + self.Omega))
        x *= self.d
        return x

    def getNorth(self):
        y  = cos(self.psi)*cos(self.time*self.om)* cos(self.time*(self.Omega + self.om))* sin(self.latitude)
        y -= cos(self.latitude) * cos(self.time*self.om) * sin(self.psi)
        y += sin(self.latitude) * sin(self.time*self.om) * sin(self.time*(self.Omega + self.om))
        y *= self.d
        return y

    def getUp(self):
        z = cos(self.time * self.om) * sin(self.latitude) * sin(self.psi)
        z += cos(self.latitude) * cos(self.psi) * cos(self.time * self.om) * cos(self.time * (self.Omega + self.om))
        z += cos(self.latitude) * sin(self.time * self.om) * sin(self.time * (self.Omega + self.om))
        z *= -self.d
        return z

    def getEast(self):
        return (-1.) * self.getWest()

    def getSouth(self):
        return (-1.)*self.getNorth()

    def getDir(self):
        w = array([self.getEast(), self.getNorth(), self.getUp()])  ## for x, y, z system
        w /= sqrt(dot(w,w))
        return w

