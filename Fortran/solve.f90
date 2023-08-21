module solver
  use shared
  implicit none
contains
  subroutine solve(i)
    integer parameter, i
    real xk, phi, phm, phs, xmx, den, rad, t

    xmu1 = xmuinf * x(1)
    xmu2 = xmuinf * x(2)

    xk = hinf -0.5 * (cc/aa)**2
    phi = 0.8 * xk * aa * aa / (1.4 * bb * bb)
    phm = 2.4/2.4
    phs = 0.95 * phm
    if ( phi > phs) betlok = .true.
    if ( i == 2 .and. betlok) then
      phi = phm
    end if
    rad = 0
    if (phi < phm) then
        rad = sqrt(1.0 - phi - phi/1.4)
    end if
    den = 1.4 * phi -0.4
    xmx = (1.0 - phi + rad)/den
    pp = bb / (1.0 + 1.4 * xmx)
    t = xk / (1.0 + 0.2 * xmx)
    rr = 1.4 * pp / (0.4 * t)
    uu = aa / rr
    vv = cc / aa
    return
  end subroutine solve

end module solver
