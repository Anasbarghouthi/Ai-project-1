import re
import math
import copy
import random
import matplotlib.pyplot as plt


def plot_path(vehicles_list, path_type="GA"):
    """
    Plot the path of vehicles (either GA or SA).
    
    vehicles_list: List of vehicles with their loaded packages (as [vehicle_id, capacity, package_info...])
    path_type: The algorithm used ("GA" or "SA")
    """
    plt.figure(figsize=(10, 8))
    
    for vehicle in vehicles_list:
        # Extract the x, y coordinates for the vehicle's path
        x_coords = [0]  # Starting point (e.g., the depot)
        y_coords = [0]
        
        for package in vehicle[2:]:
            x_coords.append(package[3])  # x coordinate of the package
            y_coords.append(package[4])  # y coordinate of the package
            
        # Close the loop by adding the depot (0,0) again at the end
        x_coords.append(0)
        y_coords.append(0)
        
        # Plot the path of the vehicle
        plt.plot(x_coords, y_coords, marker='o', label=f'Vehicle {vehicle[0]}')
    
    plt.title(f'Vehicle Routes ({path_type} Solution)', fontsize=16)
    plt.xlabel('X Coordinate', fontsize=12)
    plt.ylabel('Y Coordinate', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()


    
def load_packages ():
    """ return a list of items where each item has unique id 0 also, priority 1, weight 2, x coordinate 3, y coordinate 4  """
    a=[]
    file =open('cases.txt', 'r') 
    for line in file :
        templist=line.split('#') #divide each item when it ssee '#'
        templist=[re.sub(r'\s',"",item)for item in templist] #remove spaces
        templist = [int(item) for item in templist]
        a.append(templist)
    return a

def load_vehicles ():
    """ return a list of items where each item has unique id 0 also, priority 1, weight 2, x coordinate 3, y coordinate 4  """
    a=[]
    file =open('vehicles.txt', 'r') 
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
    
    while True:
        print ("1. Simulating Aneling ") 
        print ("2. Genetic  Algorithm ")
        print ("3. Exit ")
        algo = input("Enter on of options : ") #algorithm that will use
        algo =int (algo)
        if (algo == 1 or algo == 2 or algo == 3) :
             break  
        else :
            print ("Wrong input , Try again !!")
           
    return algo    
#!#############################     GA
def GA (package,vehicles_list): #?C == capacity , NV == number of vehicles 
    temp_package_list=copy.deepcopy(package)
    population_size=100
    generations=500
    

    best_solution =[]
    best_priority=-100
    best_path_cost=1000000
    population=[]
    # initial population 
    for i in range(population_size):
        
        temp_package_list=copy.deepcopy(package)
        temp_vehicles=copy.deepcopy(vehicles_list)
        random_package_in_vehicles(temp_vehicles,temp_package_list,)
        population.append(temp_vehicles)
    
    for i in range(generations):
        
        
        fitness_list=[]    
        for individual in population:
            temp1=copy.deepcopy(individual)
            temp2=copy.deepcopy(individual)
            fitness= priority_cost(temp1)*1000 - path_cost(temp2) # higher is better
            fitness_list.append(fitness)
        
        selected=selection(population,fitness_list,population_size//2)
        
        children=[]
        while len(children) < population_size:
            parent1=random.choice(selected)
            parent2=random.choice(selected)
            c=crossover(parent1,parent2,vehicles_list)
            children.append(c)
        i=0
        for child in children:
            if i%100 == 0:
                i=0
                mutation_function(child) 
        
        population=children

        for i in population:
            temp1=copy.deepcopy(i)
            temp2=copy.deepcopy(i)
            pri_cost=priority_cost(temp1)
            path1_cost=path_cost(temp2)
            if (pri_cost > best_priority and path1_cost < best_path_cost) or (pri_cost == best_priority and path1_cost < best_path_cost) or (pri_cost > best_priority and path1_cost == best_path_cost) :
                best_path_cost=path1_cost
                best_priority=pri_cost
                best_solution=copy.deepcopy(i)



    print("best solution that Genetic solved :",best_solution)
    print("path cost = ",best_path_cost)
    print("priority cost =",best_priority)
    plot_path(best_solution, path_type="GA")
            
              










def selection(population,fitness_list,population_size):
    selected=[]
    
    for i in range(population_size):
        
        t=random.sample(list(zip(population,fitness_list)),5)
        m=0
        index=0
        #? find max fitness value  
        for j in range(len(t)):
            if t[j][1]>m:
                m=t[j][1]
                index=j
        selected.append(copy.deepcopy(t[index][0]))
    return selected            

def crossover (parent1,parent2,vehicles_list):
    child=copy.deepcopy(vehicles_list)

    all_packages1=[]
    all_packages2=[]
    for v in parent1:
        all_packages1.extend(v[2:])
    for v in parent2:
        all_packages2.extend(v[2:])


    unique_package=[]
    
    
    i=0
    while(len(all_packages1)>i):
        if all_packages1[i] not in unique_package:
            unique_package.append(all_packages1[i])
            i+=1
        if len(all_packages2)>i and all_packages2[i] not in unique_package:
            unique_package.append(all_packages2[i])
            i+=1
        else:
            break    

    random_package_in_vehicles_GA(child,unique_package)
    return child                 

def mutation_function(child):
        v1=random.choice(child)
        v2=random.choice(child)
        if v1[0] != v2[0] and len(v2) > 2 and len(v1) > 2:
             idx1 = random.randint(2, len(v1)-1)
             idx2 = random.randint(2, len(v2)-1)
             v1[idx1], v2[idx2] = v2[idx2], v1[idx1]


def random_package_in_vehicles_GA(vehicles_list,package): 
    """this function is use for random package pick but also it is not pure random it make the property of pick higher priority more than another  """
    temp_vehi=copy.deepcopy(vehicles_list)
   
    
     
    
    while(len(package)!=0):
        
        picked_package = package[0]
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
            while len(package)!=0:
                if package[i][0] == id :
                    package.pop(i)
                    break
                i +=1 

             
        if max_capacity(vehicles_list) < min_package_weight(package): # all vehicles can't carry any remaining package   
            random_package_in_vehicles_GA (temp_vehi,package)
            vehicles_list.extend(temp_vehi)
            break
        


    

 
#!############################       SA
def SA (package,vehicles_list):  #?C == capacity , NV == number of vehicles
    T=1000
    #temp_package_list=copy.deepcopy(package)
    old_priority_cost=0
    old_path_cost=10000000000
    best_path=[]   
    path_total_cost=0
    priority_total_cost=0
    while T > 1 :
        for j in range(100): #from project des.
            temp_package_list=copy.deepcopy(package)
            temp_vehicles_list=copy.deepcopy(vehicles_list)
            #k=1 
            #while temp_package_list :  ### test ### 
                
            random_package_in_vehicles(temp_vehicles_list,temp_package_list) # after this function vehicles list == [ id , capacity , package1,... ]
            temp1_vehicles_list=copy.deepcopy(temp_vehicles_list)
            temp2_vehicles_list=copy.deepcopy(temp_vehicles_list)  
            path_total_cost+=path_cost(temp2_vehicles_list)
            priority_total_cost+=priority_cost(temp1_vehicles_list)
            
            #k +=1
            E1 = path_total_cost - old_path_cost  
            E2 = old_priority_cost - priority_total_cost
            if (E1 < 0 and E2 < 0) or (E1 == 0 and E2 < 0) or (E1 < 0 and E2 == 0):
                del best_path
                best_path=copy.deepcopy(temp_vehicles_list)
                old_path_cost = path_total_cost
                old_priority_cost = priority_total_cost
            else:
                probability = math.exp(-(E1 + E2) / T) 
                if random.random() < probability:
                    best_path=copy.deepcopy(temp_vehicles_list)
                    old_path_cost = path_total_cost
                    old_priority_cost = priority_total_cost
            del temp_package_list
            del temp_vehicles_list
            path_total_cost=0
            priority_total_cost=0        

        T *=0.9
    print ("best solution that Simulating Aneling solved :",best_path)
    print ("path cost =",old_path_cost)
    print ("priority cost =",old_priority_cost)
    plot_path(best_path, path_type="SA")
        

        

        #? determine is it better than last solution or not 
    
    

    


def random_package_in_vehicles (vehicles_list,package): 
    """this function is use for random package pick but also it is not pure random it make the property of pick higher priority more than another  """
    biased_list=[]
    temp_vehi=copy.deepcopy(vehicles_list)
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
            random_package_in_vehicles (temp_vehi,package)
            vehicles_list.extend(temp_vehi)
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
        # return to shop    
        x_new=0
        y_new=0
        dx=x_old-x_new  
        dy=y_old-y_new
        dx = dx**2   #dx^2
        dy = dy**2   #dy^2   
        sq=math.sqrt(dx+dy)
        x_old = x_new
        y_old = y_new
        total_cost +=sq


    return total_cost        

def priority_cost (vehicles_list):
    total_cost=0
    table ={ 1:5 , 2:4 , 3:3 , 4:2, 5:1 }
    for i in range(len(vehicles_list)):
        j=0
        while len(vehicles_list[i]) > 2 :
            priority=vehicles_list[i][2][1]
            total_cost +=table[priority]-j
            #delete package
            vehicles_list[i].pop(2) #delete package
            j +=1
    del vehicles_list                 
    return total_cost



#? to determine the path 
def path_list_f (path_list,vehicles_list):
    for i in range(len(vehicles_list)):
        while len(vehicles_list[i]) > 2 :
            v_id=vehicles_list[i][0]
            p_id=vehicles_list[i][2][0]
            path_list.append([v_id,p_id])
            vehicles_list[i].pop(2) #delete package
    del vehicles_list        

       
        
          








                

############################################    main    ##################################################### 

package =load_packages ()
vehicles_list=load_vehicles() 
max_weight =0
for product in package: #loop to know the max weight 
    if product[2] > max_weight: 
        max_weight = product[2]
max_v_capacity=0
for v in vehicles_list: #loop to know the max weight 
    if v[1] > max_v_capacity: 
        max_v_capacity = v[1]
if max_v_capacity < max_weight:
    print (" the number that you entered is too small ... \n")       
else:     
    algo = menu() # use max number of capacity validation
    while(True):
        if algo == 1:
            SA(package,vehicles_list) #number of vehicles and it capacity 
        elif algo == 2 :
            GA(package,vehicles_list)#number of vehicles and it capacity 
        else:
            print ("           .......   End program  .....         ")
            break
        algo = menu()         

    





