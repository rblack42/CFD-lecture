#--------------------------------------------------------------------
# File:     AXIsolver.py
#
# Author:   Roie R. Black
# Date:     Dec 9, 2003
#--------------------------------------------------------------------

# Axisymmetric Navier Stokes Solver
# Python version - 20 November, 2003
#   (original program created in 1975 at USAF ARL Laboratories)

import math
import time

from Body import Body, OgiveCylinder
from OuterBoundary import OuterBoundary, OuterCone

class AXIsolver:
    '''Axisymettric Parabolized Navier Stokes Solver'''

    def __init__(self,values):
        '''Initialize solver with input values'''
        self.values = values
        self.fout = open("solution.dat",'w')
        self.initSolver()
        

    def initSolver(self):
        '''Initialize flow field data'''

        # booleans to control solver
        self.march   = False
        self.convrg  = False
        self.delm    = 0
        self.mit     = 0
        self.betloc  = False
        self.doprint = True

        # create empty lists for the variables
        self.eta = []
        self.rho = []
        self.u   = []
        self.v   = []
        self.p   = []

        # Useful math constants
        pi  = math.acos(-1.0)
        drcon   = pi/180.0
        gamma = 1.4

        # Free Stream conditions (provided from pgm start)
        self.xminf   = self.values['minf']        # Mach number
        self.tref    = self.values['tref']        # Free stream temperature
        self.reref   = self.values['reref']       # Reference Reynolds number
        self.xmuref  = self.values['muref']       # Free stream viscosity
        self.xmuinf  = self.values['muinf']       # nondimensional viscosity (?)

        # Computational adjustment factor
        self.beta    = -20.0

        # computed free stream conditions
        self.hinf    = (1.0+2.0/((gamma - 1)*self.xminf**2))/2.0
        self.pinf    = 1.0/(gamma*self.xminf**2)

        # Outer Boundary definition
        self.thetas  = self.values['thetas']
        self.thetas  = self.thetas* drcon

        # body definition
        self.x0  = 5.0
        self.xl1 = 22.5
        self.xl2 = self.xl1 + 27.5
        self.xh  = 4.25
        self.rn  = self.xh/2.0+self.xl1*self.xl1/(2.0*self.xh)
        self.thetab  = math.asin((self.xl1-self.x0)/self.rn)
        self.rb0 = self.xh - self.rn + math.sqrt(self.rn**2-(self.xl1-self.x0)**2)
        self.dx0 = self.rb0/math.tan(self.thetab) - self.x0

        self.x0  = self.x0 + self.dx0
        self.xl1 = self.xl1 + self.dx0
        self.xl2 = self.xl2 + self.dx0
        
        # computational grid definitions
        self.dxi    = self.values['dxi']
        self.neta   = self.values['neta']
        self.nitmax = self.values['nitmax']

        # output controls
        self.nplot  = self.values['nplot']
        self.dplot  = self.values['dplot']
        self.xplot  = 0.1

        # transformed axial step size
        self.deta   = 1.0/float(self.neta-1)

        et  = -self.deta
        self.f1 = []
        self.f2 = []
        for i in range ( 0,self.neta+1 ):
            self.eta += [ et ]
            self.rho += [ 1.0 ]
            self.u   += [ 1.0 ]
            self.v   += [ 0.0 ]
            self.p   += [ self.pinf ]
            self.f1  += [0.0]
            self.f2  += [0.0]
            et  = et + self.deta
    
        # set no slip boundary condition
        self.u[1]    = 0.0
        self.v[1]    = 0.0
    
        # body and shock variables
        #   Since the original code used 1,2 for indices, define 3 values here
        self.rb  = [ 0.0, 0.0, 0.0, 0.0 ]
        self.rbx = [ 0.0, 0.0, 0.0, 0.0 ]
        self.rs  = [ 0.0, 0.0, 0.0, 0.0 ]
        self.rsx = [ 0.0, 0.0, 0.0, 0.0 ]
        self.x   = [ 0.0, 0.0, 0.0, 0.0 ]
    
        #self.xmu1    = 0.0
        #self.xmu2    = 0.0

        self.plotx1 = self.dplot
        self.plotx2 = self.dplot - self.dxi
       
        # output neta to animation file
        out = "neta = " + str(self.neta) + "\n"
        self.fout.write(out)

    def body(self):
        '''Fill in body and shock data for given X'''

        # update the x location
        if(self.march):
            # when marching, advance x by dxi
            self.x[1] = self.x[2]
            self.x[2] = self.x[1] + self.dxi
        else:
            # conical flow, reset x location to x0
            self.x[1] = self.x0 / self.xl2 - self.dxi
            self.x[2] = self.x[1] + self.dxi

        # we scale the viscosity along x    
        self.xmu1 = self.xmuinf * self.x[1]
        self.xmu2 = self.xmuinf * self.x[2]
        
        # if we are marching accelerate the marching step size
        if(self.march):
            self.dxi = 1.005 * self.dxi
            self.beta = self.beta/1.005
        # now get the body and shock data
        bl = self.mybody.bodylength
        self.rs[1] = self.shock.body.getRadius(self.x[1]*bl)/bl
        self.rs[2] = self.shock.body.getRadius(self.x[2]*bl)/bl
        self.rsx[1] = self.shock.body.getSlope(self.x[1]*bl)
        self.rsx[2] = self.shock.body.getSlope(self.x[2]*bl)
        
 
            
        self.rb[1] = self.mybody.body.getRadius(self.x[1]*bl)/bl
        self.rb[2] = self.mybody.body.getRadius(self.x[2]*bl)/bl
        self.rbx[1] = self.mybody.body.getSlope(self.x[1]*bl)
        self.rbx[2] = self.mybody.body.getSlope(self.x[2]*bl)
    #--------------------------------------------------------------------

    def printer(self,mit,delm):
        '''ancient ascii printer plotting scheme'''
        print("Flow Field Properties")
        if(self.march):
            print("Axial Location %10.5f" % self.x[2])
        else:
            print("Tangent Cone Iteration %3d (%10.5f)" % (mit, delm))
        print("  I      Rho         U          V          P          T          M        Pt")
        self.fout.write("Axial Location = %10.5f\n" % self.x[2])
        for i in range ( self.neta, 0, -1 ):
            t = self.hinf - 0.5*(self.u[i]**2 + self.v[i]**2)
            pt2 = self.p[i]
            ptg = "----------"
            xm = 0.0
            if(i != 1):
                ptg = "|          ";
                xm = math.sqrt((self.u[i]**2+self.v[i]**2)/(0.4*t))
                pt2 = self.p[i]/self.pinf*(xm/self.xminf)**7 \
                    *((7.0*self.xminf**2-1.0)/(7.0*xm**2-1.0))**2.5
            j = int(pt2/3.0 *10.0) +1
            ptg = ""
            for k in range (1,j+1):
                ptg += "*"
            line = " %2d %10.5f %10.5f %10.5f %10.5f %10.5f %10.5f %10.5f" % \
                (i,self.rho[i],self.u[i],self.v[i],self.p[i],t, xm, pt2)
            print(line)
            self.fout.write(line)
            self.fout.write('\n')
    # Derived solver ----------------------
    def dsolve(self,i,aa,bb,cc):
        '''Reduce Solution vector to primitive values'''
        gamma = 1.4
        xk = self.hinf - 0.5*(cc/aa)**2
        phi = 2*(gamma-1) * xk * aa * aa/(gamma * bb * bb)
        
        # this sets a max value for Phi, source unknown
        phm = gamma/(gamma+1)

        phs = 0.95 * phm
        if(phi > phs):
            self.betloc = True
        if((i == 2) and self.betloc):
            phi = phm

        # we restrict solutions to supersonic. As long as phi is less that phm
        #   we ignore the radical in calculating phi.
        rad = 0.0
        test = 1.0 - phi - phi/gamma
        if(phi < phm):
            rad = math.sqrt(1.0-phi-phi/gamma)
        den = gamma*phi - (gamma - 1)

        # calculate  M_x^2 
        xmx = (1.0 - phi + rad)/den

        # Set return variables
        self.pp = bb /(1.0 + gamma*xmx)
        self.tt = xk/(1.0 + 0.2*xmx)
        self.rr = 1.4*self.pp/((gamma - 1)*self.tt)
        self.uu = aa / self.rr
        self.vv = cc / aa
 
            
    #--------------------------------------------------------------------
    def solve(self,i,aa,bb,cc):
        '''Reduce Solution vector to primitive values'''
        gamma = 1.4
        xk = self.hinf - 0.5*(cc/aa)**2
        phi = 2*(gamma-1) * xk * aa * aa/(gamma * bb * bb)
        phm = gamma/(gamma+1)
        phs = 0.95 * phm
        if(phi > phs):
            self.betloc = True
        if((i == 2) and self.betloc):
            phi = phm

        # we restrict solutions to supersonic. As long as phi is less that phm
        #   we ignore the radical in calculating phi.
        rad = 0.0
        test = 1.0 - phi - phi/gamma
        if(phi < phm):
            rad = math.sqrt(1.0-phi-phi/gamma)
        den = gamma*phi - (gamma - 1)

        # calculate  M_x^2 
        xmx = (1.0 - phi + rad)/den

        # Set return variables
        self.pp = bb /(1.0 + gamma*xmx)
        self.tt = xk/(1.0 + 0.2*xmx)
        self.rr = 1.4*self.pp/((gamma - 1)*self.tt)
        self.uu = aa / self.rr
        self.vv = cc / aa
 
    #--------------------------------------------------------------------
    def precor(self):
        '''MacCormack's Predictor Corrector Solver'''

        # this code does the predictor-corrector sweep in one pass. 
        # The predictor results are stored in the working array. 
        # The corrector uses the working array values when available.

        # clear working array
        w = [ [ 0,0,0,0 ], [ 0,0,0,0 ], [ 0,0,0,0 ], [ 0,0,0,0 ], [0,0,0,0 ] ]

        gamma = 1.4
        # main predictor corrector sweep ========================================           
        for i in range (2,self.neta+1):

            # on last pass, copy new working values back into position
            if(i == self.neta):
                for j in range(1,5):
                    w[j][1] = w[j][2]
                    w[j][2] = w[j ][3]
                # set 
                w[1][3] = 1.0
                w[2][3] = 1.0
                w[3][3] = 0.0
                w[4][3] = self.pinf
            else:
                # Flowfield point - predictor ( 2 -> neta-1 )
                r1 = self.rb[1] + self.eta[i]*(self.rs[1]-self.rb[1])
                r1p = self.rb[1] +self.eta[i+1]*(self.rs[1]-self.rb[1])
                ep1 = self.rho[i]*self.u[i]*r1
                ep2 = ep1 * self.u[i]+self.p[i]*r1
                ep3 = ep1*self.v[i]
                etar = 1.0/(self.rs[1]-self.rb[1])
                if(i == 2):
                    etaxm=((self.eta[i]-1.0)*self.rbx[1] -
                            self.eta[i]*self.rsx[1])*etar
                    den1 = 1./self.deta
                    uetam = (self.u[i]-self.u[i-1])*den1
                    vetam = (self.v[i]-self.v[i-1])*den1
                    deldvm = etaxm*uetam+etar*vetam+self.v[i]/r1
                    txxm = 2.0*self.xmu1*etaxm*uetam - \
                        2.0/3.0*self.xmu1*self.beta*deldvm
                    sigxrm=self.xmu1*(etaxm*vetam+etar*uetam)
                    trrm = 2.0*self.xmu1*etar*vetam - \
                        2.0/3.0*self.xmu1*self.beta*deldvm
                    e1p = self.rho[i]*self.u[i]*r1
                    e2p = e1p*self.u[i]+self.p[i]*r1-txxm*r1
                    e3p = e1p*self.v[i]-sigxrm*r1
                    f1p = self.rho[i]*self.v[i]*r1
                    f2p = f1p*self.u[i]-sigxrm*r1
                    f3p = f1p*self.v[i]+self.p[i]*r1-trrm*r1
                if(i>2):
                    etaxm=etaxpp
                etaxp = ((self.eta[i+1]-1.0)*self.rbx[1] - \
                            self.eta[i+1]*self.rsx[1])*etar 
                etaxpp=etaxp
                uetap = (self.u[i+1]-self.u[i])*den1
                vetap = (self.v[i+1]-self.v[i])*den1
                if(i>2):
                    deldvm = dldvpp
                deldvp = etaxp*uetap+etar*vetap+self.v[i+1]*r1p
                dldvpp = deldvp
                txpp = 2.0*self.xmu1*etaxp*uetap - \
                    2.0/3.0*self.xmu1*self.beta*deldvp
                sigxrp=self.xmu1*(etaxp*vetap+etar*uetap)
                e1m = e1p
                e1p = self.rho[i+1]*self.u[i+1]*r1p
                e2m = e2p
                e2p = e1p*self.u[i+1]-txpp*r1p+self.p[i+1]*r1p
                e3m = e3p
                e3p=e1p*self.v[i+1]-sigxrp*r1p
                trrp = 2.0*self.xmu1*etar*vetap - \
                    2.0/3.0*self.xmu1*self.beta*deldvp
                f1m = f1p
                f1p = self.rho[i+1]*self.v[i+1]*r1p
                f2m = f2p
                f2p = f1p*self.u[i+1]-sigxrp*r1p
                f3m = f3p
                f3p = f1p*self.v[i+1]+self.p[i+1]*r1p-trrp*r1p
                sigpp = -self.p[i]+2.0*self.xmu1*self.v[i]/r1 \
                    -2.0/3.0*self.xmu1*self.beta*deldvm
                h3 = -sigpp
                h2 = 0.0
                h1 = 0.0
                ep1 = ep1 -self.dxi*etaxm*den1*(e1p-e1m) - \
                    self.dxi*etar*den1*(f1p-f1m)+self.dxi*h1
                ep2 = ep2 -self.dxi*etaxm*den1*(e2p-e2m) - \
                    self.dxi*etar*den1*(f2p-f2m)+self.dxi*h2
                ep3 = ep3 -self.dxi*etaxm*den1*(e3p-e3m) - \
                    self.dxi*etar*den1*(f3p-f3m)+self.dxi*h3
                r2 = self.rb[2]+self.eta[i]*(self.rs[2]-self.rb[2])
                aa = ep1/r2
                bb = ep2/r2
                cc = ep3/r2
                # solve for primative variables and store in work area
                self.solve(i,aa,bb,cc)

                # move data in working array back for corrector pass
                for j in range (1,5):
                    w[j][1] = w[j][2]
                    w[j][2] = w[j][3]

                # save current results in working array
                w[1][3] = self.rr
                w[2][3] = self.uu
                w[3][3] = self.vv
                w[4][3] = self.pp
            if(i != 2):
                # Corrector - lags one point
                r1 = self.rb[1] + self.eta[i-1]*(self.rs[1]-self.rb[1])
                xep1 = self.rho[i-1]*self.u[i-1]*r1
                xep2 = xep1 * self.u[i-1]+self.p[i-1]*r1
                xep3 = xep1*self.v[i-1]
                r2 = self.rb[2] + self.eta[i-1]*(self.rs[2]-self.rb[2])
                r2m = self.rb[2] + self.eta[i-2]*(self.rs[2]-self.rb[2])
                ep1 = w[1][2]*w[2][2]*r2
                ep2 = ep1*w[2][2]+w[4][2]*r2
                ep3 = ep1*w[3][2]
                etar = 1.0/(self.rs[2]-self.rb[2])
                if(i == 3):
                    etaxm=((self.eta[i-2]-1.0)*self.rbx[2]- \
                                self.eta[i-2]*self.rsx[2])*etar
                    uetam = (w[2][2]-w[2][1])*den1
                    vetam = (w[3][2]-w[3][1])*den1
                    deldvm = etaxm*uetam+etar*vetam+w[3][1]/r2m
                    txxm = 2.0*self.xmu1*etaxm*uetam- \
                        2.0/3.0*self.xmu1*self.beta*deldvm
                    sigxrm=self.xmu1*(etaxm*vetam+etar*uetam)
                    trrm = 2.0*self.xmu1*etar*vetam- \
                        2.0/3.0*self.xmu1*self.beta*deldvm
                    e1pc = w[1][1]*w[2][1]*r2m
                    e2pc = e1pc*w[2][1]-txxm*r2m + w[4][1]*r2m
                    e3pc = e1pc*w[3][1]-sigxrm*r2m
                    f1pc = w[1][1]*w[3][1]*r2m
                    f2pc = f1pc*w[2][1]-sigxrm*r2m
                    f3pc = f1pc*w[3][1]+w[4][1]*r2m-trrm*r2m

                etaxp = ((self.eta[i-1]-1.0)*self.rbx[2]- \
                            self.eta[i-1]*self.rsx[2])*etar 
                uetap = (w[2][3]-w[2][2])*den1
                vetap = (w[3][3]-w[3][2])*den1
                deldvp = etaxp*uetap+etar*vetap+w[3][2]*r2
                txxp = 2.0*self.xmu1*etaxp*uetap- \
                    2.0/3.0*self.xmu1*self.beta*deldvp
                sigxrp=self.xmu1*(etaxp*vetap+etar*uetap)
                e1mc = e1pc
                e1pc = w[1][2]*w[2][2]*r2
                e2mc = e2pc
                e2pc = e1pc*w[2][2]-txxp*r2+w[4][2]*r2
                e3mc = e3pc
                e3pc=e1pc*w[3][2]-sigxrp*r2
                trrp = 2.0*self.xmu1*etar*vetap- \
                    2.0/3.0*self.xmu1*self.beta*deldvp
                f1mc = f1pc
                f1pc = w[1][2]*w[3][2]*r2
                f2mc = f2pc
                f2pc = f1pc*w[2][2]-sigxrp*r2
                f3mc = f3pc
                f3pc = f1pc*w[3][2]+w[4][2]*r2-trrp*r2
                sigpp = -w[4][2]+2.0*self.xmu1*w[3][2]/r2- \
                    2.0/3.0*self.xmu1*self.beta*deldvp
                
                h3 = -sigpp
                h2 = 0.0
                h1 = 0.0
                ep1 = 0.5*(ep1 + xep1-self.dxi*etaxp*den1*(e1pc-e1mc) \
                    -self.dxi*etar*den1*(f1pc-f1mc)+self.dxi*h1)
                    
                ep2 = 0.5*(ep2 + xep2-self.dxi*etaxp*den1*(e2pc-e2mc) \
                    -self.dxi*etar*den1*(f2pc-f2mc)+self.dxi*h2)

                ep3 = 0.5*(ep3 + xep3-self.dxi*etaxp*den1*(e3pc-e3mc) \
                    -self.dxi*etar*den1*(f3pc-f3mc)+self.dxi*h3)
                aa = ep1/r2
                bb = ep2/r2
                cc = ep3/r2
                self.solve(i-1,aa,bb,cc)
                self.rho[i-1]   = self.rr
                self.u[i-1]     = self.uu
                self.v[i-1]     = self.vv

                # convergence depends on the max change in pressure
                psav            = self.p[i-1]   # save last value
                self.p[i-1]     = self.pp
                delp            = self.pp - psav  # calculate difference
                if(delp > self.delm):
                    self.delm   = delp             # update max this pass
            else:
                # we are at the lower boundary
                w[4][2] = w[4][3]
                w[2][2] = 0.0
                w[3][2] = 0.0
                w[1][2] = gamma*w[4][2]/((gamma - 1)*self.hinf)
        
        # Body conditions
        self.p[1] = self.p[2]
        self.rho[1] = gamma*self.p[1]/((gamma - 1)*self.hinf)
        
    #--------------------------------------------------------------------

    def runSolver(self):
        # Main computational loop
        mit = 0

        xstep = 0
        self.body()
        if self.doprint > 0:
            self.printer(mit,self.delm)
        convrg = False
        tic = time.perf_counter()
        while convrg == False:
            self.delm = 0.0
            self.body()
            self.precor()
            mit = mit + 1
            if(self.march):
                xstep = xstep + 1

                # see if we reached he end of the body
                if(self.x[2] > 1.0 - self.dxi):
                        convrg = True
                        print("Solution ending at x = %10.6f" % self.x[2])
                        print("Axial steps: %d\n" % xstep)
                        toc = time.perf_counter()
                        print(f"  Total time: {toc - tic:0.4f} seconds")
                # otherwise generate plot at xplot stations
                elif(self.x[2] > self.xplot):
                    if self.doprint > 0:
                        self.printer(mit,self.delm)

                    # set for next plot station
                    self.xplot = self.xplot+self.dplot
                    
            else:
                # see if we have reached nplot iterations
                if((mit/self.nplot*self.nplot) == mit):
                    if self.doprint >0:
                        self.printer(mit,self.delm)

                # check conical flow convergence
                if(self.delm <= 0.0001):
                    print("Conical solution converged on iteration %4d" % mit)
                    self.march = True
                else:
                    if(mit >= self.nitmax):
                        convrg = True
                        print("Run stopped (nitmax = %4d)" % self.nitmax)
        self.fout.close()

#================================================================================
if __name__ == '__main__':

    # test case initial data
    v = {}
    v['minf']   = 5.95          # Axial Mach Number
    v['tref']   = 1464.7157     # Reference static temperature
    v['reref']  = 2179168.0     # Ref Reynolds Number
    v['muref']  = 7.65034e-7    # Reference Viscosity
    v['muinf']  = 0.00002       
    v['thetas'] = 22.0          # Outer boundary angle
    v['dxi']    = 0.0004        # initial axial step size
    v['neta']   = 31            # number or radial points
    v['nitmax'] = 750           # max conical iterations
    v['nplot']  = 25            # steps per axial data output
    v['dplot']  = 0.05          

    # create a solver object
    solver          = AXIsolver(v)

    # define the body and outer boundary
    solver.mybody   = OgiveCylinder()
    solver.shock    = OuterCone(v['thetas'],solver.mybody.bodylength)

    # run the solver and display on console
    solver.runSolver()
                        
