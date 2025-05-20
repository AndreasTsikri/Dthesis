"""def coefs(A,B,TA,TB):
    a0=A
    a1=TA
    #a2=3.*(B-A)-2.*TA-TA
    #a3=2.*(A-B)+TA+TB
    a2=TB-B+A
    a3=2.*(B-A)-TA -TB
    return [a0,a1,a2,a3]
"""
"""
params for NACA5410:
A=np.array([0,0])

B=np.array([1,0])

TA=np.array([0,0.1584])

TB=np.array([2.1241*(cos(-15.5253*pi/180.)),(2.1241*sin(-15.5253*pi/180.))])
"""
def coefs(A,B,TA,TB):
    a0=A
    a1=TA

    
    a2=3.*(B-A)-2.*TA-TB
    a3=TA+TB-2.*(B-A)

    #a2=3.*(B-A)-2.*TA-TA
    #a3=2.*(A-B)+TA+TB
    # a2=TB-B+A
    # a3=2.*(B-A)-TA -TB
    return [a0,a1,a2,a3]

def splines(u,coef):
    a0=coef[0].copy()
    a1=coef[1].copy()
    a2=coef[2].copy()
    a3=coef[3].copy()
    r1=a0[0]+a1[0]*u+a2[0]*u*u+a3[0]*u*u*u
    r2=a0[1]+a1[1]*u+a2[1]*u*u+a3[1]*u*u*u
    #r1=sum([coef[i][0]*(u**i) for i in range(4)])
    #r2=sum([coef[i][1]*(u**i) for i in range(4)])
    return [r1,r2]
