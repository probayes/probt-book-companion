from pyplpath import *
from pypl import *
import math
import os.path

# definition of the variabes (4.3)
Dir = plSymbol('Dir',plIntegerType(-10,10))
Prox = plSymbol('Prox',plIntegerType(0,15))
Vrot = plSymbol('Vrot',plIntegerType(-10,10))

PDir = plUniform(Dir)
PProx = plUniform(Prox)

#following is obtained by orienting the front of the 
#robot in the direction of contact
def meanfunctional(Output_ , Input_):
    valdir = Input_[Dir].to_float()
    valprox = Input_[Prox].to_float()
    if valdir > 0 : 
        Output_[0]= 0.25 * (18-valprox) * (valdir - 10)
    else :
        Output_[0]= 0.25 * (18-valprox) * (valdir + 10)

def varfunctional(Output_,Input_):
    Output_[0] = 18-Input_[Prox].to_float()


fmean=plPythonExternalFunction(Dir^Prox,meanfunctional)
fvar=plPythonExternalFunction(Dir^Prox,varfunctional)

dl = plComputableObjectList()
dl.push_back(PDir)
dl.push_back(PProx)
dl.push_back(plCndNormal(Vrot,Dir^Prox,fmean,fvar))

Joint = plJointDistribution(Vrot^Dir^Prox,dl)

#simulate following
simulation_following_file=open(os.path.join(ExDir, 'chapter4', 'data', 'following.csv'),'w')
allval = plValues(Dir^Prox^Vrot)

for i in range(100):
    allval = Joint.draw()
    simulation_following_file.write('{0};{1};{2}\n'.format(allval[Vrot],\
                                                         allval[Dir],\
                                                         allval[Prox]))
simulation_following_file.close()

vals = plValues(Dir^Prox)
valr = plValues(Vrot)
vals[Dir]=6
vals[Prox]=14
meanfunctional(valr,vals)






