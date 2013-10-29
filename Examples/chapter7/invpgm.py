from pyplpath import *
from pypl import *
#import math module
from math import * 
import os.path

#variables

#define the probabilistic variables associated to range and bearing
bearing_type = plIntegerType(0,359)

#bearings
B1=plSymbol("B1",bearing_type)
B0=plSymbol("B0",bearing_type)
H=plSymbol("H",bearing_type)

#define the  proper distribution  

JointDistributionList=plComputableObjectList()

#building the specification 
JointDistributionList.push_back(plUniform(H))

avoiding_pb0  = plCndNormal(B0,H,70.0 )

pb0=plDistributionTable(B0,H)
for i in range(360) :
    IV=[]
    V=avoiding_pb0.instantiate(i).tabulate()
    maxproba = max(V[1])
    for v in V[1] :
        IV.append(1.0 - v/maxproba)
    pb0.push(plProbTable(B0,IV),i)

JointDistributionList.push_back(pb0)

pb1  = plCndNormal(B1,H,40.0 )

JointDistributionList.push_back(pb1)

#define the description
bearing_model=plJointDistribution(H^B1^B0,JointDistributionList)

#question 1
PB0kH = bearing_model.ask(B0,H)
PB0k225=PB0kH.instantiate(225)
#to draw the dirtirubution used in the book 
#PB0K225.plot(os.path.join(ExDir, 'chapter7', 'figures', 'repulsiveB0'), PL_POSTSCRIPT_PLOT)
PB0k225.plot(os.path.join(ExDir, 'chapter7', 'figures', 'repulsiveB0'))

PHkB0B1=bearing_model.ask(H,B1^B0)

sensor_reading_values=plValues(B0^B1)

sensor_reading_values[B0]= 270
sensor_reading_values[B1]= 270
PH=PHkB0B1.instantiate(sensor_reading_values)
best=PH.compile().best()
print best[0]

#creatin g fig file

def radiantodegree(x):
    if x >= 0 :
        return 180 * x / pi
    else :
        return 360 + 180 * x / pi

field = open(os.path.join(ExDir, 'chapter7', 'figures', 'invpgmfield.fig'), 'w')

field.write('#FIG 3.2  Produced by xfig version 3.2.5b \n\
Landscape\n\
Center\n\
Inches\n\
Letter\n\
100.00\n\
Single\n\
-2\n\
1200 2\n')

linecode='2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 0 2\n \
\t1 1 1.00 60.00 30.0\n'

for x in range(-50,50):
    if x % 8 == 0 : 
        for y in range(-50,50):
            if y% 8 == 0 : 
                thetab0= atan2(-y,-x)
                thetab1= atan2(-50.0-y,-50.0-x)
                sensor_reading_values[B0]= floor(radiantodegree(thetab0))
                sensor_reading_values[B1]= floor(radiantodegree(thetab1))
                best=PHkB0B1.instantiate(sensor_reading_values).compile().best()
                field.write(linecode)
                field.write('\t {0} {1} {2} {3}\n'.format( \
                            5000+(100*(x-50))+50,\
                            -5000-(100*(y-50))-50,\
                            5000+(100*(x-50))+ int(floor(250*cos(best[0]*pi/180.0))),\
                            -5000-(100*(y-50))- int(floor(250*sin(best[0]*pi/180.0)))))


field.close()


    







