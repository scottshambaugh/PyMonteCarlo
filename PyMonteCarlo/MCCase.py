from PyMonteCarlo.MCVal import MCOutVal

class MCCase():
    def __init__(self, ncase, mcinvars, isnom):
        self.ncase = ncase    # ncase is an integer
        self.isnom = isnom    # isnom is a boolean
        self.mcinvars = mcinvars  # mcvars is a dict of MCVar objects
        self.mcoutvars = dict()
        
        self.starttime = None
        self.endtime = None
        self.runtime = None
        
        self.mcinvals = self.getMCInVals()
        self.mcoutvals = dict()
        
        self.siminput = None


    def getMCInVals(self):
        mcvals = dict()
        for mcvar in self.mcinvars.values():
            mcval = mcvar.getVal(self.ncase)
            mcvals[mcval.name] = mcval
        return mcvals


    def getMCOutVals(self):
        mcvals = dict()
        for mcvar in self.mcoutvars.values():
            mcval = mcvar.getVal(self.ncase)
            mcvals[mcval.name] = mcval
        return mcvals
    
    
    def addOutVal(self, name, val, split=True):
        self.mcoutvals[name] = MCOutVal(name, self.ncase, val, self.isnom)
        if split:
            self.mcoutvals.update(self.mcoutvals[name].split())

'''
### Test ###
import numpy as np
from scipy.stats import norm
from MCVar import MCInVar
np.random.seed(74494861)
var = {'Test':MCInVar('Test', norm, (10, 4), 10)}
case = MCCase(0, var, False)
print(case.mcinvals['Test'].val)

case.addOutVal('TestOut', [[0,0],[0,0],[0,0]])
print(case.mcoutvals['TestOut'].val)
print(case.mcoutvals['TestOut'].size)
#'''