function [Cdax,Cp,a]=cplambda(windturbine,lambda,theta)
% syntax: function [Cdax,Cp,a]=cplambda(windturbine,lambda,theta)
% Determination of the dimensionless characteristics:
%    thrust coefficient versus tip speed ratio       Cdax - lambda
%    power coefficient versus tip speed ratio        Cp - lambda
%    induction factor versus tip speed ratio         a - lambda
%
% Outputs:
%    Cdax: thrust coefficient [-]
%    Cp: power coefficient [-]
%    a: induction factor [-]
% Inputs:
%    windturbine: name of file with wind turbine parameters (string)
%                 e.g.: 'LW50'
%    lambda: vector with tip speed ratios [-]
%    theta: blade pitch angle [degrees]

% required parameters
[P1,P2,P3,P4]=eval(windturbine);
% rotor radius
R=P2(1);

% stationary conditions: flap speed and tower top speed equal zero
betad=0;
xd=0;

N=length(lambda);

% calculation of the aerodynamic coefficients for each tip speed ratio by means of blade element-momentum method (BEM)
for i=1:N
   % arbitrary wind speed (Note: the dimensionless quantaties are independent of the wind speed)
   V=10;
   % the rotor angular velocity is calculated on basis of the tip speed ratio
   omr=lambda(i)*V/R;
   [Dax,Mbeta,Mr,P,Cdax(i),Cp(i),a(i)]=bem(V,theta,betad,omr,xd,P1,P2,P3);
end
