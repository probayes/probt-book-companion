from pyplpath import *
from pypl import *
import math
import os.path

def WriteVector(V,filename):
    f = open(filename,"w")
    for v in V :
        f.write('%f '%v)
    f.close()

def ReadVector(filename) :
    f = open(filename,"r")
    V = f.readline().strip().split(" ")
    fV = []
    for v in V :
        fV.append(float(v))
    f.close()
    return fV

#define the function for the water unit

def WfunctionalModel(Output_, Input_):
    alpha = math.floor((Input_[I0] + Input_[I1] + Input_[F] + Input_[C] - Input_[H])/3)
    ostar = math.floor((Input_[I0] + Input_[I1] + 10)/3)
    if alpha < 0 :
        Output_[O]=0
        return 
    elif alpha  <= ostar :
        Output_[O]=alpha
        return
    Output_[O] = 2*ostar - alpha 

# define function for the sensor
def WsensorModel(Output_,Input_):
    Output_[S]= math.floor((Input_[I0]+Input_[F])/2)

#define the type and the variables 

Wtype = plIntegerType(0,10)
I0=plSymbol('I0',Wtype)
I1=plSymbol('I1',Wtype)
F=plSymbol('F',Wtype)
S=plSymbol('S',Wtype)
C=plSymbol('C',Wtype)
O=plSymbol('O',Wtype)

#note the variable H which is used to perform the simulation
H=plSymbol('H',Wtype)


#used to build figure 3.11 
print 'figure 3.11' 
JointDistributionList=plComputableObjectList()

JointDistributionList.push_back(plUniform(I0))
JointDistributionList.push_back(plUniform(I1))
JointDistributionList.push_back(plUniform(C))
JointDistributionList.push_back(plUniform(H))
JointDistributionList.push_back(plUniform(F))

extfunctionalmodel=plPythonExternalFunction(O,I0^I1^C^F^H,WfunctionalModel)
JointDistributionList.push_back(plCndDeterministic(O,I0^I1^C^F^H,extfunctionalmodel))
extsensormodel=plPythonExternalFunction(S,I0^F,WsensorModel)
JointDistributionList.push_back(plCndDeterministic(S,I0^F,extsensormodel))

model=plJointDistribution(S^O^F^H^C^I1^I0, JointDistributionList)

#use to prepare the model used in chapter 6 
print 'preparing calibration file : take a break  > 5 minutes'
PO_K_I0I1CS = model.ask(O,I0^I1^S^C)
compiled_PO_K_I0I1CS = PO_K_I0I1CS.compile()
datafilename = os.path.join(ExDir, 'chapter6', 'data', 'calibration.txt')
table=plProbValueVector()
compiled_PO_K_I0I1CS.tabulate(table)
WriteVector(table,datafilename);
    



    
    







