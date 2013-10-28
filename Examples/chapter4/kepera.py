from pyplpath import *

from pypl import *
import csv

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
PDirProx=plUniform(Dir^Prox) 
#print it 
#learn a behavior here from a file with records obtained during following:
file = ExDir+'chapter4/data/following.csv'
#or alternatively learn a behavior here from a file with records obtained during pushing:
#file = ExDir+'chapter4/data/pushing.csv'

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


# use it in a loop to obtain a simila  behavior
# obtain dir prox from sensors
dir = 0
prox = 0
# use render to send the value of Vrot to the controller
print render(dir,prox)






