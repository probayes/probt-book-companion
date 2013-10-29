from pyplpath import *
from pypl import *
import math
import os.path

def ReadVector(filename) :
    f = open(filename,"r")
    V = f.readline().strip().split(" ")
    fV = []
    for v in V :
        fV.append(float(v))
    f.close()
    return fV

#read the file created by calibration.py
ProbaFromCalib = ReadVector(os.path.join(ExDir, 'chapter6', 'data', 'calibration.txt'))

#generic sensor model 
def WGenericsensorModel(S,I,F):
    def special_sensor_model(O_,I_):
        O_[S]= math.floor((I_[I]+I_[F])/2)
    return special_sensor_model

#define the type and the variables 

Wtype = plIntegerType(0,10)
I0=plSymbol('I0',Wtype)
I1=plSymbol('I1',Wtype)
I3=plSymbol('I3',Wtype)
F=plArray('F',Wtype,1,4)
S=plArray('S',Wtype,1,4)
C=plArray('C',Wtype,1,4)
O=plArray('O',Wtype,1,4)


JointDistributionList=plComputableObjectList()
JointDistributionList.push_back(plUniform(I0))
JointDistributionList.push_back(plUniform(I1))
JointDistributionList.push_back(plUniform(I3))
for i in range(4) :
    JointDistributionList.push_back(plUniform(F[i]))
    JointDistributionList.push_back(plUniform(C[i]))

#Conditional distribution on S[0]
extsensormodel=plPythonExternalFunction(S[0], \
                                        I0^F[0], \
                                        WGenericsensorModel(S[0],I0,F[0]))
JointDistributionList.push_back(plFunctionalDirac(S[0],I0^F[0],extsensormodel))

#Conditional distribution on S[1]
extsensormodel=plPythonExternalFunction(S[1], \
                                        I0^F[1], \
                                        WGenericsensorModel(S[1],I0,F[1]))
JointDistributionList.push_back(plFunctionalDirac(S[1],I0^F[1],extsensormodel))


#Conditional distribution on O[0] from "calibraiton" 
# file correspond to 11pow4 distriubtion
cnddist=plCndDistribution(O[0],I0^I1^S[0]^C[0],ProbaFromCalib)
JointDistributionList.push_back(cnddist)

#Conditional distribution on S[2]
extsensormodel=plPythonExternalFunction(S[2], \
                                        O[0]^F[2], \
                                        WGenericsensorModel(S[2],O[0],F[2]))
JointDistributionList.push_back(plFunctionalDirac(S[2],O[0]^F[2],extsensormodel))

#Conditional distribution on S[3]
extsensormodel=plPythonExternalFunction(S[3], \
                                        I3^F[3], \
                                        WGenericsensorModel(S[3],I3,F[3]))
JointDistributionList.push_back(plFunctionalDirac(S[3],I3^F[3],extsensormodel))


#Conditional distribution on O[1] from "calibration" 
cnddist=plCndDistribution(O[1],I0^I1^S[1]^C[1],ProbaFromCalib)
JointDistributionList.push_back(cnddist)

#Conditional distribution on O[2] from "calibration" 
cnddist=plCndDistribution(O[2],O[0]^O[1]^S[2]^C[2],ProbaFromCalib)
JointDistributionList.push_back(cnddist)

#Conditional distribution on O[3] from "calibration" 
cnddist=plCndDistribution(O[3],I3^O[2]^S[3]^C[3],ProbaFromCalib)
JointDistributionList.push_back(cnddist)

model=plJointDistribution(I0^I1^I3^F^S^C^O, JointDistributionList)
#printing the model p
print model

#define the question for the forward model 
question=model.ask(O[3],I0^I1^I3^S^C)
print question

resultA = question.instantiate([2,8,10,5,5,7,9,0,0,0,0])
#resultA.plot(os.path.join(ExDir, 'chapter6', 'figures', 'DirectO3WithCEqualZero'))
resultB = question.instantiate([2,8,10,5,5,7,9,5,5,5,5])
#resultB.plot(os.path.join(ExDir, 'chapter6', 'figures', 'DirectO3WithCEqualFive'))
resultC = question.instantiate([2,8,10,5,5,7,9,10,10,10,10])
#resultC.plot(os.path.join(ExDir, 'chapter6', 'figures', 'DirectO3WithCEqualTen'))

#define the question to get the best control 
question1=model.ask(C,I0^I1^I3^S^O[3])
resultD=question1.instantiate([2,8,10,5,5,7,9,9])
# using a genetic algorithm
val_opt = resultD.best()
#using the exact solution (faster is this case) 
compiled_resultD= resultD.compile()
compiled_val_opt =  compiled_resultD.best()
print 'compile_val_opt=', compiled_val_opt
print compiled_resultD.compute(compiled_val_opt)
print compiled_resultD.compute(val_opt)
print compiled_resultD.compute([6,6,4,9])


#using control = 6,6,4,9 
resultE = question.instantiate([2,8,10,5,5,7,9,6,6,4,9])
print resultE.compile()
#resultE.plot(os.path.join(ExDir, 'chapter6', 'figures', 'DirectO3WithCEqualOptimum'))

#introducing a constraint
H=plSymbol('H',plIntegerType(0,1))
VALMIN = plSymbol('VALMIN',plIntegerType(0,9))


#introducing a constraint
def constraint(O_,I_):
        if I_[O[3]].to_float() >= I_[VALMIN].to_float() :
            O_[H]=1
        else :
            O_[H]=0


NewJointDistributionList=JointDistributionList
NewJointDistributionList.push_back(plUniform(VALMIN))
constraintmodel =plPythonExternalFunction(H, \
                                        VALMIN^O[3], \

                                        constraint)
NewJointDistributionList.push_back(plFunctionalDirac(H,VALMIN^O[3],constraintmodel))

#define a new model
newmodel=plJointDistribution(I0^I1^I3^F^S^C^O^H^VALMIN, NewJointDistributionList)
print newmodel

#define the new question to get the best control 
newquestion1=newmodel.ask(C,I0^I1^I3^S^H^VALMIN)
#satisfy constraint H = 1 and VALMIN = 5
newresultD=newquestion1.instantiate([2,8,10,5,5,7,9,1,5])
compiled_newresultD= newresultD.compile()
new_opt_val = compiled_newresultD.best()
known_val = plValues(I0^I1^I3^S)
known_val[I0]=2
known_val[I1]=8
known_val[I3]=10
known_val[S[0]]=5
known_val[S[1]]=5
known_val[S[2]]=7
known_val[S[3]]=9

#water quality greater the 5
opt_known_val = known_val^new_opt_val
print '5: ',new_opt_val
newresultA = question.instantiate(opt_known_val)
#newresultA.plot(os.path.join(ExDir, 'chapter6', 'figures', 'NewDirectO3WithCEqualOptfor5'))

#water quality greater than 7
newresultD=newquestion1.instantiate([2,8,10,5,5,7,9,1,7])
compiled_newresultD= newresultD.compile()
new_opt_val = compiled_newresultD.best()
print '7: ', new_opt_val
opt_known_val = known_val^new_opt_val
newresultA = question.instantiate(opt_known_val)
#newresultA.plot(os.path.join(ExDir, 'chapter6', 'figures', 'NewDirectO3WithCEqualOptfor7'))

#water quality greater than 8
newresultD=newquestion1.instantiate([2,8,10,5,5,7,9,1,8])
compiled_newresultD= newresultD.compile()
new_opt_val = compiled_newresultD.best()
print '8: ',new_opt_val
opt_known_val = known_val^new_opt_val
newresultA = question.instantiate(opt_known_val)
#newresultA.plot(os.path.join(ExDir, 'chapter6', 'figures', 'NewDirectO3WithCEqualOptfor8'))


#Diagnosis
#question 
diagnosisquestion = model.ask(F,I0^I1^I3^S^C^O[3])
# for a given value of the Known variables
resultdiagnosis = diagnosisquestion.instantiate([2,8,10,5,5,4,9,5,5,5,5,7])
#allow faster access
compiled_resultdiagnosis = resultdiagnosis.compile()
vF = plValues(F)
indexed_proba_table = []
#One way to store the result in a list (probal, value1, value2....)
for v in vF :
    indexed_proba_table.append([compiled_resultdiagnosis.compute(v)] \
                                    + [vF[F[x]] for x in range(4)])
#Using Python to sort this list
sorted_indexed_prob_table = sorted(indexed_proba_table, \
                                       key=lambda el : el[0], reverse = True)


for i in range(10) :
    print sorted_indexed_prob_table[i][0],sorted_indexed_prob_table[i][1],sorted_indexed_prob_table[i][2],sorted_indexed_prob_table[i][3],sorted_indexed_prob_table[i][4]

#computing the quantile 
quantile = 0.0
i=0
while quantile < 0.95:
    quantile = quantile+ sorted_indexed_prob_table[i][0]
    i=i+1
    print sorted_indexed_prob_table[i][0],sorted_indexed_prob_table[i][1],sorted_indexed_prob_table[i][2],sorted_indexed_prob_table[i][3],sorted_indexed_prob_table[i][4]

#computing distribution on F2
#to produce figure 
F2question = model.ask(F[2],I0^I1^I3^S^C^O[3])
diagnosis_F2 = F2question.instantiate([2,8,10,5,5,4,9,5,5,5,5,7])
#diagnosis_F2.plot(os.path.join(ExDir, 'chapter6', 'figures', 'diagnosis_F2'))
