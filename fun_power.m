function Pd=fun_power(theta,V,Pn,P1,P2,P3,P4)
% syntax: function Pd=fun_power(theta,V,Pn,P1,P2,P3,P4)
% Determination of difference between aerodynamic power, for known blade pitch angle, 
% and nominal power
% This function is used by 'powercurve1' and 'equi'
%
% Output:
%    Pd: difference in power [W]
% Input:
%    theta: blade pitch anlge [degrees]
%    V: undisturbed wind speed [m/s]
%    Pn: nominal mechanical power [W]
%    P1: aerodynamic parameters
%    P2: turbine parameters
%    P3: blade geometry
%    P4: nominal values

% required parameters
% rotor radius
R=P2(1);
% nominal wind speed [m/s]
Vn=P4(1);
% nominal tip speed ratio [-]
lambdan=P4(2);

% stationary conditions: flap velocity and tower top velocity are equal zero
betad=0;
xd=0;

% the rotor angular velocity is kept constant at nominal value
omr=lambdan*Vn/R;

% power according to blade element-momentum method (BEM) for known blade pitch angle
[Dax,Mbeta,Mr,P,Cdax,Cp,a]=bem(V,theta,betad,omr,xd,P1,P2,P3);

% difference in power
Pd=P-Pn;
