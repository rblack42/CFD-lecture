      subroutine solve(i)
        logical march, betlok
        include "common.inc"
        xk = hinf-.5*(cc/aa)**2
        print *,aa,bb,cc
        phi=.8*xk*aa*aa/(1.4*bb*bb)
        print *,"phi=",phi
        phm = 1.4/2.4
        phs = 0.95*phm
        if(phi.gt.phs) betlok=.true.
        if((i.eq.2).and. betlok) phi = phm
        rad=0.
        if(phi.le.phm) rad=sqrt(1.-phi-phi/1.4)
        den=1.4*phi-.4
        xmx = (1.-phi+rad)/den
        pp = bb/(1.+1.4*xmx)
        t = xk/(1.+.2*xmx)
        rr = 1.4*pp/(.4*t)
        uu = aa/rr
        vv = cc/aa
        return
      end       
