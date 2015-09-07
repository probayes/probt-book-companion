from pyplpath import *

# import all 
from pypl import *
#import math module
from math import * 
import time

#depth 
d=1
#number of elements -1 
n=1

A=plVariable("A", plIntegerType(0,9))
B=plVariable("B", plIntegerType(0,n))
C=plVariableCollection("C",plIntegerType(0,n),1,4*d+5+1)

JointDistributionList=plComputableObjectList()

Aprobval=[]
for i in range(10):
   Aprobval.append(10.0/(i+1))

PA=plProbTable(A,Aprobval)

fakeprobtable = [0.1,0.9,0.9,0.1,0.1,0.9,0.9,0.1,0.1,0.9,0.9,0.1,0.1,0.9,0.9,0.1,0.1,0.9,0.1,0.9]


#initial line
JointDistributionList.push_back(PA)
for i in range(4):
    JointDistributionList.push_back(plDistributionTable(C[i],A,fakeprobtable))


#generic line
for i in range(d):
    JointDistributionList.push_back(plDistributionTable(C[4*(i+1)],C[i],[0.1,0.9,0.9,0.1]))
    for j in range(1,4):
        JointDistributionList.push_back(plDistributionTable(C[4*(i+1)+j],C[4*i+j-1]^C[4*i+j],fakeprobtable))

#final line
JointDistributionList.push_back(plDistributionTable(C[4*d+4],C[4*d]^C[4*d+1],fakeprobtable))
JointDistributionList.push_back(plDistributionTable(C[4*d+5],C[4*d+2]^C[4*d+3],fakeprobtable))
JointDistributionList.push_back(plDistributionTable(B,C[4*d+4]^C[4*d+5],fakeprobtable))

model = plJointDistribution(A^B^C,JointDistributionList)

question_S=model.ask(B,A,PL_OPTIMIZE_COMPILATION_TIME) 
question_U=model.ask(B,A,PL_OPTIMIZE_UPDATE_TIME) 

#book example 
Va=plValues(A)
Va=0
pBka = question_S.instantiate(Va).compile()

for i in range(10):
        Va=i
        pbka = question_U.instantiate(Va).compile()
#not convincing after all 

start = time.clock()
for j in range (100) :
    for i in range(10):
        Va=i
        pBka = question_S.instantiate(Va).compile()
end = time.clock()
print "time for a single call ", end-start

start = time.clock()
for j in range (100) :
    for i in range(10):
        Va=i
        pbka = question_U.instantiate(Va).compile()
end = time.clock()
print "time with update optimization ", end-start

