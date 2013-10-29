from pyplpath import *
# import the pypl module
from pypl import *
#import math module
from math import * 
import os.path

#variables

#define the dimension of the grid on which the boat is located
grid_half_dimension = 50
grid_discretization_steps = grid_half_dimension * 2

#define the probabilistic variables associated to location 
coordinate_type = plIntegerType(-grid_half_dimension+1,grid_half_dimension)
X=plSymbol("X", coordinate_type)
Y=plSymbol("Y", coordinate_type)

#bearings
bearing_type = plLabelType(["NE","SE","NW","SW"])
B1=plSymbol("B1",bearing_type)
B2=plSymbol("B2",bearing_type)
B3=plSymbol("B3",bearing_type)

#danger
C=plSymbol("C",plIntegerType(0,1))


#defining the probability function for Danger
#Input_[0]= value of C,Input_[1]= value of X .....


def danger_prob_function(Input_) :
    proba_for_danger = \
       min(1.0,30.0/(1+sqrt(pow((Input_[2].to_float()+50),2)+ pow((Input_[1].to_float()+50),2))))
    if Input_[0].to_float() == 1 :
        return  proba_for_danger
    else :
        return 1-proba_for_danger



#defining the probability function for Dn
#Input_[0].to_float()= value of Dn,Input_[1].to_float()= value of X  .....
#generic sensor model 
def generic_bearing_prob_function(offset_X,offset_Y):
    def bearing_prob_function(Input_) :
        NE = 0
        SE = 1
        NW = 2
        halfpi= 0.5 * pi 
        theta = atan2(-1.0*Input_[2].to_float()-offset_Y, -1.0*Input_[1].to_float()- offset_X)
        if 0 < theta and theta < halfpi :
            if Input_[0].to_int() == NE: 
                return 0.5
            elif Input_[0].to_int() == NW:
                return 0.2
            elif Input_[0].to_int() == SE :
                return 0.2
            else:
                return 0.1
        elif halfpi < theta and theta < pi:
            if Input_[0].to_int() == NE: 
                return 0.2
            elif Input_[0].to_int() == NW:
                return 0.5
            elif Input_[0].to_int() == SE :
                return 0.1
            else: 
                return 0.2
        elif theta < 0 and theta > - halfpi:
            if Input_[0].to_int() == NE: 
                return 0.2
            elif Input_[0].to_int() == NW:
                return 0.1
            elif Input_[0].to_int() == SE :
                return 0.5
            else: 
                return 0.2
        else:
            if Input_[0].to_int() == NE: 
                return 0.1
            elif Input_[0].to_int() == NW:
                return 0.2
            elif Input_[0].to_int() == SE :
                return 0.2
            else: 
                return 0.5
    return bearing_prob_function

#looking at individual distributions
pc = plCndAnonymousDistribution \
                                 (C,X^Y,plPythonExternalProbFunction \
                                                     (C^X^Y,danger_prob_function))
print pc.instantiate([-30,-30]).compile()

pd1 = plCndAnonymousDistribution \
                                (B1,X^Y,plPythonExternalProbFunction \
                                 (B1^X^Y,generic_bearing_prob_function(50.0,50.0)))            

print pd1.instantiate([-10,-10]).compile()

pd2 = plCndAnonymousDistribution \
                                (B2,X^Y,plPythonExternalProbFunction \
                                 (B2^X^Y,generic_bearing_prob_function(50.0,0.0)))            

print  pd2.instantiate([-10,-10]).compile()


pd3 = plCndAnonymousDistribution \
                                (B3,X^Y,plPythonExternalProbFunction \
                                 (B3^X^Y,generic_bearing_prob_function(0.0,50.0)))            

print pd3.instantiate([-10,-10]).compile()



#define the desciption 
            

JointDistributionList=plComputableObjectList()
            
#building the specification 
JointDistributionList.push_back(plUniform(X))
JointDistributionList.push_back(plUniform(Y))

            
#distribuitons related to distances
JointDistributionList.push_back(plCndAnonymousDistribution \
                                                (C,X^Y,plPythonExternalProbFunction \
                                                     (C^X^Y,danger_prob_function)))
JointDistributionList.push_back(plCndAnonymousDistribution \
                                (B1,X^Y,plPythonExternalProbFunction \
                                 (B1^X^Y,generic_bearing_prob_function(50.0,50.0))))

JointDistributionList.push_back(plCndAnonymousDistribution \
                                (B2,X^Y,plPythonExternalProbFunction \
                                 (B2^X^Y,generic_bearing_prob_function(50.0,0.0))))

JointDistributionList.push_back(plCndAnonymousDistribution \
                                (B3,X^Y,plPythonExternalProbFunction \
                                 (B3^X^Y,generic_bearing_prob_function(0.0,50.0))))


#define the description
localisation_with_bell_model=plJointDistribution(X^Y^C^B1^B2^B3,JointDistributionList)

question = localisation_with_bell_model.ask(C,B1^B2^B3)

vB = plValues(B1^B2^B3)
#inside the dangerous zone
vB[B1] = 'SW'
vB[B2] = 'NW'
vB[B3] = 'SE'
print "Inside dangerous zone",question.instantiate(vB).compile()

#outside de dangerous zone 
vB[B1] = 'SW'
vB[B2] = 'SW'
vB[B3] = 'NW'
print "outside dangerous zone",question.instantiate(vB).compile()

#in between (1)
vB[B1] = 'SW'
vB[B2] = 'NW'
vB[B3] = 'SW'
print "near L3 ", question.instantiate(vB).compile()

#in between (2)
vB[B1] = 'SW'
vB[B2] = 'SW'
vB[B3] = 'SE'
print "near L2" , question.instantiate(vB).compile()


question_on_XY = localisation_with_bell_model.ask(X^Y,C^B1^B2^B3)
vCB = plValues(C^B1^B2^B3)
vCB[B1] = 'SW'
vCB[B2] = 'NW'
vCB[B3] = 'SE'
vCB[C]=1
PXY=question_on_XY.instantiate(vCB)
#to draw the ditribution as in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures'),'Whereweare-SW-NW-SE')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'Whereweare-SW-NW-SE_soft'), PL_EPS_PLOT)

vCB[B1] = 'SW'
vCB[B2] = 'SW'
vCB[B3] = 'SW'
vCB[C]=0
PXY=question_on_XY.instantiate(vCB)
#to draw the ditribution as in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures'), 'Whereweare-SW-SW-SW')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'Whereweare-SW-SW-SW_soft'), PL_EPS_PLOT)

"if we do not know if we are in danger or not"

"SW SW SW"
PXY = localisation_with_bell_model.ask(X^Y,B1^B2^B3).instantiate(vCB)
#to draw the ditribution as in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures'),'Whereweare')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'Whereweare_soft'), PL_EPS_PLOT)

vCB[B1] = 'SW'
vCB[B2] = 'NW'
vCB[B3] = 'SE'

"SW NW SE"
PXY = localisation_with_bell_model.ask(X^Y,B1^B2^B3).instantiate(vCB)
#to draw the ditribution as in the book 
#PXY.to_eps(X, Y, os.path.join(ExDir, 'chapter7', 'figures'), 'WhereweareD')
PXY.plot(os.path.join(ExDir, 'chapter7', 'figures', 'WhereweareD_soft'), PL_EPS_PLOT)












