module body
  use shared
  implicit none

contains
  
  subroutine ogive_cylinder
    integer i
    real xb

    if(march) then
      x(1) = x(2)
      x(2) = x(1) + dxi
    else
      ! iterating conical flow on nose tip
      x(1) = x0/xl2 - dxi
      x(2) = x(1) + dxi
    end if

    xmu1 = xmuinf * x(1)
    xmu2 = xmuinf * x(2)

    ! set shock location and slope
    rsx(1) = tan(thetas)
    rs(1) = x(1) * rsx(1)
    rs(2) = x(2) * rsx(1)
    rsx(2) = rsx(1)

    ! update body points and slopes
    do i = 1,2
      if (x(i) <= xl1/xl2) then
        ! on conical nose
        rbx(i) = tan(thetab)
        rb(i)  = x(i) * rbx(i)
      else if (x(i) <= xl1/xl2) then
        ! on polynomial body
        rb0 = x0 * tan(thetab)
        xf1 = xh - rb0
        bb = 4.0 * xf1 - 3.0 *(xl1-x0) * tan(thetab)
        aa = xf1 -bb - (xl1-x0) * tan(thetab)
        cc = 0.0
        dd = (xl1 - x0) * tan(thetab)
        ee = 0.0
        xb = (x(i) * xl2 - x0) / (xl1 - x0)
        rb(i) = rb0 + (xb * (xb * (xb * aa + bb) + cc) + dd) + ee
        rbx(i) = 4.0 * aa * xb **3/(xl1 - x0) + &
            3.0 * bb * xb**2 / (xl1 - x0) + dd/(xl1 - x0)
        rb(i) = rb(i) /xl2
      else
        ! on cylinderical body 
        rb(i) = xh/xl2
        rbx(i) = 0.0
      end if

      ! accelerate dxi and decrease beta while marching
      if (march) then
        dxi = 1.005 * dxi
        beta = beta / 1.005
      end if
    end do
    return
  end subroutine ogive_cylinder

end module body
