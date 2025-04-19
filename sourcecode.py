import re
def load_file ():
    """ return a list of items where each item has unique id 0 also, priority 1, weight 2, x coordinate 3, y coordinate 4  """
    a=[]
    line =open('cases.txt', 'r') 
    for p in line :
        templist=p.split('#')
        templist=[re.sub(r'\s',"",item)for item in templist]
        a.append(templist)
    return a

def menu ():
    """ return a list of information which is capacity of vehicles index 0 number of vehicles index 1 algorithm to use index 2  """
    capacity =input("Enter the capacity of each car \n")
    capacity = int(capacity)
    vehicles =input ("Enter the number of available vehicles\n") 
    vehicles =int (vehicles)
    print ("chose the algorithm to use \n")
    algo = input("1.SA\n2.GA\n") #algorithm that will use 
    algo =int (algo)
    result =[capacity,vehicles,algo]
    return result    

def GA ():
    print ("in  GA")



def SA ():
    print ("in SA")




#*###########################################    main    ##################################################### 

package =load_file () 
data = menu()

if data[2] == 1:
    SA()
else:
    GA()    