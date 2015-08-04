from pyplpath import *
import os.path
from pypl import *

O = plSymbol('O',plIntegerType(0,1))
L = plSymbol('L',plRealType(0,1))
file = os.path.join(ExDir, 'chapter15', 'data', 'B_O.csv')
#define the data source ignoring unknown fields
previous_O=plCSVDataDescriptor(file,O)
#define the type of Bayesian learner 
#the prior beta distribution (here uniform : alpha=1 beta=1)
learner_O=plBayesLearnBinomial(O,1,1)
#print the distribution before learning 
distrib = learner_O.get_distribution()
print distrib
#use data
i= learner_O.learn(previous_O)
#retrieve the distribution 
distrib = learner_O.get_distribution()
#print it 
print distrib
#get the posterior distribution 
posterior=learner_O.get_aposteriori_distribution(L)
#write the decomposition
decomposition= posterior*plCndBinomial(O,L)
#define de joint distribution 
joint = plJointDistribution(decomposition) 
#tell the interpreter to use 1000 sampling points to appoximate the integral
qu=joint.ask_mc_nsamples(O,1000)
#tell the interpreter to stop integrating
#when the precision is below 0.001
qu=joint.ask_mc_convergence(O,0.001)
