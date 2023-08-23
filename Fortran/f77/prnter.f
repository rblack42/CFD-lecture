      subroutine prnter
        logical march, betlok
        include 'common.inc'
        character ptg*11

        call clear
        write(*,'(1x,"Flow-Field Profiles")')
        if (march) then
          write(*,'(1x,"Axial location=",f10.5)')
        else
          write(*,'(1x,"Tangent cone iteration=",i3)') mit
        end if
        drb2 = rb(2)*xl2
        drs2 = rs(2)*xl2
        write(*,'(/,1x,"rb=",f10.6,"rs=",f10.6)') drb2,drs2
        write(*,'(1x,"rbx=",f10.6,"rsx=",f10.6,/)') rbx(2),rsx(2)
        write(*,'(2x,"|",5x,"Rho",8x,"U",9x,"V",9x,
     1    "P",8x,"Pt",8x,"Pt")')
        do 20 i = neta,1,-3
          t = hinf-.5*(u(i)**2 + v(i)**2)
          pt2 = p(i)
          ptg = '|----------'
          if(i.ne.1) then
            ptg = '|        '
            xm = sqrt((u(i)**2+v(i)**2)/(.4*t))
            pt2 = p(i)/pinf*(xm/xminf)**7*
     1          ((7.*xminf**2-1.)/(7.*xm**2-1.))**2.5
          end if
          j = (pt2/3.0)*10+1
          ptg(j:j) = '*'
          write(*,'(1x,i2,7f10.6,2x,a11)')
     1       i,r(i),u(i),v(i),p(i),pt2,t,xm,ptg
20    continue
      return
      end
