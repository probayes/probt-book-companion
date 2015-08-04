from pyplpath import *

from pypl import *
#import math module
from math import * 

#variables
#define the dimesion of the grid on which the boat is located
grid_half_dimension = 50
grid_discretization_steps = grid_half_dimension * 2

#define the probabilistic variables associated to location 
coordinate_type = plIntegerType(-grid_half_dimension,grid_half_dimension)
X=plSymbol("X", coordinate_type)
Y=plSymbol("Y", coordinate_type)

#define the probabilistic variables associated to range and bearing
distance_type = plIntegerType(0,grid_half_dimension * 2)
bearing_type = plIntegerType(0,359)

#distances
D2=plSymbol("D2",distance_type)
D3=plSymbol("D3",distance_type)

#fault tree
F2=plSymbol("F2",plIntegerType(0,1))
F3=plSymbol("F3",plIntegerType(0,1))
A2=plSymbol("A2",plIntegerType(0,1))
A3=plSymbol("A3",plIntegerType(0,1))
B2=plSymbol("B2",plIntegerType(0,1))
B3=plSymbol("B3",plIntegerType(0,1))


#define the function necessary to compute the mean and the standard deviation of the distance to 
# each beacon knowing the position X and Y

#define the means 

def f_d_2(Output_,Input_):
    Output_[0] = hypot(Input_[X].to_float()+50.0,Input_[Y].to_float())

def f_d_3(Output_,Input_):
    Output_[0] =  hypot(Input_[X].to_float(),Input_[Y].to_float()+50.0)

#define the standard deviation 

def g_d_2(Output_,Input_):
    Output_[0]= hypot(Input_[X].to_float()+50.0,Input_[Y].to_float())/10.0 + 1

def g_d_3(Output_,Input_):
    Output_[0]= hypot(Input_[X].to_float(),Input_[Y].to_float()+50.0) /10.0 + 1

#define the logical operators for the fault tree

def external_and(Output_,Input_):
    Output_[0]=Input_[A2].to_int() & Input_[B2].to_int()

def external_or(Output_,Input_):
    Output_[0]= Input_[A3].to_int() | Input_[B3].to_int()



#define the desciption for sensor2
JointDistributionList=plComputableObjectList()

#building the specification 
JointDistributionList.push_back(plUniform(X))
JointDistributionList.push_back(plUniform(Y))

#define probability for the causes of failure
JointDistributionList.push_back(plProbTable(A2,[0.8,0.2]))
#define probability for the causes of failure
JointDistributionList.push_back(plProbTable(B2,[0.9,0.1]))
#define the fault tree for sensor 2
extfunctionalmodel=plPythonExternalFunction(F2,A2^B2,external_and)
JointDistributionList.push_back(plCndDeterministic(F2,A2^B2,extfunctionalmodel))
#define the sensormodel
sensordistrib=plDistributionTable(D2,X^Y^F2,F2)
#push the standard model when the sensor is working F2=0
sensordistrib.push(plCndNormal(D2,X^Y, \
                                               plPythonExternalFunction(X^Y,f_d_2), \
                                                plPythonExternalFunction(X^Y,g_d_2)),0)
#push a unifrom distribution when the sensor is not working F2=1
sensordistrib.push(plUniform(D2),1)

JointDistributionList.push_back(sensordistrib)

sensor_model2=plJointDistribution(X^Y^D2^F2^A2^B2,JointDistributionList)
#define the "reduce sensor model for senor 2"
PD2_K_XY=sensor_model2.ask(D2,X^Y)



########################################################
#define the desciption for sensor3
JointDistributionList=plComputableObjectList()

#building the specification 
JointDistributionList.push_back(plUniform(X))
JointDistributionList.push_back(plUniform(Y))

#define probability for the causes of failure
JointDistributionList.push_back(plProbTable(A3,[0.99,0.01]))
#define probability for the causes of failure
JointDistributionList.push_back(plProbTable(B3,[0.98,0.02]))
#define the fault tree for sensor 3
extfunctionalmodel=plPythonExternalFunction(F3,A3^B3,external_or)
JointDistributionList.push_back(plCndDeterministic(F3,A3^B3,extfunctionalmodel))
#define the sensormodel
sensordistrib=plDistributionTable(D3,X^Y^F3,F3)
#push the standard model when the sensor is working : F3=0
sensordistrib.push(plCndNormal(D3,X^Y, \
                   plPythonExternalFunction(X^Y,f_d_3), \
                   plPythonExternalFunction(X^Y,g_d_3)),0)
#push a unifrom distribution when the sensor is not working : F2=1
sensordistrib.push(plUniform(D3),1)

JointDistributionList.push_back(sensordistrib)


sensor_model3=plJointDistribution(X^Y^D3^F3^A3^B3,JointDistributionList)

#define the "reduce sensor model for senor 2"
PD3_K_XY=sensor_model3.ask(D3,X^Y)

########################################
#define the program main 
JointDistributionList=plComputableObjectList()
JointDistributionList.push_back(plComputableObject(plUniform(X)*plUniform(Y)))
JointDistributionList.push_back(sensor_model3.ask(D3,X^Y))
JointDistributionList.push_back(sensor_model2.ask(D2,X^Y))
main_model=plJointDistribution(X^Y^D3^D2,JointDistributionList)
question=main_model.ask(X^Y,D2^D3)


print question.instantiate([50,50]).compile()

