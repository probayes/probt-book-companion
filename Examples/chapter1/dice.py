from pyplpath import *

# import all 
from pypl import *

# define a probabilistic variable 
dice= plSymbol("Dice", plIntegerType(1,6))
#define a way to adress the values   
dice_value = plValues(dice)

# define a  uniform probability distribution on the variable 
P_dice = plUniform(dice)

# print it
print 'P_dice = ', P_dice

# perform two random draws with the distribution 
# and print the result
for i in range(2):
  P_dice.draw(dice_value)
  print i+1,'th trow', dice_value
