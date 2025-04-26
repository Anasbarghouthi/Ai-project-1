import re
import math
import copy
import random
def load_file ():
    """ return a list of items where each item has unique id 0 also, priority 1, weight 2, x coordinate 3, y coordinate 4  """
    a=[]
    file =open('cases.txt', 'r') 
    for line in file :
        templist=line.split('#') #divide each item when it ssee '#'
        templist=[re.sub(r'\s',"",item)for item in templist] #remove spaces
        templist = [int(item) for item in templist]
        a.append(templist)
    return a

def menu ():
    """ return a list of information which
    is capacity of vehicles index 0 number of 
    vehicles index 1 
    algorithm to use index 2  """
    #?loop for pick good capacity for all packages
    while(True):
        capacity =input("Enter the capacity of each car \n")
        capacity = int(capacity)
        if max_weight <= capacity:
            break
        print (" the number that you entered is too small ... \n")

    vehicles =input("Enter the number of available vehicles\n") 
    vehicles =int (vehicles)
    print ("choose the algorithm to use \n")
    
    while True: 
        algo = input("1.SA\n2.GA\n") #algorithm that will use
        algo =int (algo)
        if (algo == 1 or algo == 2) :
             break  
        else :
            print ("Wrong input , Try again !!")
           
        
    result =[capacity,vehicles,algo]
    return result    
#!#############################     GA
def GA (C,NV,package): #?C == capacity , NV == number of vehicles 
    temp_package_list=copy.deepcopy(package)
    print ("in  GA")

 
#!############################       SA
def SA (C,NV,package):  #?C == capacity , NV == number of vehicles
    T=1000
    #temp_package_list=copy.deepcopy(package)
    old_priority_cost=0
    old_path_cost=10000000000
    best_path=[404]
    vehicles_list=[]
    for i in range(NV): # NV number of vehicles 
        vehicles_list.append([i+1,C])  # [ id , capacity ]     
    #!#11111111
    path_total_cost=0
    priority_total_cost=0
    path_list=[]
    while T > 1 :
       
        for j in range(100): #from project des.
            temp_package_list=copy.deepcopy(package)
            
            k=1 
            while temp_package_list :  ### test ### 
                
                random_package_in_vehicles(vehicles_list,temp_package_list) # after this function vehicles list == [ id , capacity , package1,... ]
                temp1_vehicles_list=copy.deepcopy(vehicles_list)
                temp2_vehicles_list=copy.deepcopy(vehicles_list)
                        
                path_total_cost+=path_cost(vehicles_list)
                priority_total_cost+=priority_cost(temp1_vehicles_list)
                path_list_f(path_list,temp2_vehicles_list,k)
                k +=1
            if path_total_cost < old_path_cost and priority_total_cost > old_priority_cost:
                del best_path
                best_path=copy.deepcopy(path_list)
                old_path_cost = path_total_cost
                old_priority_cost = priority_total_cost
            else:
                E1 = path_total_cost - old_path_cost
                E2 = priority_total_cost - old_priority_cost
                if random.random() < math.exp(-E1/T) or random.random() < math.exp(-E2/T):
                    del best_path
                    best_path=copy.deepcopy(path_list)
                    old_path_cost = path_total_cost
                    old_priority_cost = priority_total_cost
            del temp_package_list
            del path_list
            path_list=[]        

        T *=0.99999
    print (best_path)    

        

        #? determine is it better than last solution or not 
    
    

    


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
            if i[1] >= weight: 
                i.append([id,priority,weight,x,y])
                i[1] -=weight
                fit=True 
                break     
        if fit: # so delete it 
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
             
        if max_capacity(vehicles_list) < min_package_weight(package): # all vehicles can't carry any remaining package   
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
           
def path_cost (vehicles_list):
    total_cost=0
    x_old=0
    y_old=0
    for i in range(len(vehicles_list)):
        x_old=0
        y_old=0
        while len(vehicles_list[i]) > 2 :
            x_new=vehicles_list[i][2][3]
            y_new=vehicles_list[i][2][4]
            weight=vehicles_list[i][2][2]
            vehicles_list[i][1] +=weight
            dx=x_old-x_new  
            dy=y_old-y_new
            dx = dx**2   #dx^2
            dy = dy**2   #dy^2   
            sq=math.sqrt(dx+dy)
            x_old = x_new
            y_old = y_new
            total_cost +=sq 
            #delete package
            vehicles_list[i].pop(2) #delete package         
    return total_cost        

def priority_cost (vehicles_list):
    total_cost=0
    table ={ 1:5 , 2:4 , 3:3 , 4:2, 5:1 }
    for i in range(len(vehicles_list)):
        while len(vehicles_list[i]) > 2 :
            priority=vehicles_list[i][2][1]
            total_cost +=table[priority] 
            #delete package
            vehicles_list[i].pop(2) #delete package         
    return total_cost



#? to determine the path 
def path_list_f (path_list,vehicles_list,k):
    for i in range(len(vehicles_list)):
        while len(vehicles_list[i]) > 2 :
            v_id=vehicles_list[i][0]
            p_id=vehicles_list[i][2][0]
            path_list.append([v_id,p_id,k])
            vehicles_list[i].pop(2) #delete package

       
        
          








                

############################################    main    ##################################################### 

package =load_file () 
max_weight =0
for product in package: #loop to know the max weight 
    if product[2] > max_weight: 
        max_weight = product[2]
     
data = menu() # use max number of capacity validation

if data[2] == 1:
    SA(data[0],data[1],package) #number of vehicles and it capacity 
else:
    GA(data[0],data[1],package)#number of vehicles and it capacity 

    