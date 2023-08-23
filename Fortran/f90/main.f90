program hello
  use shared
  use init
  use body
  use solver
  use maccormack
  use prtplot
  implicit none

  print *, 'Parabolized Navier Stokes Example'

  ! Initialize shared data
  call reset
  ! Main loop starts here
  call ogive_cylinder()
  call plot()
  do while (mit < 10)
    call precor()
    call plot
    mit = mit + 1
  end do
end program hello
