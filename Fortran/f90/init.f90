module init
  use shared
  implicit none

contains
  
  subroutine reset()
    real tref, xmuref, reref
    real an, drcon, pi, rm, xplot, et
    real dx0
    integer i

    pi = acos(-1.0)
    drcon = pi / 180.0

    ! initialize free stream properties
    xminf = 5.95
    xmuinf = 0.00002
    tref = 1464.7157
    xmuref = 7.65034e-7
    reref = 2179168

    beta = -20.0

    ! calculated free stream properties
    hinf = (1.0 + 2.0 / (0.4 * xminf**2))/2.0
    pinf = 1.0 / (1.4 * xminf**2)
    
    ! body definition
    x0 = 0.5
    xl1 = 22.5
    xl2 = xl1 + 27.5
    xh = 4.25
    rn = xh/2.0 + xl1*xl1/(2.0 * xh)
    thetab = asin((xl1 - x0)/rn)
    rb0 = xh -  rm + sqrt(rn * rn -(xl1-x0)**2)
    dx0 = rb0 / tan(thetab) - x0
    x0 = x0 + dx0
    xl1 = xl1 + dx0
    xl2 = xl2 + dx0

    ! computational grid definition
    dxi = 0.0004
    neta = 31
    nitmax = 750
    thetas = 22 * drcon

    ! output control
    nplot = 25
    dplot = 0.1
    xplot = 0.1

    ! transformed axial step size
    an = neta - 1
    nem1 = neta - 1
    deta = 1.0 / an

    ! initial conditions - freestream
    et = 0.0
    do i = 1,neta
      eta(i) = et
      rho(i) = 1.0
      u(i) = 1.0
      v(i) = 0.0
      p(i) = pinf
      et = et + deta

      f1(i) = 0.0
      f2(i) = 0.0
      data1(i) = 0.0
      data2(i) = 0.0
    end do

    do i = 1,2
      rb(i) = 0.0
      rbx(i) = 0.0
      rs(i) = 0.0
      rsx(i) = 0.0
    end do

    xmu1 = 0.0
    xmu2 = 0.0

    ! boundary condition on surface
    u(1) = 0.0
    v(1) = 0.0

    ! output control variables
    plotx1 = dplot
    plotx2 = dplot - dxi

    mit = 0
    nplot = 25
    dplot = 0.05

  end subroutine reset

end module init

