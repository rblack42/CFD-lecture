module prtplot
  use shared
  implicit none

contains

    subroutine plot()
      character ptg*11
      real drb2, drs2
      real pt2, xm, t
      integer i,j

      write(*,'(1x,"Flow Field Profiles")')
      if (march) then
        write(*,'(1x, "Axial location =",f10.5)') x(2)
      else
        write(*,'(1x,"Tangent cone iteration = ",i3)') mit
      end if
      drb2 = rb(2) * xl2
      drs2 = rs(2) * xl2
      write(*,'(/,1x,"rb = ",f10.6," rs = ",f10.6)') drb2, drs2
      write(*,'(1x,"rbx=",f10.6," rsx=",f10.6/)') rbx(2), rsx(2)
      write(*,'(1x, 4f12.6)') xminf, hinf, pinf, xmuinf
      write(*,'(2x,"I", 5x, "Rho",8x,"U",9x,"V", 9x,"P", 18x, "Pt", 8x, "Pt2")')
      do i = neta,1,-3
        t =  hinf - 0.5 * (u(i)**2 + v(i)**2)
        pt2 = p(i)
        ptg = '|----------'
        xm = 0.0
        if (i /= 1) then
          xm = sqrt((u(i)**2 + v(i)**2)/(0.4*t))
          pt2 = p(i) / pinf * (xm/xminf)**7 * &
              ((7.0*xminf**2-1.0)/(7.0*xm**2 - 1.0))**2.5
        end if
        j = (pt2/3.0)*10+1 
        ptg(j:j) = '*'
        write(*,'(1x,i2,6f12.6,2x,a11)') i,rho(i),u(i),v(i),p(i),t,xm, ptg
      end do
    end subroutine plot
end module prtplot
