module maccormack
  use shared
  use solver
  implicit none

contains

    subroutine precor()
      real, dimension(4,4) :: w
      real, dimension(51) :: exp1

      real :: deldvm, deldvp, delp, den1,dldvpp
      real :: e1m,e1mc,e1p,e1pc,e2m,e2mc,e2p,e2pc,e3m,e3mc,e3p,e3pc
      real :: ep1,ep2,ep3, etar,etaxm,etaxp,etaxpp
      real :: f1m,f1mc,f1p,f1pc,f2m,f2mc,f2p,f2pc,f3m,f3mc,f3p,f3pc
      real :: h1,h2,h3,psav,r1,r1p,r2,r2m
      real :: sigpp, sigxrm, sigxrp
      real :: trrm,trrp,txxm,txxp, txpp
      real :: uetam,uetap, vetam,vetap,xep1,xep2,xep3
      integer i,j

      ! initialize w
      do i=1,4
        do j = 1,4
          w(i,j) = 0.0 1=rho, 2=u, 3=v, 4=p
        end do
      end do
 
      ! main predictor corrector sweep            
      do i=2,neta
        ! last pass, update work array with free stream data
        if(i == neta) then
          do j = 1,4
              w(j,1) = w(j,2)
              w(j,2) = w(j,3)
          end do
          w(1,3) = 1.0
          w(2,3) = 1.0
          w(3,3) = 0.0
          w(4,3) = pinf
        else

          ! Flowfield point - predictor ( 2 - neta-1 )
          r1 = rb(1) + eta(i)*(rs(1)-rb(1))
          r1p = rb(1) + eta(i+1)*(rs(1)-rb(1))
          ep1 = rho(i)*u(i)*r1
          ep2 = ep1 * u(i)+p(i)*r1
          ep3 = ep1*v(i)
          etar = 1.0/(rs(1)-rb(1))
          if(i == 2) then
            etaxm=((eta(i)-1.0)*rbx(1) - &
                eta(i)*rsx(1))*etar
            den1 = 1./deta
            uetam = (u(i)-u(i-1))*den1
            vetam = (v(i)-v(i-1))*den1
            deldvm = etaxm*uetam+etar*vetam+v(i)/r1
            txxm = 2.0*xmu1*etaxm*uetam - &
                2.0/3.0*xmu1*beta*deldvm
            sigxrm=xmu1*(etaxm*vetam+etar*uetam)
            trrm = 2.0*xmu1*etar*vetam - &
                2.0/3.0*xmu1*beta*deldvm
            e1p = rho(i)*u(i)*r1
            e2p = e1p*u(i)+p(i)*r1-txxm*r1
            e3p = e1p*v(i)-sigxrm*r1
            f1p = rho(i)*v(i)*r1
            f2p = f1p*u(i)-sigxrm*r1
            f3p = f1p*v(i)+p(i)*r1-trrm*r1
          end if
          if(i>2) then
            etaxm=etaxpp
          end if
          etaxp = ((eta(i+1)-1.0)*rbx(1) - &
              eta(i+1)*rsx(1))*etar 
          etaxpp=etaxp
          uetap = (u(i+1)-u(i))*den1
          vetap = (v(i+1)-v(i))*den1
          if(i>2) then
            deldvm = dldvpp
          end if
          deldvp = etaxp*uetap+etar*vetap+v(i+1)*r1p
          dldvpp = deldvp
          txpp = 2.0*xmu1*etaxp*uetap - &
              2.0/3.0*xmu1*beta*deldvp
          sigxrp=xmu1*(etaxp*vetap+etar*uetap)
          e1m = e1p
          e1p = rho(i+1)*u(i+1)*r1p
          e2m = e2p
          e2p = e1p*u(i+1)-txpp*r1p+p(i+1)*r1p
          e3m = e3p
          e3p=e1p*v(i+1)-sigxrp*r1p
          trrp = 2.0*xmu1*etar*vetap - &
              2.0/3.0*xmu1*beta*deldvp
          f1m = f1p
          f1p = rho(i+1)*v(i+1)*r1p
          f2m = f2p
          f2p = f1p*u(i+1)-sigxrp*r1p
          f3m = f3p
          f3p = f1p*v(i+1)+p(i+1)*r1p-trrp*r1p
          sigpp = -p(i)+2.0*xmu1*v(i)/r1 &
              -2.0/3.0*xmu1*beta*deldvm
          h3 = -sigpp
          h2 = 0.0
          h1 = 0.0
          ep1 = ep1 -dxi*etaxm*den1*(e1p-e1m) - &
              dxi*etar*den1*(f1p-f1m)+dxi*h1
          ep2 = ep2 -dxi*etaxm*den1*(e2p-e2m) - &
              dxi*etar*den1*(f2p-f2m)+dxi*h2
          ep3 = ep3 -dxi*etaxm*den1*(e3p-e3m) - &
              dxi*etar*den1*(f3p-f3m)+dxi*h3
          r2 = rb(2)+eta(i)*(rs(2)-rb(2))
          aa = ep1/r2
          bb = ep2/r2
          cc = ep3/r2
              
          ! solve for primative variables and store in work area
          call solve(i)
          do j = 1,4
            w(j,1) = w(j,2)
            w(j,2) = w(j,3)
          end do
          w(1,3) = rr
          w(2,3) = uu
          w(3,3) = vv
          w(4,3) = pp
        end if

        if(i /= 2) then
              
          ! Corrector - lags one point
          r1 = rb(1) + eta(i-1)*(rs(1)-rb(1))
          xep1 = rho(i-1)*u(i-1)*r1
          xep2 = xep1 * u(i-1)+p(i-1)*r1
          xep3 = xep1*v(i-1)
          r2 = rb(2) + eta(i-1)*(rs(2)-rb(2))
          r2m = rb(2) + eta(i-2)*(rs(2)-rb(2))
          ep1 = w(1,2)*w(2,2)*r2
          ep2 = ep1*w(2,2)+w(4,2)*r2
          ep3 = ep1*w(3,2)
          etar = 1.0/(rs(2)-rb(2))
          if(i == 3) then
            etaxm=((eta(i-2)-1.0)*rbx(2)- &
                eta(i-2)*rsx(2))*etar
            uetam = (w(2,2)-w(2,1))*den1
            vetam = (w(3,2)-w(3,1))*den1
            deldvm = etaxm*uetam+etar*vetam+w(3,1)/r2m
            txxm = 2.0*xmu1*etaxm*uetam- &
                2.0/3.0*xmu1*beta*deldvm
            sigxrm=xmu1*(etaxm*vetam+etar*uetam)
            trrm = 2.0*xmu1*etar*vetam- &
                2.0/3.0*xmu1*beta*deldvm
            e1pc = w(1,1)*w(2,1)*r2m
            e2pc = e1pc*w(2,1)-txxm*r2m + w(4,1)*r2m
            e3pc = e1pc*w(3,1)-sigxrm*r2m
            f1pc = w(1,1)*w(3,1)*r2m
            f2pc = f1pc*w(2,1)-sigxrm*r2m
            f3pc = f1pc*w(3,1)+w(4,1)*r2m-trrm*r2m
            etaxp = ((eta(i-1)-1.0)*rbx(2)- &
                eta(i-1)*rsx(2))*etar 
            uetap = (w(2,3)-w(2,2))*den1
            vetap = (w(3,3)-w(3,2))*den1
            deldvp = etaxp*uetap+etar*vetap+w(3,2)*r2
            txxp = 2.0*xmu1*etaxp*uetap- &
                2.0/3.0*xmu1*beta*deldvp
            sigxrp=xmu1*(etaxp*vetap+etar*uetap)
            e1mc = e1pc
            e1pc = w(1,2)*w(2,2)*r2
            e2mc = e2pc
            e2pc = e1pc*w(2,2)-txxp*r2+w(4,2)*r2
            e3mc = e3pc
            e3pc=e1pc*w(3,2)-sigxrp*r2
            trrp = 2.0*xmu1*etar*vetap- &
                2.0/3.0*xmu1*beta*deldvp
            f1mc = f1pc
            f1pc = w(1,2)*w(3,2)*r2
            f2mc = f2pc
            f2pc = f1pc*w(2,2)-sigxrp*r2
            f3mc = f3pc
            f3pc = f1pc*w(3,2)+w(4,2)*r2-trrp*r2
            sigpp = -w(4,2)+2.0*xmu1*w(3,2)/r2- &
                2.0/3.0*xmu1*beta*deldvp
                
            h3 = -sigpp
            h2 = 0.0
            h1 = 0.0
            ep1 = 0.5*(ep1 + xep1-dxi*etaxp*den1*(e1pc-e1mc) &
                -dxi*etar*den1*(f1pc-f1mc)+dxi*h1)                    
            ep2 = 0.5*(ep2 + xep2-dxi*etaxp*den1*(e2pc-e2mc) &
                -dxi*etar*den1*(f2pc-f2mc)+dxi*h2)
            ep3 = 0.5*(ep3 + xep3-dxi*etaxp*den1*(e3pc-e3mc) &
                -dxi*etar*den1*(f3pc-f3mc)+dxi*h3)
                
            aa = ep1/r2
            bb = ep2/r2
            cc = ep3/r2
            call solve(i-1)
            rho(i-1)  = rr
            u(i-1)    = uu
            v(i-1)    = vv
            psav      = p(i-1)
            p(i-1)    = pp
            delp      = pp - psav
            if(delp > delm) then
                delm   = delp
            end if
          else
            ! we are at the lower boundary
            w(4,2) = w(4,3)
            w(2,2) = 0.0
            w(3,2) = 0.0
            w(1,2) = 1.4*w(4,2)/(0.4*hinf)
          end if
        end if
      end do  
    end subroutine precor
end module maccormack
