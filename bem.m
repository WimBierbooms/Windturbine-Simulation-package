function [Dax,Mbeta,Mr,P,Cdax,Cp,a]=bem(V,theta,betad,omr,xd,P1,P2,P3);
% syntax: function [Dax,Mbeta,Mr,P,Cdax,Cp,a]=bem(V,theta,betad,omr,xd,P1,P2,P3);
% Determintion of the aerodynamic forces, moments and power by means of the
% blade element - momentum method (BEM); for known wind speed, pitch angle, etc.
% Simplifications:
%    - uniform flow (i.e. wind speed constant over rotor plane; no yawed flow, windshear or tower shadow)
%    - no wake rotation (i.e. no tangential induction factor)
%    - no blade tip loss factor
%    - just one annular section (the total rotor plane)
%
% Output:
%    Dax: axial force [N]
%    Mbeta: aerodynamic flap moment [Nm]
%    Mr: aerodynamic rotor torque [Nm]
%    P: aerodynamic power [W]
%    Cdax: thrust coefficient [-]
%    Cp: power coefficient [-]
%    a: induction factor [-]
% Input:
%    V: undisturbed wind speed [m/s]
%    theta: pitch angle [degrees]
%    betad: flap velocity [rad/s]
%    omr: rotor angular velocity [rad/s]
%    xd: tower top velocity [m/s]
%    P1: aerodynamic parameters
%    P2: turbine parameters
%    P3: blade geometry


% Calculation of the inductionfactor a by means of BEM:
% Cdax according to the blade element method should be equal to Cdax according to the momentum theory
% Use is made of the standard Matlab routine 'fzero' to find a zero of the function 'fun_bem.m'; 'fzero' varies
% the induction factor a (in the range -0.5 to 2) until 'fun_bem' equals (about) zero.
warning off
options=optimset('Display','off');
a=fzero('fun_bem',[-0.5 2],options,V,theta,betad,omr,xd,P1,P2,P3);
warning on  

% since the induction factor is determined, the aerodynamic forces, moments and power
% can be calculated by means of the blade element method
[Dax,Mbeta,Mr,P,Cdax,Cp]=aero2(a,V,theta,betad,omr,xd,P1,P2,P3);
