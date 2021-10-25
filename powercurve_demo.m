%% power curve demo
% This is a demonstration of the powercurve1 and powercurve2 routines:
% it plots the power (P-V) curve of variable and fixed speed turbine
% resp.
%
% Note that the corresponding Matlab commands are given
% in the comment box, preceeded by >>
%
% Wim Bierbooms

%%
% We start with the variable speed turbine
% what are the inputs and outputs of the powercurve1 routine?
% use the help command:
help powercurve1

%%
% in order to call the routine we have to specify the input first:
% the values for the wind speed: from 4 to 20 m/s with steps of 0.5
%
% Note: a screen echo is suppressed by a semicolon 
V=4:0.5:20;

%%
% we can now call the powercurve1 routine
% as example we us the Lagerwey LW50 turbine
%
% Note: for ease and to avoid typing errors you can copy the command from
% the screen echo (from the help command) and paste it into the command line;
% you can edit it (replace 'windturbine' by 'LW50') and do not forget to add a semicolon
[Dax,Mbeta,Mr,P,Cdax,Cp,a,theta,omr]=powercurve1('LW50',V);
plot(V,P);shg

%%
% you can add labels and a title to the graph
xlabel('wind speed [m/s]');
ylabel('power [W]')
title('P-V curve LW50 - variable speed');

%%
% plot of the pitch angle
% (in a similar way the other outputs can be plotted)
plot(V,theta);
xlabel('wind speed [m/s]');
ylabel('pitch angle [degrees]')

%%
% Now we will deal with fixed speed stall turbines; for this purpose the
% powercurve2 routine should be used and we have to specify the rotational
% speed (rad/s)
%
% Note: as example we again use the Lagerwey LW50 turbine, so we assume
% that it is operated as a stall turbine
omr=2.4;
[Dax2,Mbeta2,Mr2,P2,Cdax2,Cp2,a2]=powercurve2('LW50',V,omr);
plot(V,P2);
xlabel('wind speed [m/s]');
ylabel('power [W]')
title('P-V curve LW50 - fixed speed');

%%
% We can draw the power curves in one graph
% Can you explain why the lines intersect at one wind speed?
plot(V,P,V,P2,'--');hold
xlabel('wind speed [m/s]');
ylabel('power [W]')
title('P-V curves LW50');
legend('variable speed','fixed speed',2);

%%
% A fixed speed turbine operates at maximum Cp at 1 wind speed only: the
% wind speed at which the nominal tip speed ratio is reached
R=25;
lambdan=7.5;
Vi=omr*R/lambdan
plot([Vi Vi],[0 max(P2)],':')
hold off

%%
% We can also compare the thrust
plot(V,Dax,V,Dax2,'--');
xlabel('wind speed [m/s]');
ylabel('axial force [N]')
legend('variable speed','fixed speed',2);

%%
% and the power coefficient
plot(V,Cp,V,Cp2,'--');
xlabel('wind speed [m/s]');
ylabel('power coefficient [-]')
legend('variable speed','fixed speed',1);

%%
% This ends the power curve demo
