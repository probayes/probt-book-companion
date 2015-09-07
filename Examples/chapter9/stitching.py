from pyplpath import *
from pypl import *
#import math module
from math import * 
import os.path

plError.ignore_this_message(122,True)

#variables

#define the dimesion of the grid on which the boat is located
grid_half_dimension = 50
grid_discretization_steps = grid_half_dimension * 2

#define the probabilistic variables associated to location 
# used in the book
#coordinate_type = plIntegerType(-grid_half_dimension,grid_half_dimension)
#use to compile the code on pc
coordinate_type = plDiscreteIntervalType(-grid_half_dimension,grid_half_dimension,50)

XB=plVariable("XB", coordinate_type)
YB=plVariable("YB", coordinate_type)

#define the probabilistic variables associated to range and bearing
distance_type = plIntegerType(0,grid_half_dimension * 2)
bearing_type = plIntegerType(0,359)

#bearings
B1=plVariable("B1",bearing_type)
B2=plVariable("B2",bearing_type)
B3=plVariable("B3",bearing_type)

#define the function necessary to compute the mean and the standard deviation of the distance to 
# each beacon knowing the position XB and YB
 

#define the function necessary to of the bearing to 
#each beacon knowing the position XB and YB.

def radiantodegree(x):
    if x >= 0 :
        return 180 * x / pi
    else :
        return 360 + 180 * x / pi

def f_b_1(Output_,Input_):
    Output_[0]= radiantodegree(atan2(Input_[YB].to_float()-50.0,Input_[XB].to_float()-50.0))


def f_b_2(Output_,Input_):
    Output_[0]= radiantodegree(atan2(Input_[YB].to_float(),Input_[XB].to_float()-50.0))

def f_b_3(Output_,Input_):
    Output_[0]= radiantodegree(atan2(Input_[YB].to_float()-50.0,Input_[XB].to_float()))


#define the desciption 

JointDistributionList=plComputableObjectList()

#building the specification 
JointDistributionList.push_back(plUniform(XB))
JointDistributionList.push_back(plUniform(YB))

#distributions related to bearing 
JointDistributionList.push_back(plCndNormal(B1,XB^YB, \
                                               plPythonExternalFunction(XB^YB,f_b_1), \
                                                10.0))

JointDistributionList.push_back(plCndNormal(B2,XB^YB, \
                                               plPythonExternalFunction(XB^YB,f_b_2), \
                                                10.0))
JointDistributionList.push_back(plCndNormal(B3,XB^YB, \
                                               plPythonExternalFunction(XB^YB,f_b_3), \
                                                10.0))
#define the description
localisation_model_with_bearings=plJointDistribution(XB^YB^B1^B2^B3,JointDistributionList)

#question 1
PXBYB_K_B1B2B3=localisation_model_with_bearings.ask(XB^YB,B1^B2^B3)

bearing_reading_values=plValues(B1^B2^B3)
#estimating the location when the readings distances are perfect
# here we assume the boat to be at [0, 0, 0]
bearing_reading_values[B1]= 225
bearing_reading_values[B2]= 180
bearing_reading_values[B3]= 270

X=plVariable("X", coordinate_type)
Y=plVariable("Y", coordinate_type)



#define a copie to rename it 
PXY_K_B1B2B3=plCndDistribution(PXBYB_K_B1B2B3)
PXY_K_B1B2B3.rename(X^Y^B1^B2^B3)

#defines the model with distances

#distances
D1=plVariable("D1",distance_type)
D2=plVariable("D2",distance_type)
D3=plVariable("D3",distance_type)

XD=plVariable("XD", coordinate_type)
YD=plVariable("YD", coordinate_type)

distance_reading_values=plValues(D1^D2^D3)
#estimating the location when the readings (distances and bearing) are perfect
# here we assume the boat to be at [0, 0, 0]
distance_reading_values[D1]= 50 * sqrt(2)
distance_reading_values[D2]= 50
distance_reading_values[D3]= 50


#define the means the standard deviations
def fg_d_1(Output_,Input_):
    m = hypot( Input_[XD].to_float()+50.0,Input_[YD].to_float()+50.0)
    Output_[0] = m
    Output_[1] = m/10.0 + 5

def fg_d_2(Output_,Input_):
    m = hypot(Input_[XD].to_float()+50.0,Input_[YD].to_float())
    Output_[0] = m
    Output_[1] = m/10.0 + 5

def fg_d_3(Output_,Input_):
    m = hypot(Input_[XD].to_float(),Input_[YD].to_float()+50.0)
    Output_[0] = m 
    Output_[1] = m/10.0 + 5


JointDistributionList=plComputableObjectList()
#building the specification 
JointDistributionList.push_back(plUniform(XD))
JointDistributionList.push_back(plUniform(YD))

#distribuitons related to distances
JointDistributionList.push_back(plCndNormal(D1,XD^YD, \
                                               plPythonExternalFunction(XD^YD,fg_d_1)))
JointDistributionList.push_back(plCndNormal(D2,XD^YD, \
                                               plPythonExternalFunction(XD^YD,fg_d_2)))
JointDistributionList.push_back(plCndNormal(D3,XD^YD, \
                                               plPythonExternalFunction(XD^YD,fg_d_3)))

#define the description
localisation_model_with_distance=plJointDistribution(XD^YD^D1^D2^D3,JointDistributionList)

PXDYD_K_D1D2D3=localisation_model_with_distance.ask(XD^YD,D1^D2^D3)
PXY_K_D1D2D3=plCndDistribution(PXDYD_K_D1D2D3)
PXY_K_D1D2D3.rename(X^Y^D1^D2^D3)

#stitching 
JointDistributionList=plComputableObjectList()
JointDistributionList.push_back(plUniform(D1))
JointDistributionList.push_back(plUniform(D2))
JointDistributionList.push_back(plUniform(D3))
JointDistributionList.push_back(plUniform(B1))
JointDistributionList.push_back(plUniform(B2))
JointDistributionList.push_back(plUniform(B3))
JointDistributionList.push_back(PXDYD_K_D1D2D3)
JointDistributionList.push_back(PXBYB_K_B1B2B3)

def cbf(out, XbYb):
    out[0] = -XbYb[0].to_int()
    out[1] = -XbYb[1].to_int()

def cdf(out, XdYd):
    out[0] = XdYd[0].to_int()
    out[1] = XdYd[1].to_int()

CD = plVariable("CD", PL_BINARY_TYPE)
PCD__XdYd = plIneqConstraint(CD, plPythonExternalFunction(XD^YD, cdf), 2)
JointDistributionList.push_back(PCD__XdYd)

CB = plVariable("CB", PL_BINARY_TYPE)
PCB__XbYb = plIneqConstraint(CB, plPythonExternalFunction(XB^YB, cbf), 2)
JointDistributionList.push_back(PCB__XbYb)
    
PXY = plDistributionTable(X^Y, D1^D2^D3^B1^B2^B3^CD^CB, CD^CB)
vcdcb = plValues(CD^CB)
vcdcb[CD] = 1
vcdcb[CB] = 0
PXY.push(PXY_K_D1D2D3, vcdcb)

vcdcb[CD] = 0
vcdcb[CB] = 1
PXY.push(PXY_K_B1B2B3, vcdcb)

PXY.push_default(plComputableObject(plUniform(X)*plUniform(Y)))


JointDistributionList.push_back(PXY)

stitch_model = plJointDistribution(JointDistributionList)

PXYS=stitch_model.ask(X^Y,D1^D2^D3^B1^B2^B3)
sensor_reading_values=plValues(D1^D2^D3^B1^B2^B3)

#estimating the location when the readings (distances and bearing) are perfect
# here we assume the boat to be at [0, 0, 0]
sensor_reading_values[D1]= 50 * sqrt(2)
sensor_reading_values[D2]= 50
sensor_reading_values[D3]= 50

sensor_reading_values[B1]= 225
sensor_reading_values[B2]= 180
sensor_reading_values[B3]= 270

PXYSI=PXYS.instantiate(sensor_reading_values)
#takes several minutes 

PXYSI.plot(os.path.join(ExDir, 'chapter9', 'figures', 'PXYsample'))

#PXYSIc = PXYSI
#PXYSIc.to_eps(X, Y, os.path.join(ExDir, 'chapter9', 'figures'), 'PXYS')



