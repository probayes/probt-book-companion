from pyplpath import *

from pypl import *
import csv
from math import *
import os.path


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

# definition of the variabes 
Dir = plSymbol('Dir',plIntegerType(-10,10))
Prox = plSymbol('Prox',plIntegerType(0,15))
Vrot = plSymbol('Vrot',plIntegerType(-10,10))


#define de distributions 
PDirProx=plUniform(Dir)*plUniform(Prox) 

#use the file for avoidance  : use simulate simulateavoid.py to produce the file
file = os.path.join(ExDir, 'chapter10', 'data', 'avoiding.csv')

PVrot_K_DirProx= learner(file).get_cnd_distribution()

# define the decomposition (equation 4.4)
Decomposition=plComputableObjectList()
Decomposition.push_back(plComputableObject(PDirProx))
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

H=plSymbol("H",plIntegerType(0,1))

PH_init= plDistributionTable(H,Prox,Prox)
random=1

for i in plValues(Prox):
    PH_init.push(plProbTable(H,random),i)


PVrot=plDistributionTable(Vrot,Dir^Prox^Theta^H,H)
PVrot.push(phototaxy_question,1) #phototaxy
PVrot.push(render_question,0) #avoidance

PH_learned = plCndLearnHistogram(H,Prox)

#define the distribution which needed to be learned 
HLearner =plEMLearner(plUniform(Prox) * plUniform(Dir) * plUniform(Theta) * PH_init * PVrot,
                      [plLearnFrozenDistribution(plUniform(Prox)),
                       plLearnFrozenDistribution(plUniform(Dir)),
                       plLearnFrozenDistribution(plUniform(Theta)),
                       PH_learned,
                       plLearnFrozenDistribution(PVrot)])
datahoming = plCSVDataDescriptor(os.path.join(ExDir, 'chapter10', 'data', 'homing.csv'), 
                                 Dir^Prox^Theta^H^Vrot)

#Perform Learning on experimental data
HLearner.run(datahoming,0.01)
#Extract usable model from the leaner
learned_model = HLearner.get_joint_distribution()

#use this question at 0.1 Hz to drive the robot
home_question=learned_model.ask(Vrot,Dir^Prox^Theta)
#use this question to classify the behavior 
behavior_question=learned_model.ask(H,Prox)
