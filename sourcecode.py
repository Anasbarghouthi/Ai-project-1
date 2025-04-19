import re
import math
import copy
import random
def load_file ():
    """ return a list of items where each item has unique id 0 also, priority 1, weight 2, x coordinate 3, y coordinate 4  """
    a=[]
    line =open('cases.txt', 'r') 
    for p in line :
        templist=p.split('#') #divide each item when it ssee '#'
        templist=[re.sub(r'\s',"",item)for item in templist] #remove spaces
        templist = [int(item) for item in templist]
        a.append(templist)
    return a

def menu (max):
    """ return a list of information which is capacity of vehicles index 0 number of vehicles index 1 algorithm to use index 2  """
    #?loop for pick good capacity for all packages
    while(True):
        capacity =input("Enter the capacity of each car \n")
        capacity = int(capacity)
        if max <= capacity:
            break
        print (" the number that you entered is too small ... \n")

    vehicles =input("Enter the number of available vehicles\n") 
    vehicles =int (vehicles)
    print ("chose the algorithm to use \n")
    algo = input("1.SA\n2.GA\n") #algorithm that will use 
    algo =int (algo)
    result =[capacity,vehicles,algo]
    return result    
#!#############################     GA
def GA (C,NV,package): #?C == capacity , NV == number of vehicles 
    temp_package_list=copy.deepcopy(package)
    print ("in  GA")

 
#!############################       SA
def SA (C,NV,package):  #?C == capacity , NV == number of vehicles 
    temp_package_list=copy.deepcopy(package)
    vehicles_list=[]
    for i in range(NV):
        vehicles_list.append([i+1,C])   
    random_package_in_vehicles(vehicles_list,temp_package_list)
    print(vehicles_list)
    


def random_package_in_vehicles (vehicles_list,package): 
    """this function is use for random package pick but also it is not pure random it make the property of pick higher priority more than another  """
    biased_list=[]
    table ={ 1:5 , 2:4 , 3:3 , 4:2, 5:1 } #for switch statement 
    for i in package:
        biased_list.extend ([i] * table[i[1]] )# for ex. higher priority (1) we add it 5 time 
    
     
    k=0
    while(len(package)!=0):
        picked_package = random.choice(biased_list) #?chose package randomly
        #!package information 
        id=picked_package[0]
        priority =picked_package[1]
        weight = picked_package[2]
        x=picked_package[3]
        y=picked_package[4]
        
        fit = False
        for i in vehicles_list:
            #check if package fit 
            if i[1] > weight:
                i.append([id,priority,weight,x,y])
                i[1] -=weight
                fit=True 
                break     
        if fit:
            i=0
            end =table[priority]
            while end!=0:
                if biased_list[i][0] == id :
                    biased_list.pop(i)
                    end -=1
                else:
                    i +=1
                    
            i=0        
            while len(package)!=0:
                if package[i][0] == id :
                    package.pop(i)
                    break
                i +=1 
        if max_capacity(vehicles_list) < min_package_weight(package):
            break 
                
            
        
def max_capacity (vlist):
    max =0
    for i in vlist :
        if i[1]> max:
            max=i[1]
    return max 
def min_package_weight(plist):
    min=100000
    for i in plist :
        if i[2] < min:
            min=i[2]
    return min
           
                            


                

#*###########################################    main    ##################################################### 

package =load_file () 
max_weight =0
for product in package: #loop to know the max weight 
    if product[2] > max_weight: 
        max_weight = product[2]
     
data = menu(max_weight) # use max number of capacity validation  

if data[2] == 1:
    SA(data[0],data[1],package) #number of vehicles and it capacity 
else:
    GA(data[0],data[1],package)#number of vehicles and it capacity 

    