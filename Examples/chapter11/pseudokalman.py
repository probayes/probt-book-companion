from pyplpath import *

from pypl import *
#import math module
import math
from math import * 

#variables

#define the dimesion of the grid on which the boat is located
grid_half_dimension = 50
grid_discretization_steps = grid_half_dimension * 2

#define the probabilistic variables associated to location 
#coordinate_type = plIntegerType(-grid_half_dimension,grid_half_dimension)
coordinate_type = plDiscreteIntervalType(-grid_half_dimension,grid_half_dimension,20)

Xt_1=plSymbol("Xt_1", coordinate_type)
Yt_1=plSymbol("Yt_1", coordinate_type)
Xt=plSymbol("Xt", coordinate_type)
Yt=plSymbol("Yt", coordinate_type)

#define the probabilistic variables associated to range and bearing
distance_type = plIntegerType(0,grid_half_dimension * 2)
bearing_type = plIntegerType(0,359)

#bearings
B1=plSymbol("B1",bearing_type)
B2=plSymbol("B2",bearing_type)
B3=plSymbol("B3",bearing_type)

#define the function necessary to of the bearing to 
#each beacon knowing the position X and Y.

def radiantodegree(x):
    if x >= 0 :
        return 180 * x / pi
    else :
        return 360 + 180 * x / pi

def f_b_1(Output_,Input_):
    Output_[0]= radiantodegree(atan2(Input_[Yt].to_float()-50.0,Input_[Xt].to_float()-50.0))

def f_b_2(Output_,Input_):
    Output_[0]= radiantodegree(atan2(Input_[Yt].to_float(),Input_[Xt].to_float()-50.0)) 

def f_b_3(Output_,Input_):
    Output_[0]= radiantodegree(atan2(Input_[Yt].to_float()-50.0,Input_[Xt].to_float()))

#define a mutable distribution for the states :
PXt_1Yt_1=plMutableDistribution(plDistribution(plUniform(Xt_1)*plUniform(Yt_1)))
#start with the specification 
newJointDistributionList=plComputableObjectList()
#use the mutable distibution as the state distribution 
newJointDistributionList.push_back(PXt_1Yt_1)
#define the transition model 
newJointDistributionList.push_back(plCndNormal(Xt,Xt_1,5))
newJointDistributionList.push_back(plCndNormal(Yt,Yt_1,5))
#define the sensor model
newJointDistributionList.push_back(plCndNormal(B1,Xt^Yt, \
                                               plPythonExternalFunction(Xt^Yt,f_b_1), \
                                                10.0))
newJointDistributionList.push_back(plCndNormal(B2,Xt^Yt, \
                                               plPythonExternalFunction(Xt^Yt,f_b_2), \
                                                10.0))
newJointDistributionList.push_back(plCndNormal(B3,Xt^Yt, \
                                               plPythonExternalFunction(Xt^Yt,f_b_3), \
                                                10.0))
#define the joint distribution 
filtered_localisation_model=plJointDistribution(newJointDistributionList)

#define the question on new state 
PXY_K_B1B2B3=filtered_localisation_model.ask(Xt^Yt,B1^B2^B3)

sensor_reading_values=plValues(B1^B2^B3)
V=[[225,180,270], [225,180,270], [225,180,270] ]
i=1
for val in V :
    #read the observations
    sensor_reading_values[B1]= val[0]
    sensor_reading_values[B2]= val[1]
    sensor_reading_values[B3]= val[2]
    #estimate the state 
    PXY=PXY_K_B1B2B3.instantiate(sensor_reading_values)
    compiled_PXY=PXY.compile()
    outputfile = ExDir+'chapter11/figures/finalPXY_{0}'.format(i)
    compiled_PXY.plot(outputfile)
    #Prepare next iteration  
    compiled_PXY.rename(Xt_1^Yt_1)
    PXt_1Yt_1.mutate(compiled_PXY)
    i=i+1







