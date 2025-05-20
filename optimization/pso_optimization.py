import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pyswarms as ps
from pyswarms.utils.plotters import (plot_cost_history)

from math import atan,pi

import os
import time
import random
import json 

import pscripts.curve_fit_params as cfp
import pscripts.Parsec_3 as prc

import file_handlers_ffa241 as fh

#define sum local functions
parsec=prc.parsec
parsec_coefs=prc.parsec_coefs

#Least Squares
func2=cfp.func2
parsec_params_LS=cfp.curve_fit_params
def define_x_coords(points_front=51,points_back=21):
    totalp=points_front+points_back    
    xf=np.linspace(0,0.2,points_front)#xf=np.linspace(0,0.1,points_front)
    
    xb=np.linspace(0.21,1,points_back)#xb=np.linspace(0.11,1,points_back)#xb=np.linspace(0.12,1,points_back)#THIS WAS BAD DISTRIBUTION---ERROR OF F2W

    xtotal=np.concatenate([xf,xb])    
    xtotal=np.concatenate([xtotal,xtotal])#xtotal=np.linspace(0,1,totalp)
    xtotal=pd.Series(xtotal)

    xi_down=xtotal[:totalp]
    xi_up=xtotal[totalp:]
    return xi_down,xi_up

def calculate_coefficients(surface,method="LS",isupsurface=True):
    try:
        if isupsurface:
            title="upSurface"
            
        else:
            title="downSurface"

        if method == "LS":
            popt1,_=cfp.fit(surface,func2)


            prc_prms_LS=parsec_params_LS(surface,popt1,up=isupsurface)
            prc_cfs_LS=parsec_coefs(prc_prms_LS)

            return prc_prms_LS,prc_cfs_LS
        elif method=="FD":
            prc_prms_fd=parsec_params_fd(surface,up=isupsurface)
            prc_cfs_fd=parsec_coefs(prc_prms_fd)
            return prc_prms_fd,prc_cfs_fd
        else:
            raise Exception("method has to be 'LS' or 'FD' ")
    except:
        raise Exception('problem with coefficients')
        
def calculate_range(params,percentage=1./100.):
    bound={"up":0,"base":0,"down":0}
    c_range={key:i for i,key in enumerate(params.keys())}
    keys_list=list(c_range.keys())
    for i,coef in enumerate(params.values()):
        base=float("%.5f"%coef)
        up=float("%.5f"%(base+abs(base*percentage)))
        down=float("%.5f"%(base-abs(base*percentage)))
        
        bound["base"]=base;bound["up"]=up;bound["down"]=down;    
        
        c_range[keys_list[i]]=bound.copy()
    return c_range

def bounds_for_pso( range_up, range_down, *k, **kw):
    #bounds
    b1=[]#upper
    b2=[]#down
    
    #coefs from down surface to upsurface
    for alfa in range_down.values():
        #print(alfa["up"]>alfa["down"])
        if alfa["up"]>alfa["down"]:
            b1.append(alfa['up'])
            b2.append(alfa["down"])
        else:
            b1.append(alfa['down'])
            b2.append(alfa["up"])
    i=0
    for alfa in range_up.values():
        #print(alfa["up"]>alfa["down"])
        if alfa["up"]>alfa["down"]:
            b1.append(alfa['up'])
            b2.append(alfa["down"])
        else:
            b1.append(alfa['down'])
            b2.append(alfa["up"])
    b1=np.array(b1)
    b2=np.array(b2)
    bounds=(b2,b1)    
    return bounds

#CONSTRAIN
def constrain(sderiv):
    violation=False
    times=0
    for i in range(len(sderiv)-1):
        if sderiv[i]*sderiv[i+1]<=0:
            times+=1
    if times>1:
        violation=True    
    return violation#return violation,times

#read x-COORDINATES from "airfoil"
def x_coords_from_airfoil():
    with open("airfoil","r") as f:
        lines=f.readlines()
    lines.pop(0)
    lines.pop(0)
    xall=[]
    for line in lines:
        ex,_=line.split()
        xall.append(float(ex))
    xall=pd.Series(xall)
    xd=xall[:60]
    xu=xall[60:]
    return xd,xu

#PSO functions
def yi_TESTER(x):#main function  -> x = [param,down ,... param,up]
    
    n_particles=x.shape[0]
    n_params=x.shape[1]    
    params_names=['a1', 'tan_thita', 'xmax', 'ymax', 'sb']

    objective=np.arange(n_particles,dtype=float)
    i=0
    for part in (x):
        
        params_down={params_names[i]:inside for i,inside in enumerate(part) if (i<len(part)/2)}
        
        params_up={params_names[i-n_params]:inside for i,inside in enumerate(part) if inside not in params_down.values() }
        
        
        #1.calculate coefficients from params 
        coefs_down=parsec_coefs(params_down)
        coefs_up=parsec_coefs(params_up)
        
        #2.calculate points y
        yi_down=parsec(xi_down,*coefs_down)##yi_down --same type as -->xi_down,
        yi_up=parsec(xi_up,*coefs_up)
        
        #2.1 CHECK CONSTRAIN
        yi_test_up=np.array(yi_up)
        yi_test_up=yi_test_up[30:]
        sderiv=np.diff(yi_test_up,n=2)
        violation=constrain(sderiv)
        
        #3.write files
        if violation:
            objF=100.
        else:#if not violation then run the fortran!!
            ##ffa24_11.dat
            fh.FFA_241_DAT_wrapper(xi_down,yi_down,xi_up,yi_up,out="ffa_TES.dat")#dont forget to change the "airfoil.inp " file also!
            #FFA_241_DAT_wrapper(xi_down,yi_down,xi_up,yi_up,out="t2.dat")
            #FFA_241_DAT(xi_up,y_up,out="t1.dat",up=False)
            
            ##distr.inp
            #fh.distr_wrapper(xi_down,coefs_down,coefs_up,out="t1.inp")\
            fh.distr_wrapper(xi_down,coefs_down,coefs_up,out="distr.inp")\
            #distr_wrapper(xi_down,coefs_down,coefs_up,out="t1.inp")
            
            ##airfoil.inp
            fh.airfoil_inp_wrapper(xi_down,coefs_down,coefs_up,out='airfoil.inp')
            #airfoil_inp_wrapper(xi_down,coefs_down,coefs_up,out='test_airfoil.dat')
            print("OK")
            ##execute fortran
            #fh.execute_file(test=1.,name_of_file="a.out")
            #fh.execute_file(test=1.,name_of_file="run_airfoil_MY_AIRFOIL")
            fh.execute_file(test=1.,name_of_file="run_airfoil_MY_AIRFOIL_2")#--->se auto grafw to 'airfoil' me ligotera dekadika!
            
            ##read output of calc_sound, "objective.dat"
            objF=fh.read_objective(name="objective.dat")
            print(objF,type(objF))


            #os.system(f"echo {params_up} >> paramsAndObjective.mine")
            #os.system(f"echo {params_down} >> paramsAndObjective.mine")
        file_to_write="paramsAndObjective.mine"
        with open(file_to_write,"a") as f:
            f.write(json.dumps(params_up))
            f.write("\n")
            f.write(json.dumps(params_down))
            f.write("\n")
        #os.system(f"echo {objective[i]} >> paramsAndObjective")
        #os.system(f"echo {objF} >> paramsAndObjective.mine")
        os.system(f" echo {objF} >> paramsAndObjective.mine ")

        objective[i]=objF#for each particle save objectiveF to an array!
        i+=1
    print("objective:",objective)
    return objective #return np.ones(n_particles)
    

#'rosenbrock_with_args' is the inpt fnction on pso.It can have any name!
def rosenbrock_with_args(x):
    
    print("START PYTHON")
    #random_time= random.random()*0.2+random.random()*0.3+random.random()*0.5#+random.random()*0.2+random.random()*0.2
    #random_time= random.random()*0.5+random.random()*0.5+random.random()*0.5#+random.random()*0.2+random.random()*0.2
    #random_time= random.random()*0.5+random.random()*random.random()*0.3 +random.random()*0.2#+random.random()*0.2
    #random_time=random.random()*0.1+random.random()*0.6+ random.random()*0.5+random.random()*random.random()*0.3 +random.random()*0.2#+random.random()*0.2
    #random_time=random.random()*0.5+random.random()*0.6+ random.random()*0.5+random.random()*random.random()*0.4+random.random()*0.9 #+random.random()*0.2
    #random_time=random.random()*0.5+ random.random()*0.2 + random.random()*0.5 + random.random()*0.5
    #os.system(f" echo {random_time} >> outputTime.mine ")
    #time.sleep(random_time)
    #y=yi(x)    
    #print("OF:",y)
    #print("y=",y)
    y=yi_TESTER(x)
    return y
#-----------------------        
#MAIN PROGRAM
#-----------------------

#read initial ffa_241.dat and 'save' X column for use
with open("ffa_241.dat","r") as f:
    lines=f.readlines()
X=[]
Y=[]
for line in lines[1:]:
    x,y=(line.split())
    X.append(x)
    Y.append(y)
dc={"X":X,"Y":Y}
df=pd.DataFrame(dc)

downSurface=df[:53]
#upperSurface=df[52:]
upperSurface=df[53:]
#upperSurface=df[51:]
upperSurface=upperSurface.astype(float)
downSurface=downSurface.astype(float)

#SAVE ORIGINAL FILE
for file in [downSurface,upperSurface]:
    with open("./ORIGINAL_FFA.dat", 'a') as f:
        dfAsString = file.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write("\n")

downSurface=downSurface.sort_index(ascending=False)
downSurface=downSurface.reset_index()
downSurface.drop('index',inplace=True,axis=1)

#define GLOBAL xi_up,xi_down from the original ffa2411

#xi_up=upperSurface['X']#here it is pd.Series-->change xi_down and xi_up to to numpy array!
#xi_down=downSurface['X']
#xi_down,xi_up=define_x_coords(points_front=41,points_back=31)
#xi_down,xi_up=define_x_coords(points_front=35,points_back=25)
#xi_down,xi_up=define_x_coords(points_front=24,points_back=26)

#xi_down,xi_up=define_x_coords(points_front=25,points_back=35)
xi_down,xi_up =x_coords_from_airfoil()

print("x coords=",xi_down,xi_up)
#parameters of original ffa2411
PARAMS_LS_UP, _ =calculate_coefficients(upperSurface,method="LS",isupsurface=True)
PARAMS_LS_DOWN, _=calculate_coefficients(downSurface,method="LS",isupsurface=False)
print("PARAMETERS OF PARSEC AFTER PERFORMING LEAST SQUARES APPROXIMATION ON FFA POINTS\n")
print(f"PARAMS_UP:\n{PARAMS_LS_UP}")
print(f"PARAMS_DOWN:\n{PARAMS_LS_DOWN}")

#bounds for PSO

percentage=8./100#percentage=10./100..#percentage=3./100.

range_down=calculate_range(PARAMS_LS_DOWN,percentage)
range_up=calculate_range(PARAMS_LS_UP,percentage)

#print("range_up\n",range_up,"\nrange_down\n",range_down)
bounds=bounds_for_pso(range_up,range_down)
print("BOUNDS\n",bounds)

if not (bounds[0]<bounds[1]).all():
    raise Exception("problem with bounds:lower bounds must be LOWER than UPPER bounds!!")
    
#PSO
# Initialize swarm
#options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
#options = {'c1': 0.9, 'c2': 0.2, 'w':0.9}
#options = {'c1': 0.4, 'c2': 0.8, 'w':1.0}
#options = {'c1': 0.4, 'c2': 1.0, 'w':0.7}
#options = {'c1': 2.0, 'c2': 0.5, 'w':0.8}
options = {'c1': 0.5, 'c2': 2.0, 'w':0.8}
#c1-->personal best, c2 ---> global best

my_particles=2#my_particles=6
my_processes=1
my_iterations=1#my_iterations=50

# Call instance of PSO with bounds argument
optimizer = ps.single.GlobalBestPSO(n_particles=my_particles, dimensions=10, options=options, bounds=bounds)#optimizer = GlobalBestPSO(n_particles=1, dimensions=10, options=options, bounds=bounds)

#worker
if __name__=='__main__':
    
    cost, pos = optimizer.optimize(rosenbrock_with_args,iters=my_iterations,n_processes=my_processes)
    

    plot_cost_history(cost_history=optimizer.cost_history)
    plt.show()
    plt.savefig(f"historyplot-{my_iterations}iters-{my_particles}part-{my_processes}proc")