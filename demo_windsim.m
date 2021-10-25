function demo_windsim

K = MENU('Choose a demo','cp-lambda','power curve','BEM','cp-lambda (Matlab 6.0 version)','power curve (Matlab 6.0 version)','BEM (Matlab 6.0 version)');

if K==1
    playshow cplambda_demo
elseif K==2
    playshow powercurve_demo
elseif K==3
    playshow bem_demo
elseif K==4
    playshow cplambda_demo60
elseif K==5
    playshow powercurve_demo60
else
    playshow bem_demo60
end


