from pyplpath import *
from pypl import *
import os.path

file = os.path.join(ExDir, 'chapter15', 'data', 'weights.csv')
C = plSymbol('C',plIntegerType(0,1))
W = plSymbol('W',plRealType(0,100))
#define a binomial law P(C=1) = 0.55
pC=plBinomial(C,0.55)
#define a conditonnal probability table 
pWkC=plDistributionTable(W,C)
#define the weight distribution for female 
pWkC.push(plNormal(W,45.0,10.0),0)
#define the weight distribution for male
pWkC.push(plNormal(W,55.0,15.0),1)
#define the joint distribution
model = plJointDistribution(pC*pWkC)
#define the question
pW=model.ask(W)
#draw a store result in a file 
vW = plValues(W)
dataset=open(file,'w')
dataset.write('W\n')
for i in range(1000):
    pW.draw(vW)
    dataset.write('{0}\n'.format(vW[W]))
dataset.close()


