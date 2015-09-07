from pyplpath import *
from pypl import *
import math
import os.path

# definition of the variabes (4.3)
Dir = plVariable('Dir',plIntegerType(-10,10))
Prox = plVariable('Prox',plIntegerType(0,15))
Vrot = plVariable('VRot',plIntegerType(-10,10))

PDir = plUniform(Dir)
PProx = plUniform(Prox)

#avoid is obtained by orienting the front of the 
#robot in the oposit direction of the obstacle 
def meanfunctional(Output_ , Input_):
    Output_[0]= -Input_[Dir].to_float()

def varfunctional(Output_,Input_):
    Output_[0] = 18-(1*Input_[Prox].to_float())

fmean=plPythonExternalFunction(Dir^Prox,meanfunctional)
fvar=plPythonExternalFunction(Dir^Prox,varfunctional)

dl = plComputableObjectList()
dl.push_back(PDir)
dl.push_back(PProx)
dl.push_back(plCndNormal(Vrot,Dir^Prox,fmean,fvar))

Joint = plJointDistribution(Vrot^Dir^Prox,dl)

#simulate avoid
simulation_avoid_file=open(os.path.join(ExDir, 'chapter10', 'data', 'avoiding.csv'), 'w')
allval = plValues(Dir^Prox^Vrot)

for i in range(100):
    allval = Joint.draw()
    simulation_avoid_file.write('{0};{1};{2}\n'.format(allval[Vrot],\
                                                         allval[Dir],\
                                                         allval[Prox]))
simulation_avoid_file.close()




