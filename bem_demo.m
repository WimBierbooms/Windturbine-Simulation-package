%% BEM demo
% This is a demonstration of Blade Element Momentum theory (BEM)
%
% Note that the corresponding Matlab commands are given
% in the comment box, preceeded by >>
%
% Wim Bierbooms
% Date: 6-5-'04

%%
% Blade Element Momentum theory is a combination of the blade-element method
% and momentum theory
%
% We start with the blade-element method; it is implemented in the Matlab
% routine aero
help aero

%%
% As example we use the Lagerwey LW50 turbine: first all the parameters of
% this turbine are put in the parameter vectors P1, P2, P3 and P4
%
% The aerodynamic forces depend on the operational conditions; for this
% demo we consider the following mean wind speed (m/s), rotational speed
% (rad/s) and pitch angle (degrees)
[P1,P2,P3,P4]=LW50;
V=7
omr=2
theta=0

%%
% For values of the induction factor a in between 0 and 1 the thrust
% coefficient Cdax is calculated
for i=1:100,a(i)=i/100;[Dax,Mbeta,Mr,P,Cdax1(i),Cp]=aero(a(i),V,theta,0,omr,0,P1,P2,P3);end
plot(a,Cdax1);
xlabel('induction factor a (-)');
ylabel('thrust coefficient (-)');

%%
% Next momentum theory is applied; the relation between the thrust
% coefficient Cdax and the induction factor a is given by:
Cdax2=4*a.*(1-a);
plot(a,Cdax2);
xlabel('induction factor a (-)');
ylabel('thrust coefficient (-)');

%%
% The relations between the thrust coefficient Cdax and the induction
% factor a according to the blade-element method and momentum theory can be
% shown in one graph
plot(a,Cdax1,a,Cdax2,'--');hold on;
xlabel('induction factor a (-)');
ylabel('thrust coefficient (-)');
legend('blade element theory','momentum theory');

%%
% The essence of BEM is the calculation of the induction factor a by
% equating the expressions according to the blade-element method and
% momentum theory (i.e. the intersection of the 2 lines
%
% The induction factor can be calculated in an iterative way:
% We start with some initial guess, say 0.8 and calculate the corresponding
% thrust coefficient according to the blade-element method, i.e. this point
% lies on the blue line and is indicated by a red cross
a0=0.8
[Dax,Mbeta,Mr,P,Cdax0,Cp]=aero(a0,V,theta,0,omr,0,P1,P2,P3);
plot(a0,Cdax0,'r*');

%%
% Next a new induction factor is calculated from the value of the trust
% coefficient according to momentum theory, i.e. this point lies on the
% green line and is indicated by a red circle
%
% Note: for this purpose we have to rewrite the (quadratic) expression
% according to momentum theory
plot(a0,Cdax0,'m*');
a0=0.5-0.5*sqrt(1-Cdax0)
plot(a0,Cdax0,'ro');

%%
% We can repeat this untill convergence is reached; the new points are
% indicated in red, the older ones in magenta
%
% NOTE: USE SPACE BAR TO SEE THE NEXT POINTS
plot(a0,Cdax0,'mo');
for i=1:6
   [Dax,Mbeta,Mr,P,Cdax0,Cp]=aero(a0,V,theta,0,omr,0,P1,P2,P3);
   plot(a0,Cdax0,'r*');pause;plot(a0,Cdax0,'m*');
   a0=0.5-0.5*sqrt(1-Cdax0)
   plot(a0,Cdax0,'ro');pause;plot(a0,Cdax0,'mo');
end

%%
% The final answer is:
a0

%%
% It is also possible to find the intersection by use of the standard
% Matlab routine 'fzero'.
% This is implemented in the routine 'bem' (in combination with 'fun_bem')
[Dax,Mbeta,Mr,P,Cdax,Cp,a]=bem(V,theta,0,omr,0,P1,P2,P3);
a

%%
% This ends the BEM demo
