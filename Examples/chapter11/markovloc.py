from pyplpath import *

from pypl import *
#import math module
import math
from math import * 

#variables

#define the dimesion of the grid on which the boat is located
grid_half_dimension = 50
grid_discretization_steps = grid_half_dimension * 2

#define the probabilistic variables associated to the location 
coordinate_type = plDiscreteIntervalType(-grid_half_dimension,grid_half_dimension,30)

Xt_1=plSymbol("Xt_1", coordinate_type)
Yt_1=plSymbol("Yt_1", coordinate_type)
Xt=plSymbol("Xt", coordinate_type)
Yt=plSymbol("Yt", coordinate_type)

#define the probabilistic variables associated to the location 
speed_type = plIntegerType(-5,+5)

Mxt_1=plSymbol("Mxt_1", speed_type)
Myt_1=plSymbol("Myt_1", speed_type)


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

#gives the next location 
def f_vx(Output_,Input_) :
    Output_[0]=Input_[Xt_1].to_float()+ Input_[Mxt_1].to_float()
def f_vy(Output_,Input_) :
    Output_[0]=Input_[Yt_1].to_float()+ Input_[Myt_1].to_float()


#define the initial desciption 



#recusive specification : 
#define the initial distribution  X_0 Y_0
PXt_1Yt_1=plMutableDistribution(plDistribution(plUniform(Xt_1)*plUniform(Yt_1)))

JointDistributionList=plComputableObjectList()
#use the mutable distibution as the prior on the state distribution 
JointDistributionList.push_back(PXt_1Yt_1)
#use avialable knowledge on M_t :
JointDistributionList.push_back(plUniform(Mxt_1))
JointDistributionList.push_back(plUniform(Myt_1))
#define the transition model with motor commands 
JointDistributionList.push_back(plCndNormal(Xt,Xt_1^Mxt_1,\
                                plPythonExternalFunction(Xt_1^Mxt_1,f_vx),2))
JointDistributionList.push_back(plCndNormal(Yt,Yt_1^Myt_1, \
                                plPythonExternalFunction(Yt_1^Myt_1,f_vy),2))
#define the sensor model
JointDistributionList.push_back(plCndNormal(B1,Xt^Yt, \
                                               plPythonExternalFunction(Xt^Yt,f_b_1), \
                                                10.0))
JointDistributionList.push_back(plCndNormal(B2,Xt^Yt, \
                                               plPythonExternalFunction(Xt^Yt,f_b_2), \
                                                10.0))
JointDistributionList.push_back(plCndNormal(B3,Xt^Yt, \
                                               plPythonExternalFunction(Xt^Yt,f_b_3), \
                                                10.0))
#define the joint distribution 
filtered_localisation_model=plJointDistribution(JointDistributionList)

#define the question on new state 
PXY_K_B1B2B3=filtered_localisation_model.ask(Xt^Yt,B1^B2^B3^Mxt_1^Myt_1)
print PXY_K_B1B2B3

sensor_reading_values=plValues(B1^B2^B3^Mxt_1^Myt_1)
V=[[225,169,280,8,8], [225,154,295,8,8], [225,137,312,8,8]]
#V=[ [227, 180, 273,3,3], [228,180,277,3,3], [230,180,280,3,3]]
i=1
for val in V :
    #read the observations
    sensor_reading_values[B1]= val[0]
    sensor_reading_values[B2]= val[1]
    sensor_reading_values[B3]= val[2]
    sensor_reading_values[Mxt_1]= val[3]
    sensor_reading_values[Myt_1]= val[4]
    print sensor_reading_values
    #estimate the state 
    PXY=PXY_K_B1B2B3.instantiate(sensor_reading_values)
    compiled_PXY=PXY.compile()
    outputfile = ExDir+'chapter11/figures/VPXY_{0}'.format(i)
    compiled_PXY.plot(outputfile)
    #Prepare next iteration  
    compiled_PXY.rename(Xt_1^Yt_1)
    PXt_1Yt_1.mutate(compiled_PXY)
    i=i+1

print 'titi'

