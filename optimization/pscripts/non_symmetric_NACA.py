from math import cos,sin,pi,tan,atan
def mean_camber(m,p,x):
    if x<p:
        yc=m*(2.*p*x-x*x)/(p*p)
        #dydx=(m/(p*p))*(2.*p-2.*x)
        dydx=(2.*m*(p-x))/(p*p)
    else:
        yc=m*((1.-2.*p)+2.*p*x-x*x)/((1.-p)**2.)
        dydx=(m)*(2.*p-2.*x) /((1.-p)**2.)
    return [yc,dydx]
    
def NACA00xx_thickness(x,thick=.12):
    #polyn=(0.2969*x**0.5)-0.1260*x-0.3516*x*x+0.2843*x*x*x-0.1036*x*x*x*x
    polyn=(0.2969*x**0.5)-0.1260*x-0.3516*x*x+0.2843*x*x*x-0.1036*x*x*x*x
    y=5.*(thick)*polyn
    return y
    

def non_symmetric_naca(m,p,x,thick=.12):
    mc= mean_camber(m,p,x)
    
    yc=mc[0]
    dycdx=mc[1]
    yt=NACA00xx_thickness(x,thick)
    thita=atan(dycdx)
    sin_thita=sin(thita)
    cos_thita=cos(thita)
    
    xu=x-yt*sin_thita
    xl=x+yt*sin_thita
    yu=yc+yt*cos_thita
    yl=yc-yt*cos_thita
    return [xu,yu],[xl,yl]
