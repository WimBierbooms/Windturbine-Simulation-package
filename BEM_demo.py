from aero import aero
from bem import bem
import numpy as np
import matplotlib.pyplot as plt
wm = plt.get_current_fig_manager() 
wm.window.attributes('-topmost', 1)
wm.window.attributes('-topmost', 0)

## written by Dennis van Dommelen, 2014

def BEM_demo():
    print 'This is a demonstration of Blade Element Momentum theory (BEM)'
    print ''
    print 'Note that the corresponding Python commands are given'
    print 'Proceed by pressing enter'
    print ''
    print 'Dennis van Dommelen'
    print 'Date: 11-12-13'

    raw_input("_____________________________________________________________ \n")
    print 'Blade Element Momentum theory is a combination of the blade-element method and momentum theory'
    print ''
    print 'We start with the blade-element method; it is implemented in the python routine aero, by typing: \'help(aero)\' we can find the input arguments for this function.'
    help(aero)

    raw_input("_____________________________________________________________\n")
    print 'As example we use the a wind turbine of your choice: first all the parameters of this turbine are put in the parameter vectors P1, P2, P3 and P4'
    print ''
    print 'Choose one of the following wind turbines:'
    windturbine = raw_input("Type the wind turbine you would like to analyse, e.g. V90, S88, NREL_5MW: ")
    print 'The aerodynamic forces depend on the operational conditions; for this demo we consider the following mean wind speed (m/s), rotational speed (rad/s) and pitch angle (degrees)'
    print '_____________________________________________________________'
    print 'windturbine_name = windturbine+\'.txt\''
    print '[P1,P2,P3,P4]=eval(open(windturbine_name, \'r\').read())'
    print 'V=7.'
    print 'R=P2[0]'
    print 'Lambda_nominal = P4[1]'
    print 'omr=Lambda_nominal*V/R'
    print 'theta=P4[2]'
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]=eval(open(windturbine_name, 'r').read())
    V=7.
    R=P2[0]
    Lambda_nominal = P4[1]
    omr=Lambda_nominal*V/R
    theta=P4[2]

    raw_input("_____________________________________________________________ \n")
    print 'For values of the induction factor a in between 0 and 1 the thrust coefficient Cdax is calculated'
    print 'First create some empty lists: '
    print '_____________________________________________________________'
    print 'a=[]'
    print 'Dax = []'
    print 'Mbeta = []'
    print 'Mr = []'
    print 'P = []'
    print 'Cdax1 = []'
    print 'Cp = []'
    print '_____________________________________________________________'
    print '\n Then with using a for loop calculate the values which should be added to the list'
    print '_____________________________________________________________'
    print 'for i in range(101): \n        a.append(i/100.) \n        [Daxi,Mbetai,Mri,Pi,Cdax1i,Cpi]=aero(a[i],V,theta,0,omr,0,windturbine) \n         Dax.append(Daxi) \n        Mbeta.append(Mbetai) \n        Mr.append(Mri) \n         P.append(Pi) \n         Cdax1.append(Cdax1i) \n        Cp.append(Cpi) \n'
    print '_____________________________________________________________'
    print 'Now the plot can be created using the standard plt.plot(x,y) and plt.show() command, it may take a moment for the plot to appear so please wait'
    a=[]
    Dax = []
    Mbeta = []
    Mr = []
    P = []
    Cdax1 = []
    Cp = []
    for i in range(101):
        a.append(i/100.)
        [Daxi,Mbetai,Mri,Pi,Cdax1i,Cpi]=aero(a[i],V,theta,0,omr,0,windturbine)
        Dax.append(Daxi)
        Mbeta.append(Mbetai)
        Mr.append(Mri)
        P.append(Pi)
        Cdax1.append(Cdax1i)
        Cp.append(Cpi)
    plt.plot(a,Cdax1)
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.show()
    print "_____________________________________________________________ \n"
    print 'Next momentum theory is applied; the relation between the thrust coefficient Cdax and the induction factor a is given by:'
    print 'Cdax2=4*a.*(1-a) \n This is again calculated by first creating lists, then appending the values like before'
    Cdax2 =[]
    for i in range(len(a)):
        Cdax2.append(4*a[i]*(1-a[i]))
    plt.plot(a,Cdax2)
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.show()

    print "_____________________________________________________________ \n"
    print 'The relations between the thrust coefficient Cdax and the induction factor a according to the blade-element method and momentum theory can be shown in one graph'
    plt.plot(a,Cdax1,a,Cdax2,'--')
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.legend(('blade element theory','momentum theory'))
    plt.show()
    
    print "_____________________________________________________________ \n"
    print 'The essence of BEM is the calculation of the induction factor a by equating the expressions according to the blade-element method and momentum theory (i.e. the intersection of the 2 lines'
    print ''
    print 'The induction factor can be calculated in an iterative way:'
    print 'We start with some initial guess, say 0.7 and calculate the corresponding thrust coefficient according to the blade-element method, i.e. this point lies on the blue line and is indicated by a red cross'
    a0=0.5
    [Dax,Mbeta,Mr,P,Cdax0,Cp]=aero(a0,V,theta,0,omr,0,windturbine)
    plt.plot(a,Cdax1,a,Cdax2,'--')
    plt.plot(a0,Cdax0,'r*')    
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.legend(('blade element theory','momentum theory'))
    plt.show()

    print "_____________________________________________________________ \n"
    print 'Next a new induction factor is calculated from the value of the trust coefficient according to momentum theory, i.e. this point lies on the green line and is indicated by a red circle'
    print ''
    print 'Note: for this purpose we have to rewrite the (quadratic) expression according to momentum theory'
    plt.plot(a,Cdax1,a,Cdax2,'--')
    plt.plot(a0,Cdax0,'m*')
    a0=0.5-0.5*np.sqrt(1.-Cdax0)
    plt.plot(a0,Cdax0,'ro')
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.legend(('blade element theory','momentum theory'))
    plt.show()

    print "_____________________________________________________________ \n"
    print 'We can repeat this untill convergence is reached; the new points are indicated in red, the older ones in magenta'
    
    plt.plot(a,Cdax1,a,Cdax2,'--')
    plt.plot(a0,Cdax0,'mo')
    [Dax,Mbeta,Mr,P,Cdax0,Cp]=aero(a0,V,theta,0,omr,0,windturbine)
    plt.plot(a0,Cdax0,'r*')
    a0=0.5-0.5*np.sqrt(1.-Cdax0)
    plt.plot(a0,Cdax0,'ro')
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.legend(('blade element theory','momentum theory'))
    plt.show()
    
    print "_____________________________________________________________ \n"
    print 'We can repeat this untill convergence is reached; the new points are indicated in red, the older ones in magenta'
    
    plt.plot(a,Cdax1,a,Cdax2,'--')
    plt.plot(a0,Cdax0,'mo')
    [Dax,Mbeta,Mr,P,Cdax0,Cp]=aero(a0,V,theta,0,omr,0,windturbine)
    plt.plot(a0,Cdax0,'r*')
    a0=0.5-0.5*np.sqrt(1.-Cdax0)
    plt.plot(a0,Cdax0,'ro')
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.legend(('blade element theory','momentum theory'))
    plt.show()


    print "_____________________________________________________________ \n"
    print 'We can repeat this untill convergence is reached; the new points are indicated in red, the older ones in magenta'
    
    plt.plot(a,Cdax1,a,Cdax2,'--')
    plt.plot(a0,Cdax0,'mo')
    [Dax,Mbeta,Mr,P,Cdax0,Cp]=aero(a0,V,theta,0,omr,0,windturbine)
    plt.plot(a0,Cdax0,'r*')
    a0=0.5-0.5*np.sqrt(1.-Cdax0)
    plt.plot(a0,Cdax0,'ro')
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.legend(('blade element theory','momentum theory'))
    plt.show()

    print "_____________________________________________________________ \n"
    print 'We can repeat this untill convergence is reached; the new points are indicated in red, the older ones in magenta'
    
    plt.plot(a,Cdax1,a,Cdax2,'--')
    plt.plot(a0,Cdax0,'mo')
    [Dax,Mbeta,Mr,P,Cdax0,Cp]=aero(a0,V,theta,0,omr,0,windturbine)
    plt.plot(a0,Cdax0,'r*')
    a0=0.5-0.5*np.sqrt(1.-Cdax0)
    plt.plot(a0,Cdax0,'ro')
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.legend(('blade element theory','momentum theory'))
    plt.show()

    print "_____________________________________________________________ \n"
    print 'We can repeat this untill convergence is reached; the new points are indicated in red, the older ones in magenta'
    
    plt.plot(a,Cdax1,a,Cdax2,'--')
    plt.plot(a0,Cdax0,'mo')
    [Dax,Mbeta,Mr,P,Cdax0,Cp]=aero(a0,V,theta,0,omr,0,windturbine)
    plt.plot(a0,Cdax0,'r*')
    a0=0.5-0.5*np.sqrt(1.-Cdax0)
    plt.plot(a0,Cdax0,'ro')
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.legend(('blade element theory','momentum theory'))
    plt.show()


    print "_____________________________________________________________ \n"
    print 'We can repeat this untill convergence is reached; the new points are indicated in red, the older ones in magenta'
    
    plt.plot(a,Cdax1,a,Cdax2,'--')
    plt.plot(a0,Cdax0,'mo')
    [Dax,Mbeta,Mr,P,Cdax0,Cp]=aero(a0,V,theta,0,omr,0,windturbine)
    plt.plot(a0,Cdax0,'r*')
    a0=0.5-0.5*np.sqrt(1.-Cdax0)
    plt.plot(a0,Cdax0,'ro')
    plt.xlabel('induction factor a (-)')
    plt.ylabel('thrust coefficient (-)')
    plt.legend(('blade element theory','momentum theory'))
    plt.show()

    print "_____________________________________________________________ \n"
    print 'The final answer is:',a0

    raw_input("_____________________________________________________________ \n")
    print 'It is also possible to find the intersection by use of the standard scipy.optimize routine \'fsolve\'. This is implemented in the routine \'bem\' (in combination with \'fun_bem\')'
    [Dax,Mbeta,Mr,P,Cdax,Cp,a]=bem(V,theta,0,omr,0,windturbine)
    print 'a=',a

    raw_input("_____________________________________________________________ \n")
    print 'This ends the BEM demo'

