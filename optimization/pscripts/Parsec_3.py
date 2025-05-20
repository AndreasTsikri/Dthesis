
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from pscripts.finite_dif import *
from pscripts.finite_diff_2 import *

def parsec(x,a, b, c,d,e,f):    
    #6th order polynomial
    exp=[i/2. for i in range(1,12,2)]
    try:      
        ef= a*(x**exp[0]) + b*(x**exp[1]) + c*(x**exp[2]) + d*(x**exp[3]) + e*(x**exp[4])+ f*(x**exp[5])   
        return  ef        
    except:
        raise('problem with x= {}'.format(x))
        
def Amat( Xmax):
        return np.array(
            [[1.0,          1.0,         1.0,          1.0,          1.0        ],
             [Xmax**1.5,        Xmax**2.5,       Xmax**3.5,        Xmax**4.5,        Xmax**5.5],
             [1.5,          2.5,         3.5,          4.5,          5.5        ],
             [1.5* Xmax**0.5,   2.5* Xmax**1.5,  3.5*Xmax**2.5,   4.5*Xmax**3.5,   5.5*Xmax**4.5 ],
             [0.75*Xmax**-0.5, 3.75*Xmax**0.5, 8.75*Xmax**1.5, 15.75*Xmax**2.5, 24.75*Xmax**3.5]])

def Bmat(Xmax,Ymax,a1,tan_thita,sb):
    return np.array([-a1,
                     Ymax-a1*Xmax**0.5,
                     tan_thita-0.5*a1,
                     -0.5*a1*Xmax**-0.5,
                     sb+0.25*a1*Xmax**-1.5])

#up --> check if it is the upper or lower surface!
def parsec_params(real_surface_points,up=True):
    #if real_surface_points.index.start !=0:
        #raise Exception("dataframe indexes must be at the form ' index =0 at x0=0 ,index = n at xn=1 ',starting from 0 end to n!")
    if up:
        ycrest=max(real_surface_points['Y'])
        xcrest=float(real_surface_points['X'][real_surface_points['Y']==ycrest])
    else:
        ycrest=min(real_surface_points['Y'])
        xcrest=float(real_surface_points['X'][real_surface_points['Y']==ycrest])
    #ycrest=max(real_surface_points['Y'])
    #xcrest=float(real_surface_points['X'][real_surface_points['Y']==ycrest])
    idx_crest=real_surface_points['X'][real_surface_points['Y']==ycrest].index
    #dy2/dx2 at y=ymax using CENTRAL DIFF! --->sb
    pidx_crest=real_surface_points['X'][real_surface_points['Y']==ycrest].index
    idxs=[idx_crest-2,idx_crest-1,idx_crest,idx_crest+1,idx_crest+2]

    y_surface=list([float(real_surface_points['Y'][idxs[i]]) for i in range(len(idxs))])
    x_surface=list([float(real_surface_points['X'][idxs[i]]) for i in range(len(idxs))])
    #_,sb=central_dif(real_surface_points,idxs)
    sb=second_deriv_central_dif(x_surface,y_surface)[1]
    ##print(sb)

    #a1-using FORWARD DIFF!
    #idxs=[real_surface_points['X'].index[0],real_surface_points['X'].index[1],real_surface_points['X'].index[2]]
    idxs=[real_surface_points['X'].index[1],real_surface_points['X'].index[2],real_surface_points['X'].index[3]]
    x_surface=list([float(real_surface_points['X'][idxs[i]]) for i in range(len(idxs))])
    y_surface=list([float(real_surface_points['Y'][idxs[i]]) for i in range(len(idxs))])

    fderivs_atLE=forward_dif(x_surface,y_surface)

    Rle=((1.+(fderivs_atLE[0])**2.)**1.5)/fderivs_atLE[1]
    Rle=abs(Rle)

    a1=(2.*Rle)**0.5
    print("Rle,a1: ",Rle,a1)

    ##tan_thita using BACKWARD DIFF!
    idxs=[real_surface_points['X'].index[-2],real_surface_points['X'].index[-1]]
    x_surface=list([float(real_surface_points['X'][idxs[i]]) for i in range(len(idxs))])
    y_surface=list([float(real_surface_points['Y'][idxs[i]]) for i in range(len(idxs))])
    #print(idxs)
    tan_thita=first_deriv_backward_dif(x_surface,y_surface)
    #print("tan_thita",tan_thita)
    #params dict
    params_labels=["a1","tan_thita","xmax","ymax","sb"]
    params={f"{i}":0 for i in params_labels}
    
    if up:
        params["a1"]=a1
    else:
        params["a1"]=-a1
        
    params["tan_thita"]=tan_thita
    params["xmax"]=xcrest
    params["ymax"]=ycrest
    params["sb"]=sb
    ##print(params)

    return params

def parsec_coefs(params):
    if type(params)!= dict:
        print('please make params as a dict with 5 key-value pairs')
        return -1
    if len(params) !=5 :
        print('please make params list to have 5 elements')
        return -1
    xmax=params['xmax']
    ymax=params['ymax']
    a1=params['a1']
    tan_thita=params['tan_thita']#first derive at x=0
    sb=params['sb']#second derivative at x=xmax
    
    A=Amat(xmax)
    B=Bmat(xmax,ymax,a1,tan_thita,sb)
    solution=np.linalg.solve(A,B)
    ##print(solution)
    solution=np.insert(solution,0,[a1])
    ##print(solution)
    return solution

def plot_parsec(f,coefs,real_surface_points,title='aifoil PARSEC parametarization'):
    #x=np.linspace(0,1,150)
    
    plt.scatter(real_surface_points['X'],f(real_surface_points['X'],*coefs))  
    plt.scatter(real_surface_points['X'],real_surface_points['Y'])
    #plt.scatter(x,f(x,*coefs))
    
    plt.title(title)
    
    #plt.title('aifoil PARSEC parametarization')
    
    #plt.scatter(downSurface['X'],downSurface['Y'])
    
    plt.xlim(-0.01,1)
    plt.legend(["fake airfoil(PARSEC)","true Airfoil-up","true Airfoil-down"])
    plt.show()
