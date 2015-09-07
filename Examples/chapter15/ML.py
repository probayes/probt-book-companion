from pyplpath import *
from pypl import *
import os.path

O = plVariable('O',plRealType(-100,100))
O_I=plVariable('O_I',plIntegerType(0,2))
file = os.path.join(ExDir, 'chapter15', 'data', 'previous_O.csv')
#define the data source ignoring unknown fields
previous_O=plCSVDataDescriptor(file,O^O_I)
previous_O.ignore_unknown_variables()
#define the type of ML learner 
learner_O=plLearn1dNormal(O)
#use data
i= learner_O.learn(previous_O)
#retrieve the distribution 
distrib = learner_O.get_distribution()
#print it 
print distrib
#learning another distribution from the same source
previous_O.rewind()
learner_O_I=plLearnHistogram(O_I)
i= learner_O_I.learn(previous_O)
distrib_I = learner_O_I.get_distribution()
print distrib_I
#same as above but brows the data only once
previous_O.rewind()
learner_O_I.reset()
learner_O.reset()
#define a vector of distributions to learn 
global_learner = plLearnDistributions([learner_O_I,learner_O],O_I^O)
i=global_learner.learn(previous_O)
list_distrib=global_learner.get_computable_object_list()
print 'global learning \n',list_distrib[0],'\n',list_distrib[1]
#continue learning 
file1 =  os.path.join(ExDir, 'chapter15', 'data', 'previous_O1.csv')

previous_O1=plCSVDataDescriptor(file1,O)
previous_O1.ignore_unknown_variables()
learner_O.reset()
i= learner_O.learn(previous_O)
i= learner_O.learn(previous_O1)
distrib = learner_O.get_distribution()
#print it 
print distrib



