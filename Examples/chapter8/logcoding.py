from pyplpath import *

from pypl import *
import math


#define the function for the water unit

def LogCoding(Output_, Input_):
    if Input_[A].to_float() == math.floor(math.log(Input_[B].to_float(),2))  :
        Output_[LAMBDA]=1
    else :
        Output_[LAMBDA]=0
    return

WBtype = plIntegerType(1,255)
WAtype = plIntegerType(1,7)

A=plSymbol('A',WAtype)
B=plSymbol('B',WBtype)
LAMBDA = plSymbol('LAMBDA',plIntegerType(0,1))

jointlist=plComputableObjectList()
jointlist.push_back(plUniform(A))
jointlist.push_back(plUniform(B))
diracDistrib = plFunctionalDirac(LAMBDA,A^B,plPythonExternalFunction(LAMBDA,A^B,LogCoding))
allvals = plValues(A^B^LAMBDA)
allvals[A]=3
allvals[B]=9
print diracDistrib.instantiate(allvals)
jointlist.push_back(plFunctionalDirac(LAMBDA,A^B,plPythonExternalFunction(LAMBDA,A^B,LogCoding)))

model=plJointDistribution(LAMBDA^A^B, jointlist)
question = model.ask(A,LAMBDA)
question.instantiate(1).compile().plot(ExDir+'chapter8/figures/logassignBtoA',PL_POSTSCRIPT_PLOT)

 
jointlist=plComputableObjectList()
jointlist.push_back(plUniform(A))
jointlist.push_back(plNormal(B,32,30))
diracDistrib = plFunctionalDirac(LAMBDA,A^B,plPythonExternalFunction(LAMBDA,A^B,LogCoding))
allvals = plValues(A^B^LAMBDA)
allvals[A]=3
allvals[B]=9
print diracDistrib.instantiate(allvals)
jointlist.push_back(plFunctionalDirac(LAMBDA,A^B,plPythonExternalFunction(LAMBDA,A^B,LogCoding)))

model=plJointDistribution(LAMBDA^A^B, jointlist)
question = model.ask(A,LAMBDA)
question.instantiate(1).compile().plot(ExDir+'chapter8/figures/logassignBGausstoA',PL_POSTSCRIPT_PLOT)


























    













