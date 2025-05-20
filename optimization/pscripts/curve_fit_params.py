import scipy.optimize as optimization
import pandas as pd
#func2 -->function to be fitted on data
def func2(x,a, b, c,d,e,f):    
    #6th order polynomial
    exp=[i/2. for i in range(1,12,2)]
    try:      
        ef= a*(x**exp[0]) + b*(x**exp[1]) + c*(x**exp[2]) + d*(x**exp[3]) + e*(x**exp[4])+ f*(x**exp[5])   
        return  ef        
    except:
        raise('problem with x= {}'.format(x))

def fit(upperSurface,func2):
    xdata1=upperSurface['X']
    ydata1=upperSurface['Y']

    popt1, pcov1 = optimization.curve_fit(func2,xdata1, ydata1)
    return [popt1,pcov1]

def curve_fit_params(upperSurface,popt1,up=True):#'popt1' are coefficients of the 6th order fitted curve 
    if up:
        ymax=max(upperSurface['Y'])
    else:
        ymax=min(upperSurface['Y'])

    xmax=float(upperSurface.loc[upperSurface['Y']== ymax]['X'])
    print('xmax= %f'%xmax)
    a1=popt1[0]
    Rle=a1*a1/2.
    tan_thita=0
    for i in range(1,7):
        tan_thita=tan_thita+ popt1[i-1]*(i-0.5)
    sb=0
    for i in range(1,7):
        sb=sb + popt1[i-1]*(i-0.5)*(i-1.5)*(xmax**(i-2.5))
    #thita=atan(tan_thita)

    #params dict
    params_labels=["a1","tan_thita","xmax","ymax","sb"]
    params={f"{i}":0 for i in params_labels}

    params["a1"]=a1
    params["tan_thita"]=tan_thita
    params["xmax"]=xmax
    params["ymax"]=ymax
    params["sb"]=sb

    print(params)
    return params
