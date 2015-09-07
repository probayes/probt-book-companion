from pyplpath import *

from pypl import *

#define the variables type
Booltype = plIntegerType(0,1)

#define the variable for the submodel 
Rain=plVariable('Rain',Booltype)
Sprinkler=plVariable("Sprinkler",Booltype)
GrassWet=plVariable("GrassWet",Booltype)

#define the distribution for the submodel 
PRainParis=plProbTable(Rain,[0.7,0.3]) #prior on raining probability 
PSprinklerkRain=plCndDistribution(Sprinkler,Rain,[0.1,0.9,0.9,0.1])
PGrassWetkRainSprinkler=plCndDistribution(GrassWet,Rain^Sprinkler,[1,0,0,1,0,1,0,1,0,1])
print PRainParis
print PSprinklerkRain
print PGrassWetkRainSprinkler

#decomposition
jointlist=plComputableObjectList()
jointlist.push_back(PRainParis)
jointlist.push_back(PSprinklerkRain)
jointlist.push_back(PGrassWetkRainSprinkler)

submodel=plJointDistribution(Rain^Sprinkler^GrassWet,\
                             jointlist)
print 'Paris', submodel.ask(Rain,GrassWet)\
.instantiate([1]).compile()

#define the new variable of the model
Roof=plVariable('Roof',Booltype)

#define the new decomposition using question to another program 
jointlist=plComputableObjectList()
jointlist.push_back(submodel.ask(GrassWet))
jointlist.push_back(submodel.ask(Rain,GrassWet))
jointlist.push_back(plCndDistribution(Roof,Rain,[1,0,0,1])) 

model=plJointDistribution(Rain^Roof^GrassWet,\
                             jointlist)

#verification
#extended model 
jointlist=plComputableObjectList()
jointlist.push_back(PRainParis)
jointlist.push_back(PSprinklerkRain)
jointlist.push_back(PGrassWetkRainSprinkler)
jointlist.push_back(plCndDistribution(Roof,Rain,[1,0,0,1]))

extendedmodel=plJointDistribution(Rain^Roof^GrassWet^Sprinkler,\
                             jointlist)


print 'with subroutine', model.ask(Rain).compile() 
print 'without subroutine', extendedmodel.ask(Rain).compile() 
print 'with subroutine', model.ask(GrassWet).compile()
print 'without subroutine', extendedmodel.ask(GrassWet)\
.compile()
print 'with subroutine', model.ask(Roof,GrassWet)\
.instantiate([1]).compile()
print 'without subroutine', extendedmodel.ask(Roof,GrassWet)\
.instantiate([1]).compile()

#changing distribution by changing data 
PRainNice=plProbTable(Rain,[0.9,0.1]) 
submodel.replace(Rain,PRainNice)
print 'Nice', submodel.ask(Rain,GrassWet)\
.instantiate([1]).compile()

# redefining the model
jointlist=plComputableObjectList()
jointlist.push_back(submodel.ask(GrassWet^Rain))
jointlist.push_back(plCndDistribution(Roof,Rain,[1,0,0,1])) 

model=plJointDistribution(Rain^Roof^GrassWet,\
                             jointlist)
print 'Nice', model.ask(Roof,GrassWet)\
.instantiate([1]).compile()

#alternative 
model.replace(Rain,PRainParis)
print 'Paris', model.ask(Roof,GrassWet)\
.instantiate([1]).compile()


#selecting subroutines 
#defines a new variable
Location = plVariable("Location", plLabelType(['Paris','Nice']))
locval=plValues(Location)

jointlist=plComputableObjectList()
#push a uniform distribution for the location
jointlist.push_back(plUniform(Location))
#now define the two distributions corresponding to Paris and Nice
PGrasswetkLocation=plDistributionTable(GrassWet,Location)
locval[Location]='Paris'
submodel.replace(Rain,PRainParis) 
PGrasswetkLocation.push(submodel.ask(GrassWet),locval)
locval[Location]='Nice'
submodel.replace(Rain,PRainNice) 
PGrasswetkLocation.push(submodel.ask(GrassWet),locval)
#and push it in the joint distribution list
jointlist.push_back(PGrasswetkLocation)
#idem for the conditional ditribution on Rain
PRainkGrasswetLocation=plDistributionTable(Rain,GrassWet^Location,Location)
locval[Location]='Paris'
submodel.replace(Rain,PRainParis) 
PRainkGrasswetLocation.push(submodel.ask(Rain,GrassWet),locval)
locval[Location]='Nice'
submodel.replace(Rain,PRainNice) 
PRainkGrasswetLocation.push(submodel.ask(Rain,GrassWet),locval)
#and push it in the joint distribution list
jointlist.push_back(PRainkGrasswetLocation)
#dirac model when it has  rain the roof is wet  
jointlist.push_back(plCndDistribution(Roof,Rain,[1,0,0,1])) 

model=plJointDistribution(Rain^Roof^GrassWet^Location,\
                             jointlist)
question = model.ask(Rain,GrassWet^Location)
val = plValues(GrassWet^Location)
val[GrassWet]=1
val[Location]='Paris'
print 'Result for Paris'
print question.instantiate(val).compile()
val[Location]='Nice'
print 'Result for  Nice'
print question.instantiate(val).compile()



