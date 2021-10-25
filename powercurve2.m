function [Dax,Mbeta,Mr,P,Cdax,Cp,a]=powercurve2(windturbine,V,omr)
% syntax: [Dax,Mbeta,Mr,P,Cdax,Cp,a]=powercurve2(windturbine,V,omr)
% Determination of the characteristics of a CONSTANT SPEED wind turbine
%    axial force versus wind speed                  Dax - V
%    aerodynamic flap moment versus wind speed      Mbeta - V
%    aerodynamic rotor torque versus wind speed     Mr - V
%    aerodynamic power versus wind speed            P - V
%    thrust coefficient versus wind speed           Cdax - V
%    power coefficient versus wind speed            Cp - V
%    induction factor versus wind speed             a - V
%
% Outputs:
%    Dax: axial force [N]
%    Mbeta: aerodynamic flap moment [Nm]
%    Mr: aerodynamic rotor torque [Nm]
%    P: aerodynamic power [W]
%    Cdax: thrust coefficient [-]
%    Cp: power coefficient [-]
%    a: induction factor [-]
% Inputs:
%    windturbine: name of file with wind turbine parameters (string)
%                 e.g.: 'LW50'
%    V: vector with wind speeds [m/s]
%    omr: rotor angular velocity [rad/s]

% required parameters
[P1,P2,P3,P4]=feval(windturbine);
% nominal blade pitch angle [degrees]
thetan=P4(3);

% stationary conditions: flap speed and tower top speed equal zero
betad=0;
xd=0;

N=length(V);

% the blade pitch angle equals nominal blade pitch angle
theta=thetan;

% calculation of the aerodynamic forces, moments etc., for each wind speed,
% by means of blade element-momentum method (BEM)
for i=1:N
   [Dax(i),Mbeta(i),Mr(i),P(i),Cdax(i),Cp(i),a(i)]=bem(V(i),theta,betad,omr,xd,P1,P2,P3);
end
