       subroutine body
         logical march, betlok
         include 'common.inc'
       if (march) then
         x(1) = x(2)
         x(2) = x(1) + dxi
       else
         x(1) = x0/xl2-dxi
         x(2) = x(1) + dxi
       end if
       xmu1 = xmuinf*x(1)
       xmu2 = xmuinf*x(2)
       rsx(1) = tan(thetas)
       rsx(2) = rsx(1)
       rs(1) = x(1)*rsx(1)
       rs(2) = x(2)*rsx(2)
       do 200 i=1,2
        if(x(i).le.(x0/xl2)) then
         rbx(i) = tan(thetab)
         rb(i) = x(i)*rbx(i)
       else if (x(i).le.(xl1/xl2)) then
         rb0 = x0*tan(thetab)
         xf1 = xh-rb0
         bb = 4.*xf1-3.*(xl1-x0)*tan(thetab)
         aa = xf1-bb-(xl1-x0)*tan(thetab)
         cc = 0.
         dd = (xl1-x0)*tan(thetab)
         ee = 0.
         xb = (x(i)*xl2-x0)/(xl1-x0)
         rb(i) = rb0 + xb*(xb*(xb*(xb*aa +bb) + cc) + dd) + ee
         rbx(i) = 4.*aa*xb**3/(xl1-x0) +
     1      3.*bb*xb**2/(xl1-x0)+dd/(xl1-x0)
         rb(i) = rb(i)/xl2
       else
         rb(i) = xh/xl2
         rbx(i) = 0.
       end if
200    continue
       if (march) then
         dxi = 1.005 * dxi
         beta = beta/1.005
       end if
       print *,'rb = ', rb(1), ' rs = ', rs(1)
       return
       end
