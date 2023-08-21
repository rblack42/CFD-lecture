from matplotlib.animation import FuncAnimation
import numpy as np
import sys


class PropertyAnimator:
    '''display selected flow field property'''

    def __init__(self, fname, prop = 7):
        try:
            fin = open(fname,'r')
        except IOError:
            print("file not found:", fname)
            sys.exit()
        print("Animation file:", fname)
        
        # get neta and frame count
        line = fin.readline()
        self.neta = int(line.split()[-1])
        print("Number of radial grid points:", self.neta)
    
        # load all remaining lines in solution
        self.lines = fin.readlines()
        self.nlines = len(self.lines)
        self.nframes = int(self.nlines/(self.neta + 1))
        print("Processing:", self.nlines," lines", self.nframes, " frames")
        print(self.lines[0])

        # count lines
        self.count = 0

        # count frames
        self.frame = 1

        # track axial location
        self.eta = float(self.lines[0].split()[-1])
        self.eta_cone = self.eta
        self.conical = True

    def increment(self):
        '''increment line counter'''
        self.count += 1
        if self.count % (self.neta + 1) == 0:
            self.line = self.lines[self.count]
            self.frame += 1
            self.eta = float(self.line.split()[-1])
            if self.eta > self.eta:
                self.conical = False
            print(self.line)

    def __call__(self):
        self.increment()
        print(self.count, self.frame, self.eta, self.conical)
        if self.count > self.nlines:
            print("reached count:", self.count)
            self.count = 0

if __name__ == '__main__':
    an = PropertyAnimator('solution.dat')

    while True:
        an()
    
    
