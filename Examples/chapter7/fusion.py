from pyplpath import *
from pypl import *
#import math module
from math import * 
import os.path

#variables

#define the dimesion of the grid on which the boat is located
grid_half_dimension = 50
grid_discretization_steps = grid_half_dimension * 2

#define the probabilistic variables associated to location 
coordinate_type = plIntegerType(-grid_half_dimension,grid_half_dimension)
X=plVariable("X", coordinate_type)
Y=plVariable("Y", coordinate_type)

#define the probabilistic variables associated to range and bearing
distance_type = plIntegerType(0,grid_half_dimension * 2)
bearing_type = plIntegerType(0,359)

#distances
D1=plVariable("D1",distance_type)
D2=plVariable("D2",distance_type)
D3=plVariable("D3",distance_type)

#bearings
B1=plVariable("B1",bearing_type)
B2=plVariable("B2",bearing_type)
B3=plVariable("B3",bearing_type)

#define the function necessary to compute the mean and the standard deviation of the distance to 
# each beacon knowing the position X and Y

#define the means 
def f_d_1(Output_,Input_):
    Output_[0] =  hypot( Input_[X].to_float()+50.0,Input_[Y].to_float()+50.0)

def f_d_2(Output_,Input_):
    Output_[0] = hypot(Input_[X].to_float()+50.0,Input_[Y].to_float())

def f_d_3(Output_,Input_):
    Output_[0] =  hypot(Input_[X].to_float(),Input_[Y].to_float()+50.0)

#define the standard deviation 
def g_d_1(Output_,Input_):
    Output_[0]= hypot( Input_[X].to_float()+50.0,Input_[Y].to_float()+50.0) /10.0 + 5
    if Output_[0].to_float() <= 0.0 : 
        print "g_d_1 = ezero"

def g_d_2(Output_,Input_):
    Output_[0]= hypot(Input_[X].to_float()+50.0,Input_[Y].to_float())/10.0 + 5
    if Output_[0].to_float() <= 0.0 : 
        print "g_d_2 = zero"

def g_d_3(Output_,Input_):
    Output_[0]= hypot(Input_[X].to_float(),Input_[Y].to_float()+50.0) /10.0 + 5
    if Output_[0].to_float() <= 0.0 : 
        print "g_d_3 = zero"

#define the function necessary to of the bearing to 
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



#define the desciption 

JointDistributionList=plComputableObjectList()

#building the specification 
JointDistributionList.push_back(plUniform(X))
JointDistributionList.push_back(plUniform(Y))

#distribuitons related to distances
JointDistributionList.push_back(plCndNormal(D1,X^Y, \
                                               plPythonExternalFunction(X^Y,f_d_1), \
                                                plPythonExternalFunction(X^Y,g_d_1)))
JointDistributionList.push_back(plCndNormal(D2,X^Y, \
                                               plPythonExternalFunction(X^Y,f_d_2), \
                                                plPythonExternalFunction(X^Y,g_d_2)))
JointDistributionList.push_back(plCndNormal(D3,X^Y, \
                                               plPythonExternalFunction(X^Y,f_d_3), \
                                                plPythonExternalFunction(X^Y,g_d_3)))

#distributions related to bearing 
JointDistributionList.push_back(plCndNormal(B1,X^Y, \
                                               plPythonExternalFunction(X^Y,f_b_1), \
                                                10.0))
JointDistributionList.push_back(plCndNormal(B2,X^Y, \
                                               plPythonExternalFunction(X^Y,f_b_2), \
                                                10.0))
JointDistributionList.push_back(plCndNormal(B3,X^Y, \
                                               plPythonExternalFunction(X^Y,f_b_3), \
                                                10.0))
#define the description
localisation_model=plJointDistribution(X^Y^D1^D2^D3^B1^B2^B3,JointDistributionList)


#question 1
PXY_K_D1D2D3B1B2B3=localisation_model.ask(X^Y,D1^D2^D3^B1^B2^B3)
print PXY_K_D1D2D3B1B2B3 

sensor_reading_values=plValues(D1^D2^D3^B1^B2^B3)

#estimating the location when the readings (distances and bearing) are perfect
# here we assume the boat to be at [0, 0, 0]
sensor_reading_values[D1]= 50 * sqrt(2)
sensor_reading_values[D2]= 50
sensor_reading_values[D3]= 50

sensor_reading_values[B1]= 225
sensor_reading_values[B2]= 180
sensor_reading_values[B3]= 270

PXY=PXY_K_D1D2D3B1B2B3.instantiate(sensor_reading_values)
#to draw the dirtirubution used in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures'), 'loc00')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_soft'), PL_EPS_PLOT)
#question 2 : when only the bearings are known 
PXY_K_B1B2B3=localisation_model.ask(X^Y,B1^B2^B3)
print PXY_K_B1B2B3
sensor_reading_values[B1]= 225
sensor_reading_values[B2]= 180
sensor_reading_values[B3]= 270
PXY=PXY_K_B1B2B3.instantiate(sensor_reading_values)
#to draw the ditribution as in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures'), 'loc00_with_bearings_only')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_with_bearings_only_soft'), PL_EPS_PLOT)

#question 3 : when only the two distances are known 
PXY_K_D2D3=localisation_model.ask(X^Y,D2^D3)
print PXY_K_D2D3
sensor_reading_values[D2]= 50
sensor_reading_values[D3]= 50
PXY=PXY_K_D2D3.instantiate(sensor_reading_values)
#to draw the ditribution as in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures'), 'loc00_with_D2_and_D3_only')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_with_D2_and_D3_only_soft'), PL_EPS_PLOT)

#question 4 : with three distances but with a wrong distance for D3
PXY_K_D1D2D3=localisation_model.ask(X^Y,D1^D2^D3)
print PXY_K_D1D2D3
sensor_reading_values[D1]= 50 * sqrt(2.0)
sensor_reading_values[D2]= 50
sensor_reading_values[D3]= 70
PXY=PXY_K_D1D2D3.instantiate(sensor_reading_values)
#to draw the ditribution as in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures'),'loc00_with_D1_D2_ok_and_D3_wrong')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_with_D1_D2_ok_and_D3_wrong_soft'), PL_EPS_PLOT)

#Estimating the location when one reading is an outlier (case 2)
# here we assume the boat to be at [0, 0, 0]
sensor_reading_values[D1]= 50 * sqrt(2)
sensor_reading_values[D2]= 50
sensor_reading_values[D3]= 50

sensor_reading_values[B1]= 225
sensor_reading_values[B2]= 100 #here is the incoherent value 
sensor_reading_values[B3]= 270
PXY=PXY_K_D1D2D3B1B2B3.instantiate(sensor_reading_values)
#to draw the ditribution as in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures'),'loc00_with_one_error')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_with_one_error_soft'), PL_EPS_PLOT  )



sensor_reading_values[B2]= 180 #coherent value 

#question 4 : Where to look for landmark 3 if we know the location of the landmarks 1 and  2
PB3_K_B1B2D1D2=localisation_model.ask(B3,B1^B2^D1^D2)
PB3=PB3_K_B1B2D1D2.instantiate(sensor_reading_values)
PB3.plot(os.path.join(ExDir, 'chapter7', 'figures', 'B3'), PL_POSTSCRIPT_PLOT)

#new model when standard deviation on Bearings  depends on distance  
def g_b_1(Output_,Input_):
    Output_[0] = max (5, 20 - 500 / (10+ Input_[D1].to_float()))

def g_b_2(Output_,Input_):
    Output_[0] = max(5, 20 - 500 / (10 + Input_[D2].to_float()))

def g_b_3(Output_,Input_):
    Output_[0] = max(5, 20 - 500 / (10 + Input_[D3].to_float()))


JointDistributionList=plComputableObjectList()

#building the specification 
JointDistributionList.push_back(plUniform(X))
JointDistributionList.push_back(plUniform(Y))

#distribuitons related to distances
JointDistributionList.push_back(plCndNormal(D1,X^Y, \
                                               plPythonExternalFunction(X^Y,f_d_1), \
                                                plPythonExternalFunction(X^Y,g_d_1)))
JointDistributionList.push_back(plCndNormal(D2,X^Y, \
                                               plPythonExternalFunction(X^Y,f_d_2), \
                                                plPythonExternalFunction(X^Y,g_d_2)))
JointDistributionList.push_back(plCndNormal(D3,X^Y, \
                                               plPythonExternalFunction(X^Y,f_d_3), \
                                                plPythonExternalFunction(X^Y,g_d_3)))

#distributions related to bearing 
JointDistributionList.push_back(plCndNormal(B1,X^Y^D1, \
                                               plPythonExternalFunction(X^Y^D1,f_b_1), \
                                               plPythonExternalFunction(X^Y^D1,g_b_1)))
JointDistributionList.push_back(plCndNormal(B2,X^Y^D2, \
                                               plPythonExternalFunction(X^Y^D2,f_b_2), \
                                               plPythonExternalFunction(X^Y^D2,g_b_2)))
JointDistributionList.push_back(plCndNormal(B3,X^Y^D3, \
                                               plPythonExternalFunction(X^Y^D3,f_b_3), \
                                               plPythonExternalFunction(X^Y^D3,g_b_3)))
#define the description
new_localisation_model=plJointDistribution(X^Y^D1^D2^D3^B1^B2^B3,JointDistributionList)

#question 3 : when only the bearings are known 
PXY_K_B1B2B3=new_localisation_model.ask(X^Y,B1^B2^B3)
print PXY_K_B1B2B3
sensor_reading_values[B1]= 225
sensor_reading_values[B2]= 180
sensor_reading_values[B3]= 270
PXY=PXY_K_B1B2B3.instantiate(sensor_reading_values)
#to draw the ditribution as in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures), 'loc00_M2_with_bearings_only')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'loc00_M2_with_bearings_only_soft'), PL_EPS_PLOT)

