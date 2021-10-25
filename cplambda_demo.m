%% cp-lambda demo
% This is a demonstration of the cplambda routine:
% it plots a cp-lambda curve
%
% Note that the corresponding Matlab commands are given
% in the comment box, preceeded by >>
%
% Wim Bierbooms
% Date: 4-5-'04

%%
% what are the inputs and outputs of this routine?
% use the help command:
help cplambda

%%
% in order to call the routine we have to specify the inputs first:
% the pitch angle and the values for lambda: from 3 to 14 with steps of 0.1
%
% Note: a screen echo is suppressed by a semicolon 
theta=0
lambda=3:0.1:14;

%%
% we can now call the cplambda routine
% as example we us the Lagerwey LW50 turbine
%
% Note: for ease and to avoid typing errors you can copy the command from
% the screen echo (from the help command) and paste it into the command line;
% you can edit it (replace 'windturbine' by 'LW50') and do not forget to add a semicolon
[Cdax,Cp,a]=cplambda('LW50',lambda,theta);
plot(lambda,Cp);shg

%%
% you can add labels and a title to the graph
xlabel('tip speed ratio [-]');
ylabel('power coefficient [-]')
title('Cp-lambda curve LW50');

%%
% you can run cplambda again for another pitch angle
%
% Note: use other variable names, otherwise the results will be overwritten
theta2=2;
[Cdax2,Cp2,a2]=cplambda('LW50',lambda,theta2);

%%
% and plot them in one graph
plot(lambda,Cp,lambda,Cp2,'--');

%%
% you can zoom in by using the tools in the graph window or by using the
% axis command, specifying the minimum and maximum value of the x- and
% y-axis
axis([5 8 0.2 0.6])

%%
% you can add a legend
legend('theta=0','theta=2');

%%
% plot of the induction factor
% (in a similar way the thrust coefficient can be plotted)
plot(lambda,a,lambda,a2,'--');
xlabel('tip speed ratio [-]');
ylabel('induction factor [-]')
legend('theta=0','theta=2');

%%
% This ends the cp-lambda demo
