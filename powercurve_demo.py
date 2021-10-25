from powercurve1 import powercurve1
from powercurve2 import powercurve2
import numpy as np
import matplotlib.pyplot as plt
wm = plt.get_current_fig_manager() 
wm.window.attributes('-topmost', 1)
wm.window.attributes('-topmost', 0)

## written by Dennis van Dommelen, 2014

def powercurve_demo():
    print 'This is a demonstration of the powercurve1 and powercurve2 routines:'
    print 'it plots the power (P-V) curve of variable and fixed speed turbine resp. '
    print 'Note that some of the corresponding Python commands are given'
    print 'Proceed by pressing enter'
    print ''
    print 'Dennis van Dommelen'
    print 'Date: 11-12-13'

    raw_input("_____________________________________________________________ \n")
    print 'We start with the variable speed turbine'
    print 'What are the inputs of the powercurve1 routine? Use the help command:\'help(powercurve1)\''
    help(powercurve1)

    raw_input("_____________________________________________________________ \n")
    print 'In order to call the routine we have to specify the input first:'
    print 'the values for the wind speed: from 4 to 20 m/s with steps of 0.5'
    print '_____________________________________________________________'
    print 'V=np.arange(4,20.5,0.5)'
    print '_____________________________________________________________'
    V=np.arange(4,20.5,0.5)

    raw_input("_____________________________________________________________ \n")
    print 'We can now call the powercurve1 routine'
    print 'Choose one of the following wind turbines:'
    windturbine = raw_input("Type the wind turbine you would like to analyse, e.g. V90, S88, NREL_5MW: ")
    print 'Note: for ease and to avoid typing errors you can copy the command from'
    print '_____________________________________________________________'
    print '[Dax,Mbeta,Mr,P,Cdax,Cp,a,theta,omr]=powercurve1(windturbine,V)'
    print '_____________________________________________________________'
    print 'Now the plot can be created using the standard plt.plot(x,y) and plt.show() command, it may take a moment for the plot to appear so please wait'
    [Dax,Mbeta,Mr,P,Cdax,Cp,a,theta,omr]=powercurve1(windturbine,V)
    plt.plot(V,P)
    plt.show()
    print'_____________________________________________________________\n'

    print 'You can add labels and a title to the graph with the plt.xlabel() plt.ylabel() plt.title() commands' 
    plt.plot(V,P)
    plt.xlabel('wind speed [m/s]')
    plt.ylabel('power [W]')
    plt.title('P-V curve'+windturbine+' - variable speed')
    plt.show()
    print'_____________________________________________________________\n'

    print 'Plot of the pitch angle (in a similar way the other outputs can be plotted)'
    plt.plot(V,theta)
    plt.xlabel('wind speed [m/s]')
    plt.ylabel('pitch angle [degrees]')
    plt.show()
    print'_____________________________________________________________\n'

    raw_input("_____________________________________________________________ \n")
    print 'Now we will deal with fixed speed stall turbines; for this purpose the powercurve2 routine should be used and we have to specify the rotational speed (rad/s) \n'

    print 'Note: as example we again use the wind turbine you chose, so we assume that it is operated as a stall turbine, therefor omr=2.4'
    omr=2.4
    print 'It may take a moment for the plot to appear so please wait'
    [Dax2,Mbeta2,Mr2,P2,Cdax2,Cp2,a2]=powercurve2(windturbine,V,omr)
    
    plt.plot(V,P2)
    plt.xlabel('wind speed [m/s]')
    plt.ylabel('power [W]')
    plt.title('P-V curve '+windturbine+' - fixed speed')
    plt.show()
    print'_____________________________________________________________\n'

    raw_input("_____________________________________________________________ \n")
    print 'We can draw the power curves in one graph'
    print 'Can you explain why the lines intersect at one wind speed?'
    plt.plot(V,P,V,P2,'--')
    plt.xlabel('wind speed [m/s]')
    plt.ylabel('power [W]')
    plt.title('P-V curves '+windturbine+'')
    plt.legend(('variable speed','fixed speed'),2)
    plt.show()
    print'_____________________________________________________________\n'

    raw_input("_____________________________________________________________ \n")
    print 'A fixed speed turbine operates at maximum Cp at 1 wind speed only: the wind speed at which the nominal tip speed ratio is reached'
    R=25;
    lambdan=7.5;
    Vi=omr*R/lambdan
    plt.plot(V,P,V,P2,'--')
    plt.xlabel('wind speed [m/s]')
    plt.ylabel('power [W]')
    plt.title('P-V curves '+windturbine+'')
    plt.legend(('variable speed','fixed speed'),2)
    plt.plot([Vi,Vi],[0,max(P2)],':')
    plt.show()
    print'_____________________________________________________________\n'
    

    print 'We can also compare the thrust'
    plt.plot(V,Dax,V,Dax2,'--')
    plt.xlabel('wind speed [m/s]')
    plt.ylabel('axial force [N]')
    plt.legend(('variable speed','fixed speed'),2)
    plt.show()
    print'_____________________________________________________________\n'


    print 'And the power coefficient'
    plt.plot(V,Cp,V,Cp2,'--')
    plt.xlabel('wind speed [m/s]')
    plt.ylabel('power coefficient [-]')
    plt.legend(('variable speed','fixed speed'),1)
    plt.show()
    
    print 'This ends the power curve demo'

