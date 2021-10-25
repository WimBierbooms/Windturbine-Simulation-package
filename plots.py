from cplambda import cplambda
from powercurve1 import powercurve1
import matplotlib.pyplot as plt
import numpy as np
import timeit

## written by Dennis van Dommelen, 2014

def plots(windturbine,thetabool):
    ##Syntax plots(windturbine,thetabool)
    ##Inputs:       windturbine: the name of the windturbine file as a string
    ##                          e.g. 'V90'
    ##              thetabool: thetabool = True/False. If true, multiple thetas
    ##                          will be plotted against each other
    ##                          if false: only the nominal theta will be plotted

    ##runtime
    start = timeit.default_timer()
    
    ## required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())

    ##Creating a sequence for lambda
    lambdalist=[]
    for l in range(10,251,5):
        lambdalist.append(l/10.)

    ##the normal thetha
    thetan=P4[2]
    t_list = [thetan]
    
    ##the string for the legend (plot)
    theta_legend = ['Theta = '+str(thetan)]

    ##if thetabool is true, multiple thetas will be added to the list t_list
    if thetabool:
        for t in range(-5,26,5):
            if t>thetan:
                t_list.append(t)
                theta_legend.append('Theta = '+str(t))
    ##creating empty lists for the plots (multiple rows for multiple thetas)
    Cdax_list=[[0 for col in range(len(lambdalist))] for row in range(len(t_list))]
    Cp_list=[[0 for col in range(len(lambdalist))] for row in range(len(t_list))]
    a_list= [[0 for col in range(len(lambdalist))] for row in range(len(t_list))]

    ##Calculating the values for plotting
    for i in range(len(t_list)):
        theta = t_list[i]          
        [Cdax,Cp,a]=cplambda(windturbine,lambdalist,theta)
        Cdax_list[i]=Cdax
        Cp_list[i]=Cp
        a_list[i]=a
        
    ##Cdax Lambda curve
    fig=plt.figure()
    for i in range(len(Cdax_list)):
        plt.plot(lambdalist,Cdax_list[i])
    plt.grid(True)
    plt.ylabel('Cdax')
    plt.xlabel('Lambda')
    plt.legend(theta_legend)
    plt.title('Cdax Lambda curve '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/Cdax-lambda.png')
   

    ##Cp Lambda curve
    fig=plt.figure()
    for i in range(len(Cp_list)):
        plt.plot(lambdalist,Cp_list[i])
    plt.grid(True)
    plt.ylabel('Cp')
    plt.xlabel('Lambda')
    plt.axis([min(lambdalist),max(lambdalist),-0.6,0.6])
    plt.legend(theta_legend)
    plt.title('Cp Lambda curve for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/Cp-lambda.png')
    

    ##a Lambda curve
    fig=plt.figure()
    for i in range(len(a_list)):
        plt.plot(lambdalist,a_list[i])
    plt.grid(True)
    plt.ylabel('a')
    plt.xlabel('Lambda')
    plt.legend(theta_legend)
    plt.title('a Lambda curve for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/a-lambda-theta.png')
    
#---------------------------------------------------------------------------------#
    ##The next part will be for plotting the powercurve

    Vlist = []
    for v in range(5,251,5):
        Vlist.append(v/10.)
    [Dax_list,Mbeta_list,Mr_list,P_list,Cdax_list,Cp_list2,a_list2,theta_list,omr_list] = powercurve1(windturbine,Vlist)     
    
    ##Axial force curve
    fig=plt.figure()
    plt.plot(Vlist,Dax_list)
    plt.grid(True)
    plt.ylabel('Dax [N]')
    plt.xlabel('V [m/s]')
    plt.title('Axial force versus wind speed for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/Dax-v.png')


    ##Aerodynamic flap moment curve
    fig=plt.figure()
    plt.plot(Vlist,Mbeta_list)
    plt.grid(True)
    plt.ylabel('Mbeta [Nm]')
    plt.xlabel('V [m/s]')
    plt.title('Aerodynamic flap moment versus wind speed for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/Mbeta-v.png')

    ##Aerodynamic rotor torque curve
    fig=plt.figure()
    plt.plot(Vlist,Mr_list)
    plt.grid(True)
    plt.ylabel('Mr [Nm]')
    plt.xlabel('V [m/s]')
    plt.title('Aerodynamic rotor torque versus wind speed for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/Mr-v.png')

    ##Aerodynamic power curve
    fig=plt.figure()
    plt.plot(Vlist,P_list)
    plt.grid(True)
    plt.ylabel('P [W]')
    plt.xlabel('V [m/s]')
    plt.title('Aerodynamic power versus wind speed for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/P-v.png')


    ##Thrust coefficient curve
    fig=plt.figure()
    plt.plot(Vlist,Cdax_list)
    plt.grid(True)
    plt.ylabel('Cdax')
    plt.xlabel('V [m/s]')
    plt.title('Thrust coefficient versus wind speed for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/Cdax-v.png')

    ##Power coefficient curve
    fig=plt.figure()
    plt.plot(Vlist,Cp_list2)
    plt.grid(True)
    plt.ylabel('Cp')
    plt.xlabel('V [m/s]')
    plt.title('Power coefficient versus wind speed for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/Cp-v.png')   

    ##Induction factor curve
    fig=plt.figure()
    plt.plot(Vlist,a_list2)
    plt.grid(True)
    plt.ylabel('a')
    plt.xlabel('V [m/s]')
    plt.title('Induction factor versus wind speed for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/a-v.png')

    ##blade pitch angle curve
    fig=plt.figure()
    plt.plot(Vlist,theta_list)
    plt.grid(True)
    plt.ylabel('Theta [deg]')
    plt.xlabel('V [m/s]')
    plt.title('Blade pitch angle versus wind speed for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/theta-v.png')

    ##rotor angular velocity curve
    fig=plt.figure()
    plt.plot(Vlist,omr_list)
    plt.grid(True)
    plt.ylabel('Omr [rad/s]')
    plt.xlabel('V [m/s]')
    plt.title('Rotor angular velocity versus wind speed for the '+ windturbine + ' windturbine')
    fig.savefig('plots/'+windturbine+'/omr-v.png') 

    stop = timeit.default_timer()

    time = round(stop-start,1)
    
    print 'All files are saved in the specified wind turbine folder'
    print 'This folder is located at Plots/'+windturbine
    print 'It took',time,'seconds to generate the plots'
        
