import os.path
from pyplpath import *

# import the pypl module
# import all 
from pypl import *

def build_spam_question (nf, nfi, nt , nti):
    """
    nf : number of valid emails
    nfi (vector of integer) : number of time words i of the dictionary 
    appears in valid emails
    nt : number of spams
    nt  (vector of integer) : number of time words i of the dictionary 
    appears in spams
    returns a "Question" which will be used to evaluate 
    the probability for a mail to be a spam 
    site effect : prints the value necessary to build table 2.2 and 2.3
    """
#define the number of word
    N=len(nfi)
#define a binary type
    binary_type = plIntegerType(0,1)
#define a binary variable
    Spam = plSymbol("Spam",binary_type)
#define N binary variable with
    W = plArray("W",binary_type,1,N)
#define a prior distribution probability on Spam 
    P_Spam = plProbTable(Spam,[nf,nt])
    print 'P_spam',P_Spam
#start defining all the  distribution  
    JointDistributionList = plComputableObjectList() 
    JointDistributionList.push_back(P_Spam)
#define the Probabability of Wi Knowing Spam
    for i in range(N):
    #define a conditional distribution of each word i 
        P_Wi_K_Spam = plDistributionTable(W[i],Spam)
    #define the two distributions on Wi : 
    #one for Spam = 0 
        P_Wi_K_Spam.push(plProbTable(W[i],[ 1-((float(nfi[i])+1)/(2+nf)),(float(nfi[i])+1)/(2+nf)]) ,0)
    #the other for Spam = 1 
        P_Wi_K_Spam.push(plProbTable(W[i],[ 1-((float(nti[i])+1)/(2+nt)),(float(nti[i])+1)/(2+nt)]) ,1)
        #write the information necessary to table 2.2
        print P_Wi_K_Spam
    # and store it in a  distribution list  
        JointDistributionList.push_back(P_Wi_K_Spam)
#define the model
    model = plJointDistribution(Spam^W, JointDistributionList)
    model.draw_graph(os.path.join(ExDir, "chapter2", "data", "spam_graph"))
#define the question
    quest = model.ask(Spam,W)
    v = plValues(W)
#use all the possible values to build table 2.3     
    for i in v:
        print i 
        print quest.instantiate(i).compile()
    return quest

def use_spam_question(question,w):
    """ given a quesiton (question) and a vector telling if word i appears or not 
    in the email (w) : computes and prints the probability of being a spam 
    """
    print w, question.instantiate(w).compile()

#tests 
#number of emails considered as non spam  : 
nf = 250
#number of emails considered as spam : nt 
nt = 750
#number of time words i appears in non spam messages 
nfi = [0, 125, 250, 0, 125 ]
#number of time words i appears in spam messages 
nti = [375 ,0 ,0 ,750 , 375]

# build the question and print informations about the model
my_question = build_spam_question (nf, nfi, nt ,nti)
#what is the probability distribution for a mail containing 
#"next" "programming" and "you"
use_spam_question(my_question,[0,1,1,0,1])

