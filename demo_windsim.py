from cplambda_demo import cplambda_demo
from powercurve_demo import powercurve_demo
from BEM_demo import BEM_demo

## written by Dennis van Dommelen, 2014

menu = {}
menu['1']="cp-lambda" 
menu['2']="power curve"
menu['3']="BEM"
menu['4']="exit demo"
while True: 
    options=menu.keys()
    options.sort()
    print 'Choose a demo: \n'
    for entry in options: 
      print entry, menu[entry]

    selection=raw_input("Please Select: ") 
    if selection =='1': 
        cplambda_demo()    
    elif selection == '2': 
        powercurve_demo() 
    elif selection == '3':
        BEM_demo()
    elif selection == '4':
        break
      
    else: 
      print "Unknown Option Selected!" 
