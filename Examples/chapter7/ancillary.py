from pyplpath import *
from pypl import *
from math import * 
import os.path

#variables

#define the dimesion of the grid on which the boat is located
grid_half_dimension = 50
grid_discretization_steps = grid_half_dimension * 2

#define the probabilistic variables associated to location 
coordinate_type = plIntegerType(-grid_half_dimension,grid_half_dimension)
X=plSymbol("X", coordinate_type)
Y=plSymbol("Y", coordinate_type)

#define the probabilistic variables associated to range and bearing
bearing_type = plIntegerType(0,359)

#bearings
B1=plSymbol("B1",bearing_type)
B2=plSymbol("B2",bearing_type)
B3=plSymbol("B3",bearing_type)

#Ancilary Variable "
V =plSymbol("V",plLabelType(["true","false"]))

#define the function necessary to get bearing to 
#each beacon knowing the position X and Y.

def radiantodegree(x):
    if x >= 0 :
        return 180 * x / pi
    else :
        return 360 + 180 * x / pi

def f_b_1(Output_,Input_):
    Output_[0]= radiantodegree(atan2(Input_[Y].to_float()-50.0,Input_[X].to_float()-50.0))

def f_b_2(Output_,Input_):
    Output_[0]= radiantodegree(atan2(Input_[Y].to_float(),Input_[X].to_float()-50.0))

def f_b_3(Output_,Input_):
    Output_[0]= radiantodegree(atan2(Input_[Y].to_float()-50.0,Input_[X].to_float()))

#define the function necessary to get the precision on the bearing 
#knowing the anciliary clue 

def g_b (Output_,Input_) :
    if Input_[V].to_float()== 0 : 
        Output_[0]= 10
    else :
        Output_[0]= 30

#define the desciption 
JointDistributionList=plComputableObjectList()

#building the specification 
JointDistributionList.push_back(plUniform(X))
JointDistributionList.push_back(plUniform(Y))

#building soft evidence 
#here assume no visibility 
JointDistributionList.push_back(plProbTable(V,[0,1]))

#distributions related to bearing 
JointDistributionList.push_back(plCndNormal(B1,X^Y^V, \
                                               plPythonExternalFunction(X^Y^V,f_b_1), \
                                               plPythonExternalFunction(X^Y^V,g_b)))
JointDistributionList.push_back(plCndNormal(B2,X^Y^V, \
                                               plPythonExternalFunction(X^Y^V,f_b_2), \
                                                plPythonExternalFunction(X^Y^V,g_b)))
JointDistributionList.push_back(plCndNormal(B3,X^Y^V, \
                                               plPythonExternalFunction(X^Y^V,f_b_3), \
                                               plPythonExternalFunction(X^Y^V,g_b)))
#define the description
localisation_model=plJointDistribution(X^Y^V^B1^B2^B3,JointDistributionList)

sensor_reading_values=plValues(B1^B2^B3)

# here we assume the boat to be at [0, 0, 0]
sensor_reading_values[B1]= 225
sensor_reading_values[B2]= 180
sensor_reading_values[B3]= 270

#estimating the location with low visibility 
PXY_K_B1B2B3=localisation_model.ask(X^Y,B1^B2^B3)
PXY=PXY_K_B1B2B3.instantiate(sensor_reading_values)
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_with_ancillary_set_to_false'))

#estimating the location with High visibility 
localisation_model.replace(V,plProbTable(V,[1,0]))
PXY_K_B1B2B3=localisation_model.ask(X^Y,B1^B2^B3)
PXY=PXY_K_B1B2B3.instantiate(sensor_reading_values)
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_with_ancillary_set_to_true'))

#estimating the location with low visibility 
localisation_model.replace(V,plProbTable(V,[0.1,0.9]))
PXY_K_B1B2B3=localisation_model.ask(X^Y,B1^B2^B3)
PXY=PXY_K_B1B2B3.instantiate(sensor_reading_values)
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_with_soft_evidence'))


#estimating the location with approximate visibility 
localisation_model.replace(V,plProbTable(V,[0.5,0.5]))
PXY_K_B1B2B3=localisation_model.ask(X^Y,B1^B2^B3)
PXY=PXY_K_B1B2B3.instantiate(sensor_reading_values)
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_with_soft_evidence_05'))

