from pyplpath import *

from pypl import *
import csv
from math import *


###### avoidance code based on learning #######

def learner(filename):
    """
    Defines the probability P(Vrot | Dir^Prox) using learning
    The records obtained during learning 
    are stored a file (filename). In a real example they could directly
    be obtained on the fly from sensor readings.
    It is also possible to interrupt learning and use the 
    distribution at any time. Resuming learning is also possible
    to obtain a new distribution
    """
    VrotDirProxLearner = plCndLearn1dNormal(Vrot,Dir^Prox)
    sample=plValues(Vrot^Dir^Prox)
    VrotDirProxReader = csv.reader(open(file,'rb'),delimiter=';')
    for row in VrotDirProxReader:
        sample[Vrot] = int(row[0])
        sample[Dir] = int(row[1])
        sample[Prox]= int(row[2])
        # learn with this new point
        VrotDirProxLearner.add_point(sample)
    return VrotDirProxLearner

#define the render function 
def render(dir,prox):
    """
    from the value of dir and prox 
    computes the probability distribution P(Vrot | Dir Prox)
    and draw the value of rot from this distribution. This value 
    mau be used to direct the robot 
    """
    
    VrotValue = plValues(Vrot)
    render_question.instantiate([dir,prox]).draw(VrotValue)
    # this is the value sent to the robot controller
    return VrotValue[Vrot]


# definition of the variabes (4.3)
Dir = plSymbol('Dir',plIntegerType(-10,10))
Prox = plSymbol('Prox',plIntegerType(0,15))
Vrot = plSymbol('Vrot',plIntegerType(-10,10))

#define de distributions (4.5)
PDirProx=plComputableObject(plUniform(Dir)*plUniform(Prox))

#use the file for avoidance  : use simulate simulateavoid.py to produce the file
file = ExDir+'chapter10/data/avoiding.csv'

PVrot_K_DirProx= learner(file).get_cnd_distribution()

# define the decomposition (equation 4.4)
Decomposition=plComputableObjectList()
Decomposition.push_back(PDirProx)
Decomposition.push_back(PVrot_K_DirProx)

# define the bayesian program
# define the description 
render_description=plJointDistribution(Vrot^Dir^Prox,Decomposition)
# define the associated question 
render_question=render_description.ask(Vrot,Dir^Prox)

##### define the avoidance code 
Theta = plSymbol('Theta',plIntegerType(-10,10))
PTheta=plUniform(Theta) 
Decomposition=plComputableObjectList()
Decomposition.push_back(PTheta)
Decomposition.push_back(plCndNormal(Vrot,Theta,2))
phototaxy_description=plJointDistribution(Decomposition)
phototaxy_question=phototaxy_description.ask(Vrot,Theta)
#### Combine the behaviors ######

#the proximity is measured by infrared sensors a proximity of 0 means :
#far away and 15 means close from obstacles. 


def generic_H_prob_function(alpha,beta):
    def H_prob_function(Input_) :
        v = 1.0/(1.0+exp(beta*(alpha-Input_[1].to_float())))
        if Input_[0].to_int() == 0 : #H=0 means Avoidance  
            return v
        else:
            return 1-v
    return H_prob_function

H=plSymbol("H",plIntegerType(0,1))
PH = plCndAnonymousDistribution(\
      H,Prox,plPythonExternalProbFunction( \
      H^Prox,generic_H_prob_function(9,0.25 )))
#H is used a key to select the proper behavior
PVrot=plDistributionTable(Vrot,Dir^Prox^Theta^H,H)
PVrot.push(phototaxy_question,1) #phototaxy
PVrot.push(render_question,0) #avoidance
#define the decomposition 
JointDistributionList=plComputableObjectList()
JointDistributionList.push_back(plUniform(Prox))
JointDistributionList.push_back(plUniform(Theta))
JointDistributionList.push_back(plUniform(Dir))
JointDistributionList.push_back(PH)
JointDistributionList.push_back(PVrot)

#define the dspecification and the question 
home_specification=plJointDistribution(JointDistributionList)
home_question=home_specification.ask(Vrot,Dir^Prox^Theta)

#define a new question on H  
behavior_question=home_specification.ask(H,Vrot^Dir^Prox^Theta)


#simulate homing
simulation_homing_file=open(ExDir+'chapter10/data/homing.csv','w')
allval = plValues(Dir^Prox^Theta^H^Vrot)

simulation_homing_file.write('Dir;Prox;Theta;H;Vrot\n')

for i in range(100):
    allval = home_specification.draw()
    simulation_homing_file.write('{0};{1};{2};{3};{4}\n'.format(\
            allval[Dir],allval[Prox],allval[Theta],allval[H],allval[Vrot]))
simulation_homing_file.close()








    
