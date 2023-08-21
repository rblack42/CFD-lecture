import numpy as np

class PropertyAnimator(object):
    
    def __init__(self, fname):
        fin = open(fname,'r')
        line = fin.readline()
        self.neta = int(line.split()[-1])
        self.lines = fin.readlines()
        fin.close()

    def unpack_axial_locations(self,lines):
        '''filter only axial location lines'''
        slist = list(filter(lambda x: x.startswith('A'), lines))
        return slist

    def unpack_properties(self,lines):
        '''filter only property lines'''
        plist = list(filter(lambda x: not x.startswith('A'), lines))
        tp = []
        for l in plist:
            parts = l.split()
            parts = [float(s) for s in parts]
            tp.append(parts[self.propNum])
        tp = np.array(tp)
        pmax = np.max(tp)
        pmin = np.min(tp)
        props = np.reshape(tp,(-1,31))
        return props, pmin, pmax


    def load(self, n=7):
        self.propNum = n
        self.stations = self.unpack_axial_locations(self.lines)
        self.properties, self.min, self.max = self.unpack_properties(self.lines)
        return self.stations, self.properties, self.max, self.min
    
    def run(self):
        pass

if __name__ == '__main__':
    pa = PropertyAnimator('solution.dat')
    stations, properties, pmin, pmax = pa.load(6)
    print(pmax, pmin, len(stations), len(properties))
    print(properties[0])
