#we use **_wrappers to try to catch errors if we have conflict when trying reading or writing files!!
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyswarms as ps
from math import atan,pi
import os
import time
import random

import pscripts.curve_fit_params as cfp
import pscripts.Parsec_3 as prc

#import file_handlers_ffa241 as fh
parsec=prc.parsec
parsec_coefs=prc.parsec_coefs
##LS
func2=cfp.func2
parsec_params_LS=cfp.curve_fit_params

def FFA_241_DAT_wrapper(xi_down,yi_down,xi_up,yi_up,out="t1.dat"):
    if type(xi_down)!=pd.Series or type(yi_down)!=pd.Series or type(xi_up)!=pd.Series or type(yi_up)!=pd.Series:
        raise Exception("args must be type of  pandas.Series ")
    try:
        #main func
        FFA_241_DAT(xi_down,yi_down,xi_up,yi_up,out=out)
    except:
        os.system(" echo 'exception occured-ffa_241.dat' >>exceptions.mine")
        time.sleep(0.1)
        #main func
        FFA_241_DAT(xi_down,yi_down,xi_up,yi_up,out=out)
        
def FFA_241_DAT(xi_down,yi_down,xi_up,yi_up,out="t1.dat",xFromAirfoil=True):#must get as argument first the down side!
    n1=len(xi_down)
    n2=len(xi_up)#or len(y)
    n=n1+n2
    print("n=",n)
    #if not from_airfoil:
    #if not isXFromAir:
   # if not xFromAirfoil:
    #x_topic=np.array(xi_down.sort_index(ascending=False))
    #y_topic=np.array(yi_down.sort_index(ascending=False))
    x_topic=np.array(xi_down)
    y_topic=np.array(yi_down)
    with open(out,"w") as f:
        phrase="%i\n"%(n)
        f.write(phrase)
        for i in range(n1):
            #phrase="\t%.5f"%x_topic[i]+"\t%.5f\n"%y_topic[i]
            phrase="\t%.6f"%x_topic[i]+"\t%.6f\n"%y_topic[i]#6 sign digits
            f.write(phrase)    
    x_topic=np.array(xi_up)
    y_topic=np.array(yi_up)
    with open(out,"a") as f:            
        for i in range(n2):
            #phrase="\t%.5f"%x_topic[i]+"\t%.5f\n"%y_topic[i]
            phrase="\t%.6f"%x_topic[i]+"\t%.6f\n"%y_topic[i]#6 sign digits
            f.write(phrase)
   # else:
   #     print("WE ENTER THE AIRFOIL")
   #     with open(out,'w') as f:
   #         first_line=str(n1+n2)+'\n'
   #         f.write(first_line)
   #         for i in range(len(xi_down)):
   #             str_to_write="    "+"%.6f"%xi_down[i]+"\t"+"%.6f"%yi_down[i]+"\n"
   #             f.write(str_to_write)
   #         for i in range(len(xi_up)):
   #             str_to_write="    "+"%.6f"%xi_up[i]+"\t"+"%.6f"%yi_up[i]+"\n"
   #             f.write(str_to_write)
###--------------------------------#--------------------------------


#wrapper
def distr_wrapper(xi_down,parsec_coefs_up,parsec_coefs_down,out="t1.inp"):
    if type(xi_down)!=pd.Series:#-->kalutera kanta ola arrays eks arxhs!
        raise Exception("xi_down must be type of  pandas.Series ")
    try:
        #main func
        distr_TESTERS(xi_down,parsec_coefs_up,parsec_coefs_down,out=out)
    except:
        os.system(" echo 'exception occured-distr.inp' >>exceptions.mine")

        os.system("cp ../fwtest_4/distr.inp .")

        #time.sleep(0.1)
        timer=random.random()*0.5+random.random()*0.2

        time.sleep(timer)
        #main func
        distr_TESTERS(xi_down,parsec_coefs_up,parsec_coefs_down,out=out)#gia na to kaneis swsta edw vale anti gia distr_TESTERS-->distr_wrapper!


def distr_TESTERS(xi_down,parsec_coefs_down,parsec_coefs_up,out="t1.inp"):
    yi_topic_down=np.array(parsec(xi_down,*parsec_coefs_down))
    yi_topic_up=np.array(parsec(xi_down,*parsec_coefs_up))
    
    #thicknes
    thick="%.2f"%(100*max(yi_topic_up-yi_topic_down))
    if ( len(thick.split(".")[0])) <2:
        #print(thick)
        thick="0" + thick
        #print("thick=",thick,"len of first two =",len(thick.split(".")[0]))
    with open("distr.inp","r") as f:
        lines=np.array(f.readlines())            
    new_lines=[lines[0],lines[1]]
    for line in lines[2:]:
        split=line.split()
        #print(split)
        split[-1]=str(thick)
        nl=""
        for numb in split:
            nl=nl+numb+"\t"
        nl=nl+"\n"
        new_lines=np.append(new_lines,nl)        
        with open(out,"w") as f:
            for line in new_lines:
                f.write(line)


#--------------------------------#--------------------------------
                
                
def airfoil_inp_wrapper(xi_down,parsec_coefs_down,parsec_coefs_up,out='test_airfoil.dat'):
    if type(xi_down)!=pd.Series:#-->kalutera kanta ola arrays eks arxhs!
        raise Exception("xi_down must be type of  pandas.Series ")
    try:
        #main func
        airfoil_inp(xi_down,parsec_coefs_down,parsec_coefs_up,out=out)
    except:
        os.system(" echo 'exception occured-airfoil.inp' >>exceptions.mine")
        time.sleep(0.2)
        #main func
        airfoil_inp(xi_down,parsec_coefs_down,parsec_coefs_up,out=out)


def airfoil_inp(xi_down,parsec_coefs_down,parsec_coefs_up,out='airfoil.TEST'):
    
    yi_topic_down=np.array(parsec(xi_down,*parsec_coefs_down))
    yi_topic_up=np.array(parsec(xi_down,*parsec_coefs_up))    
    #thicknes
    thick="%.2f"%(100*max(yi_topic_up-yi_topic_down))
    if ( len(thick.split(".")[0])) <2:
        #print(thick)
        thick="0" + thick
        #print("thick=",thick,"len of first two =",len(thick.split(".")[0]))
    print("thick=",thick)
    with open("airfoil.inp","r") as f:
        lines=f.readlines()
    splitted_line=lines[9].split()
    splitted_line[0]=thick
    
    line_to_write="   "
    spaces="          "
    for i in splitted_line:
        #line_to_write=line_to_write+i+'\t\t'
        line_to_write=line_to_write + i + spaces
    line_to_write=line_to_write+'\n'
    
    with open(out,'w') as f :
        for i in range(len(lines)):
            if i!=9 :
                write_=lines[i]
            else:
                write_=line_to_write
            f.write(write_)

#--------------------------------#--------------------------------
            
def execute_file(test=1.,name_of_file="a.out"):
    try:
        #os.system(f"./{name_of_file}")
        #os.system(f"./{run_airfoil_ONLY_NACA}")#this claculate deltas only for naca0012!

        ###os.system(f"./{name_of_file}")

        #print("test value instead of executing fortran!:",test)
        print("Executed fortran!: OK")
    except:
        raise Exception("problem when executing fortran")
        
#--------------------------------#--------------------------------
        
def read_objective(name="objective.dat"):
    try:
        with open(name,"r") as f:
            objf=float(f.readline())
            
        if type(objf) != float:
            raise Exception("objective must be float value")
        return objf
    except:
        raise Exception("problem reading objective function!")
