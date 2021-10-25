from cplambda import cplambda
import numpy as np
import matplotlib.pyplot as plt
wm = plt.get_current_fig_manager() 
wm.window.attributes('-topmost', 1)
wm.window.attributes('-topmost', 0)

## written by Dennis van Dommelen, 2014

def cplambda_demo():
    
    print 'This is a demonstration of the cplambda routine, it plots a cp-lambda curve'
    print ''
    print 'Note that some of the corresponding Python commands are given'
    print 'Proceed by pressing enter'
    print ''
    print 'Dennis van Dommelen'
    print 'Date: 11-12-13'

    raw_input("_____________________________________________________________ \n")
    print 'What are the inputs of this routine?'
    print 'Use the help command: \'help(cplambda)\''
    help(cplambda)

    raw_input("_____________________________________________________________ \n")
    print 'In order to call the routine we have to specify the inputs first:'
    print 'The pitch angle and the values for lambda: from 3 to 14 with steps of 0.1'
    print ''
    print 'Note: a screen echo is suppressed by a semicolon '
    print '_____________________________________________________________'
    print 'theta=0'
    print '_____________________________________________________________'
    theta=0
    print 'A list consisting of values for lambda is beging created:'
    print '_____________________________________________________________'
    print 'lambdalist=np.arange(3,14.1,0.1)'
    print '_____________________________________________________________'
    lambdalist=np.arange(3,14.1,0.1)

    raw_input("_____________________________________________________________ \n")
    print 'We can now call the cplambda routine'
    print ''
    print 'Choose one of the following wind turbines:'
    windturbine = raw_input("Type the wind turbine you would like to analyse, e.g. V90, S88, NREL_5MW: ")
    print '_____________________________________________________________'
    print '[Cdax,Cp,a]=cplambda(windturbine,lambdalist,theta)'
    print '_____________________________________________________________'
    print 'Now the plot can be created using the standard plt.plot(x,y) and plt.show() command, it may take a moment for the plot to appear so please wait'
    [Cdax,Cp,a]=cplambda(windturbine,lambdalist,theta)
    
    
    plt.plot(lambdalist,Cp)
    plt.show()
    print'_____________________________________________________________\n'

    print 'You can add labels and a title to the graph with the plt.xlabel() plt.ylabel() plt.title() commands'
    
    plt.plot(lambdalist,Cp)
    plt.xlabel('tip speed ratio [-]')
    plt.ylabel('power coefficient [-]')
    plt.title('Cp-lambda curve LW50')
    plt.show()
    print'_____________________________________________________________\n'

    print 'You can run cplambda again for another pitch angle'
    print ''
    print 'Note: use other variable names, otherwise the results will be overwritten'
    print '_____________________________________________________________'
    print 'Set theta2=2.'
    theta2=2.
    print '[Cdax2,Cp2,a2]=cplambda(windturbine,lambdalist,theta2)'
    print '_____________________________________________________________'
    [Cdax2,Cp2,a2]=cplambda(windturbine,lambdalist,theta2)

    raw_input("_____________________________________________________________ \n")
    print 'And plot them in one graph'
    plt.plot(lambdalist,Cp,lambdalist,Cp2,'--')
    plt.show()
    print'_____________________________________________________________\n'

    print 'You can zoom in by using the tools in the graph window or by using the plt.axis() command, specifying the minimum and maximum value of the x- and y-axis'
    plt.plot(lambdalist,Cp,lambdalist,Cp2,'--')
    plt.axis([5, 8, 0.2, 0.6])
    plt.show()
    print'_____________________________________________________________\n'

    print 'You can add a legend with the plt.legend command'
    plt.plot(lambdalist,Cp,lambdalist,Cp2,'--')
    plt.legend(('theta=0','theta=2'))
    plt.show()
    print'_____________________________________________________________\n'

    
    print 'Plot of the induction factor (in a similar way the thrust coefficient can be plotted)'
    plt.plot(lambdalist,a,lambdalist,a2,'--')
    plt.xlabel('tip speed ratio [-]')
    plt.ylabel('induction factor [-]')
    plt.legend(('theta=0','theta=2'))
    plt.show()
    print'_____________________________________________________________\n'

    
    print 'This ends the cp-lambda demo'

