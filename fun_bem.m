function Cdaxd=fun_bem(a,V,theta,betad,omr,xd,P1,P2,P3)
% syntax: function Cdaxd=fun_bem(a,V,theta,betad,omr,xd,P1,P2,P3)
% Determination of the difference of the thrust coefficient Cdax according to
% the blade element method and the momentum theory; for known induction factor a
% This function is used by 'bem.m'
%
% Output:
%    Cdaxd: difference in thrust coefficient [-]
% Inputs:
%    a: induction factor [-]
%    V: undisturbed wind speed [m/s]
%    theta: pitch angle [degrees]
%    betad: flap velocity [rad/s]
%    omr: rotor angular velocity [rad/s]
%    xd: tower top velocity [m/s]
%    P1: aerodynamic parameters
%    P2: turbine parameters
%    P3: blade geometry

% Cdax according to blade element method
[Dax,Mbeta,Mr,P,Cdax,Cp]=aero2(a,V,theta,betad,omr,xd,P1,P2,P3);

% Cdax according to momentum theory (the total rotor plane is treated as 1 annular section)
if (a > 0.5 & a < 1.62)
  % for these values of the induction factor a the momentum theory is not valid;
  % instead an empirical relation is used
  Cdax2=1.49/(1.99-a);
else
  % momentum theory
  Cdax2=4*a*abs(1-a);
end

% difference in thrust coefficient Cdax according to
% blade element method and momentum theory
Cdaxd=Cdax-Cdax2;
