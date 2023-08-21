A Short History of CFD and HPC
##############################
:Author: Roie R. Black
:Email: roie.black@gmail.com
:Docs: https://rblack42.github.io/CFD-talk

The project contains the notes I prepared for a lecture on the development of
High Performance Computing and Computational Fluid Dynamics, presented to
students in a CFD class at Kansas University in August, 2023. 

The repository contains an example program that solves the axisymmetric flow
over an ogive-cylinder shape flying at Mach 6. The solution scheme is a
Parabolized Navier-Stokes solver using MacCormack's method. I developed this
program in 1975 using Fortran IV, and it took 10 minutes to complete a solution on a CDC-6600 mainframe.

Today, it runs in under one second on my Macbook Pro (M1-Max) using Python!

This project is based on work I did in 1975 while
conducting research in CFD at the Aerospace Research Laboratory at
Wright-Patterson Air Force Base in Dayton, Ohio. This code was an initial step in my Ph.D.
program, sadly incomplete. However it is a nice, simple introduction to CFD.
