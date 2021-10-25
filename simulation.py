import control.matlab as cm
import matplotlib.pyplot as plt
import timeit
from transfer import transfer
from gust2 import gust2
from gust1 import gust1
from powercurve1 import powercurve1
wm = plt.get_current_fig_manager() 
wm.window.attributes('-topmost', 1)
wm.window.attributes('-topmost', 0)

## written by Dennis van Dommelen, 2014

def simulation(windturbine,V,gust=0,time=100,flap=False,tower=False,rotor=False,torsion=False):
    ## Inputs:
    ##
    ##      windturbine:    the string of the wind turbine for which the simulation has to be done
    ##      V:              Undisturbed wind speed
    ##      gust:           choose 1 for gust 1, choose 2 for gust 2, otherwise a step input is used
    ##                  gust 1: smooth wind gust which starts after 5 seconds and amplitude 1
    ##                  gust 2: wind gust with the shape of a sine; the frequency equals the rotor angular velocity (1P)
    ##      time:           the time of the simulation in seconds, standard it is 100 seconds
        
    ##      flap:           if True the flap angle and the flap angular velocity are plotted
    ##      tower:          if True the tower top displacement and velocity are plotted
    ##      rotor:          if True the rotor angular velocity is plotted
    ##      torsion:        if True the torsion angle transmission and the torsion angular velocity transmission are plotted
    ## You can decide which plots has to be generated, if for example you would like to know the V90's tower response to a gust of type 1:
    ## use the following command: simulation('V90',1,tower=True)
    

    ## start of the runtime
    start = timeit.default_timer()

    ## required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ## rotor radius
    R=P2[0]
    ## nominal wind speed [m/s]
    Vn=P4[0]
    ## nominal tip speed ratio [-]
    lambdan=P4[1]


    
    
    ##Select the system which is used and use the output of the transfer function
    sys=transfer(windturbine,V)

    #Generation of lists for time and wind speed
    t1=[]
    U=[]

    ##The time the program simulates devided by 100+1.
    for i in range(time*100+1):
        t1.append(i/100.)
        
    ##Change in wind speed due to a gust (gust1 and gust2) or a step input (append(1))
    for i in range(len(t1)):
        if gust == 1:
            U.append(gust1(t1[i]))
        elif gust == 2:
            ##calculation of omr
            if V <= Vn:
                 ## partial load conditions (wind speed smaller or equal nominal wind speed)
                 ## the tip speed ratio equals nominal tip speed ratio, so the rotor angular velocity equals:
                 omr=lambdan*V/R
            else:
                 ## full load conditions (wind speed larger than nominal wind speed)
                 ## the rotor angular velocity is kept constant at nominal value
                 omr=lambdan*Vn/R
            U.append(gust2(t1[i],omr))    
        else:
            U.append(1.0)

    #Generate a list with 0s with the same length as t1 and U
    input1= [0]*len(t1)

    ##Generation of the input list, consisting of the 0s and the changes in wind speed
    input_list=[]
    for i in range(len(U)):
        input_list.append([input1[i],U[i]])


    ##The simulation of the dynamic response
    [y,t,x]=cm.lsim(sys,input_list,t1)

   
    ##Generation of empty lists for the outputs
    flapangle = []
    flapvelo = []
    towertopdis = []
    towertopspeed = []
    rotorangvelo = []
    torangtran = []
    torangvelo = []

    ##Creating a complete list for all outputs
    names = []

    ##The different outputs strings and their units are put in another list
    states=[]


    if flap:
        names.append(flapangle)
        names.append(flapvelo)
        states.append('flap angle [rad]')
        states.append('flap angular velocity [rad/s]')
    if tower:
        names.append(towertopdis)
        names.append(towertopspeed)
        states.append('tower top displacement [m]')
        states.append('tower top speed [m/s]')
    if rotor:
        names.append(rotorangvelo)
        states.append('rotor angular velocity [rad/s]')
    if torsion:
        names.append(torangtran)
        names.append(torangvelo)
        states.append('torsion angle transmission [rad]')
        states.append('torsion angular velocity transmission [rad/s]')
        
    ##Different colors for each plot
    colors = ['b','g','r','c','m','y','b']

    ##Adding the values of the simulation to each different list
    for i in range(len(x)):
        flapangle.append(x[i][0])
        flapvelo.append(x[i][1])
        towertopdis.append(x[i][2])
        towertopspeed.append(x[i][3])
        rotorangvelo.append(x[i][4])
        torangtran.append(x[i][5])
        torangvelo.append(x[i][6])

    ##end of runtime
    stop = timeit.default_timer()
    
    ##The plotting command
    for i in range(len(names)):
            if len(names)>3:
                plt.subplot(len(names)/2+1,2,i+1)
                plt.plot(t,names[i],colors[i])
                plt.ylabel(states[i])
            else:
                plt.subplot(len(names)/2+1,1,i+1)
                plt.plot(t,names[i],colors[i])
                plt.ylabel(states[i])
    plt.show()            

    ##Printing the time needed to create the plots
    print round(stop-start,1),'s'



