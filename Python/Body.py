#--------------------------------------------------------------------
# File:     Body.py
#
# Author:   Roie R. Black
# Date:     Dec 9, 2003
# Course:   CS 5335
#--------------------------------------------------------------------

import math

class PolyBody:
    '''Class to manage polynomial body segments'''

    def __init__(self,x0,x1,poly):
        '''CONSTRUCTOR - create polynomial for body segment'''
        self.x0 = x0
        self.x1 = x1
        self.coef = []
        self.degree = len(poly)
        for c in poly:
            self.coef.append(c)
       
    def getSegRadius(self,x):
        '''Return the radius for a given x'''
        xbar = (x-self.x0)/(self.x1-self.x0)
        if (xbar < 0)or(xbar>1.0):
            rad = -1.0
        else:
            # figure the polynomial
            rad = self.coef[0]
            for i in range(0,self.degree-1):
                rad = rad*xbar+self.coef[i+1]
        return rad

    def getSegSlope(self,x):
        '''Return the slope for a given x'''
        xbar = (x - self.x0)/(self.x1 - self.x0)
        if(xbar <0)or(xbar>1.0):
            slope = 1.0
            return slope
        else:
            factor = float(self.degree -1)
            slope = factor*self.coef[0]
            for i in range(0,self.degree-2):
                 factor = factor-1.0
                 slope = slope*xbar+factor*self.coef[i+1]
        slope = slope / (self.x1-self.x0)
        return slope
    
    def getSegCurvature(self,x):
        '''Return the curvature for a given x'''
        xbar = (x - self.x0)/(self.x1 - self.x0)
        if(xbar <0)or(xbar>1.0):
            curve = 1.5
            return curve
        else:
            d1 = self.degree-2
            d2 = self.degree-1
            factor = float(d1*d2)
            curve = factor*(self.coef[0])
            for i in range(0,self.degree-3):
                d1 = d1-1
                d2 = d2-1
                factor = float(d1*d2)
                curve = curve*xbar+factor*self.coef[i+1]
            curve = curve / (self.x1 - self.x0)**2
        return curve
    
class Body:
    '''Class to manage body definition'''
    def __init__(self,segments):
        '''CONSTRUCTOR - initialize segment array for this body'''
        self.segments = segments

    def getRadius(self,x):
        '''Return radius for any given x on a segmented body'''
        nseg = len(self.segments)
        for seg in range (0,nseg):
            rad= self.segments[seg].getSegRadius(x)
            if rad > 0.0:
                break
        return rad

    def getSlope(self,x):
        '''Return slope for any given x on a segmented body'''
        nseg = len(self.segments)
        for seg in range (0,nseg):
            slope= self.segments[seg].getSegSlope(x)
            if slope < 1.0:
                break
        return slope
    
    def getCurvature(self,x):
        '''Return curvature for any given x on a segmented body'''
        nseg=len(self.segments)
        for seg in range(0,nseg):
            curve = self.segments[seg].getSegCurvature(x)
            if (curve < 1.0):
                break
        return curve
        
class OgiveCylinder:
    '''Test Body for CFDexplorer'''

    def __init__(self):
        '''Initialize polynomial coefficients for ogive cylinder test body'''
        pi  = math.acos(-1.0)
        drcon   = pi/180.0
        thetas = 22.0 * drcon

        # figure the body geometry

        x0  = 5.0       # first computational point
        x1  = 22.5      # length of ogive
        x2  = 50.0      # length of cylinder part
        xh  = 4.25      # cylinder body radius

        rn  = (x1*x1 + xh*xh)/(2.0*xh)
        thetab  = math.asin((x1-x0)/rn)
      
        rb0 = xh - rn + math.sqrt(rn**2 -(x1-x0)**2)
        dx0 = rb0/math.tan(thetab) - x0

        # adjust the body positions for the new shape
        x0  = x0 + dx0
        x1  = x1 + dx0
        x2  = x2 + dx0

        # nondimensionalize the body dimension data using x2

        # calculate the polynomial coefficients
        tanthetab = math.tan(thetab)
        L = x1 - x0
        M = xh - rb0
        bb = 4.0 * M - 3.0 * L * tanthetab
        aa = M - bb - L * tanthetab
        cc = 0.0
        dd = L * tanthetab
        ee = rb0
        poly = [aa,bb,cc,dd,ee]
            
        # create the array of body objects
        segments = []
        segments.append(PolyBody(0.0,x0,[x0*math.tan(thetab),0.0]))
        segments.append(PolyBody(x0,x1,poly))
        segments.append(PolyBody(x1,x2,[xh]))
        self.body = Body(segments)
        self.bodylength = x2
        self.name = 'Ogive-Cylinder'
        
    def getBodyPoints(self,num,dx,scale):
        points = [];
        x = 0
        for i in range(num):
           y = self.body.getRadius(x)*scale
           x = x + dx
           points.append([x/dx,y/dx])
        return points

    def getBodySlopes(self,num,dx,scale):
        slopes=[]
        x = 0
        for i in range(num):
           y = self.body.getSlope(x)*scale
           x = x + dx
           slopes.append([x/dx,y/dx])

        return slopes

    def getBodyCurvatures(self,num,dx,scale):
        curves = []
        x = 0
        for i in range(num):
           y = self.body.getCurvature(x)*scale
           x = x + dx
           curves.append([x/dx,y/dx])
        return curves
    
if __name__ == "__main__":
    
    mybody = OgiveCylinder()
    length = mybody.bodylength

    print("Body %s length = %10.6f\n" % (mybody.name,mybody.bodylength))
    
    nsteps = 300
    dxi = (mybody.bodylength/float(nsteps))
    xi = 0.0
    print("dxi=%10.6f nsteps=%d\n" % (dxi,nsteps))
    for i in range (0,nsteps):
        xi = xi + dxi
        rad = mybody.body.getRadius(xi)
        slope = mybody.body.getSlope(xi)
        curve = mybody.body.getCurvature(xi)
        print("X=%10.6f R=%10.6f dR/dx=%10.6f d2r/dx2=%10.6f\n" % (xi,rad,slope,curve))
