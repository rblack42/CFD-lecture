       program rrbaxi
       logical march,convrg,defdat,betlok
       character flag
       include "common.inc"

C      set logical flags
       march = .false.
       convrg = .false.
       write(*, '(1x,"rrbaxi v1.0")')
      
       tref = 1464.7157
       xmuref = 7.65034e-7
       reref = 2179168.0

       xminf = 5.95
       thetas = 22.0
       x0 = 5.0
       dxi = 0.0004
       xmuinf = 0.00002
       beta = -20.0
       neta = 31
       nitmax = 750
       nplot = 2
       dplot = 0.1
       xplot = 0.1

       hinf = (1.+2./(.4*xminf**2))/2.
       pinf = 1./(1.4*xminf**2)
       an = neta-1
       nem1 = neta-1
       deta = 1./an
       pi = acos(-1.)
       drcon = pi/180.
       xl1 = 22.5
       xl2 = xl1+27.5
       xh = 4.25
       rn = xh/2.+xl1*xl1/(2*xh)
       thetab = asin((xl1-x0)/rn)
       thetas = thetas*drcon
       rb0 = xh-rn+sqrt(rn*rn-(xl1-x0)**2)
       dx0 = rb0/tan(thetab)-x0
       x0 = x0+dx0
       xl1 = xl1+dx0
       xl2 = xl2+dx0
c      set initial conditions
       et=0.
       do 50 i=1,neta
          eta(i) = et
          r(i) = 1.
          u(i) = 1.
          v(i) = 0.
          p(i) = pinf
          et = et + deta
50     continue
       u(1) = 0.
       v(1) = 0.

       xmu1 = 0.0
       xmu2 = 0.0

       mit = 0
       call body
       call prnter
100    continue
       delm = 0.
       call body
       call precor
       mit = mit + 1
       print *,'mit=', mit
       if (march) then
         if (x(2).gt.xplot) then
           call prnter
           xplot = xplot + dplot
         end if
       else
         if ((mit/nplot*nplot).eq.mit) call prnter
         if (delm .le. 0.00001) then
           convrg = .true.
           print *,'converged at iteration = ',mit
         else if (mit .eq. mitmax) then
           convrg = .true.
           print *,'Run stopped at nitmax = ',nitmax
         end if
         if (convrg) then
           write(*,'(1x, "Release for marching (y/n)")')
           read(*,'(1a1)') flag
           march = ((flag .eq. 'y') .or. (flag .eq. 'Y'))
           if (.not. march) go to 300
           print *,'marching...'
           call prnter
           xplot = xplot + dplot
         end if
       end if
       if (x(2) .lt. 1.) go to 100
300    continue
       call prnter
       stop
       end
