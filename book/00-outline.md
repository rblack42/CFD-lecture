# Lecture Outline

(* indicates picture, + indicates physical example)

1. How did you get here?
	- Grow up in the Smithsonian (Wright Flyer *)
	- Take a ride in a Connie (*)
2. Human Flight
    - Build something and jump off a cliff
        - DaVinci Ornithopter (*)
    - Models are safer
        - Indoor models (*)
        - Serious wind tunnel models (*)
        - Another way? The Numerical Wind Tunnel
3. The Math of Flight
    - Leibnitz calculus (1684)
    - Isaac Newton laws of motion (1687)
    - Taylor Series (1715)
        - finite differences
    - Rankine laws of thermodynamics (1850)
    - Navier Stokes (1822-1850)
    - Add in gas laws
    - Then find a way to solve them
        - lop off terms to make them easier
        - Potential flow - we could figure out airfoils!
    - We need a better way!
4. Basic Computers
    - Abacus (*,+)
    - Mechanical calculating machines
        - Da Vinci drawing
        - Blaise Pascal's Pascaline (+)
        - Babbage Engine
            - Ada Agusta Lovelace invented programming (1843)
            - Jacquard Loom punched cards (1804)
        - Curta Calculator (*,+)
            - developed during WWII by prisoner
            - replaced my slide rule (+)
    - World War II
        - Harvard Mark 1 (1944) (+ book)
            - Grace Hopper
        - John Von Neumanm describes a computer architecture (1945) (*)
        - ENIAC (1945) (*.+)
    - Mainframe Era
        - IBM 360 (1964) (*)
            - powered Va Tech
            - six at Johnson Space Center for Apollo
    - Shockley's Transistor ( (1956) (*,+)
5. Supercomputers
    - CDC-6600 (1964) first "supercomputer" (*)
        - Powered early CFD work (my PNS code)
    - ILLIAC IV at NASA Ames (*)
        - First parallel machine
6. Serious Supercomputers
    - Cray-1 (1973) (*,+)
        - first vector machine 64 numbers high!
        - Programmed in assembly language initially!
7. Integrated Circuits
    - Intel 4004 (1971) (*)
        - designed for calculators (4-bits)
    - Intel 8080
        - first home computers
    - KIM-1 board (*)
        - used as a trainer for Cray programming!
8. Shrinking Chips
    - 8086 16-bit machine
        - powered first IBM PCs
    - now at 3nm - 10-80 thousand times smaller than hair (+)
    - IBM logo (1989) (*)
9. Hitting the Wall
    - Intel "dual core" chip (1993) (*,+)
10 Multi-Core Supercomputers
    - Cray 2 (1985) 4 processors reached 1.9 GFLOPS! (*)
    - Beowulf Clusters (+)
        - small PCs on a network (NASA 1998)
        - limited by network speed (Grace Hopper's wire)
11. Clustered Supercomputers
    - Connection Machine - 65536 microprocessors (*)
12. GPU Development
    - Thank gamers for this
    - GPU on a chip

13. Today's machines
    - NCAR Cheyenne 145000 Intel Xeon processors) (*)
    - DOE Frontier (8699905 AMD chips) (*)
14. Custom Chips
    - FPGA
    - CFD Engines?
        - AI Powered or designed?
        - Adaptive machines

15. CFD Today
    - Early work in limited memory trained us to break problem up
        - training for parallel machines
    - Start small, then build up        
        - axisymmetric flow - to full 3D
        - MacCormack's Predictor-Corrector
        - Beam-Warming for better (more stable) solutions
    - Use Symbolic Math
        - I validated Beam-Warming code using Macsyma at MIT
    - Parallel Programming
        - Think your code through
        - Use libraries like MPI to move data between machines
        - Let advanced compilers help (Modern Fortran)
        - Baby Clusters
            - Raspberry Pi cluster - Cheap!



