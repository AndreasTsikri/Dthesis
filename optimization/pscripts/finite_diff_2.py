def second_deriv_central_dif(x_surface,y_surface):
    x_mm, x_m, x, x_p, x_pp=x_surface
    y_mm, y_m, y, y_p, y_pp=y_surface
    
    #h_mm=x_m - x_mm
    h_mm=x_m - x_mm
    h_m=x - x_m
    h_p=x_p - x
    h_pp=x_pp - x_p
    
    fderiv_p=(y_pp-y)/(h_p+h_pp)
    fderiv_m=(y-y_mm)/(h_m+h_mm)
    #fderiv_m=(y_mm-y)/(h_m+h_mm)
    
    fderiv=(y_p-y_m)/(h_m+h_p)
    
    sderiv=(fderiv_p-fderiv_m)/(h_m+h_p)
    return fderiv,sderiv
#forward differences -->for Leading Edge
def forward_dif(x_surface,y_surface):
    x,x_plus,xpp=x_surface
    y,y_plus,ypp=y_surface
    h1=x_plus-x
    h2=xpp-x_plus
    fderiv=(y_plus-y)/h1
    f_deriv_p=(ypp-y_plus)/h2
    sderiv=(f_deriv_p-fderiv )/h1
    return [fderiv,sderiv]
#first derivative -->for Trealing Edge
def first_deriv_backward_dif(x_surface,y_surface):
    x_minus,x=x_surface
    y_minus,y=y_surface
    
    dh01=(x-x_minus)
    dy01=y-y_minus
    fderiv=dy01/dh01
    print("yminus,y = ",y_minus,y)
    return fderiv

