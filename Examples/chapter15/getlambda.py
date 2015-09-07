from pyplpath import *
from pypl import *
import os.path

C = plVariable('C',plIntegerType(0,1))
W = plVariable('W',plRealType(0,100))
#define a ML learner for a binomial law
pC_learner = plLearnHistogram(C)
pW_learner = plCndLearn1dNormal(W,C)
#define intial guess : P(Lambda|pi_0)
pC_init = plBinomial(C,0.70)
pWkC_init = plDistributionTable(W,C)
pWkC_init.push(plNormal(W,20.0,40.0),0)
pWkC_init.push(plNormal(W,70.0,40.0),1)
#define the learner 
learner=plEMLearner(pC_init*pWkC_init,
                    [pC_learner,pW_learner])
#define the data source 
file = os.path.join(ExDir, 'chapter15', 'data', 'weights.csv')
data = plCSVDataDescriptor(file,W)
#perform learning stop with a threshold 
learner.run(data,10e-9)
#get the prameters
print learner.get_distribution(0)
print learner.get_distribution(1)





