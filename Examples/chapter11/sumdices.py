from pyplpath import *

from pypl import *
from math import * 
import os.path

def dirac_01_S1(Output_,Input_):
    Output_[S[1]]= Input_[O[1]]

def generic_dirac_si(i) :
    def dirac(Output_, Input_):
        Output_[S[i]]= Input_[O[i]]+Input_[S[i-1]]
    return dirac

def dices_game(O,S) :
    JointDistributionList=plComputableObjectList()
    JointDistributionList.push_back(plUniform(O[1]))
    JointDistributionList.push_back(plFunctionalDirac(S[1],O[1],plPythonExternalFunction(S[1],O[1],dirac_01_S1)))
    for i in range(2,len(S)):
        JointDistributionList.push_back(plUniform(O[i]))
        JointDistributionList.push_back(plFunctionalDirac(S[i],S[i-1]^O[i],plPythonExternalFunction(S[i],S[i-1]^O[i],generic_dirac_si(i))))
    return plJointDistribution(JointDistributionList)



#example 

N=3
O=plArray("O",plIntegerType(1,6),1,N+1)
S=[]
S.append("null")
for i in range(1,N+1):
    S.append(plSymbol("S"+str(i),plIntegerType(i,i*6))) 

D3=dices_game(O,S)
PS3kO1=D3.ask(S[3],O[1])
PS3=PS3kO1.instantiate(4).compile()
#to draw the distribution used in the book 
#PS3.plot(os.path.join(ExDir, 'chapter11', 'figures', 'PS3kO1'))
PO3kS3=D3.ask(O[3],S[3])
PO3=PO3kS3.instantiate(14).compile()
#PO3.plot(os.path.join(ExDir, 'chapter11', 'figures', 'PO3kS3'))




