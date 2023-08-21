module shared
  implicit none

  logical :: march, convrg, defdat, betlok
  character :: flag

  ! flow field variables
  real, dimension(51) ::  rho, u, v, p, eta
  real, dimension(51) :: f1, f2, data1, data2
  ! free stream conditions set for test run
  real :: xminf, tref, reref, xmuinf, xmuref
  
  real :: beta ! computation adjustment factor
 
  ! Calculated free stream properties
  real :: hinf, pinf

  ! Body geometry data
  real :: xl1, xl2, xh, rn, x0, thetab 
  
  ! Outer boundary of computational field
  real :: thetas

  real, dimension(2) :: rb, rbx, rs, rsx, x
  real :: rb0, xf1

  ! Flow field computation variables
  real :: aa, bb, cc, dd, ee, rr, uu, vv, pp

  ! Iteration control variables
  integer :: mit, nplot, nitmax, neta, nem1
  real :: deta, xmu1, xmu2, dxi, delm

  ! Graphics/print controls
  real :: dplot, xplot
  real :: plotx1, plotx2
end module shared
