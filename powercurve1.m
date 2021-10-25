function [Dax,Mbeta,Mr,P,Cdax,Cp,a,theta,omr]=powercurve1(windturbine,V)
% syntax: function [Dax,Mbeta,Mr,P,Cdax,Cp,a,theta,omr]=powercurve1(windturbine,V)
% Determination of the characteristics of a VARIABLE SPEED REGULATED wind turbine
%    axial force versus wind speed                  Dax - V
%    aerodynamic flap moment versus wind speed      Mbeta - V
%    aerodynamic rotor torque versus wind speed     Mr - V
%    aerodynamic power versus wind speed            P - V
%    thrust coefficient versus wind speed           Cdax - V
%    power coefficient versus wind speed            Cp - V
%    induction factor versus wind speed             a - V
%    blade pitch angle versus wind speed            theta - V
%    rotor angular velocity versus wind speed       omr - V
% It is assumed that the wind turbine has an optimal lambda control, so:
%    Partial load (V<=Vn): lambda=lambdan, theta=thetan
%    Full load (V>Vn): omr=omrn; theta such that power equals nominal power
%
% Outputs:
%    Dax: axial force [N]
%    Mbeta: aerodynamic flap moment [Nm]
%    Mr: aerodynamic rotor torque [Nm]
%    P: aerodynamic power [W]
%    Cdax: thrust coefficient [-]
%    Cp: power coefficient [-]
%    a: induction factor [-]
%    theta: blade pitch angle [degrees]
%    omr: rotor angular velocity [rad/s]
% Inputs:
%    windturbine: name of file with wind turbine parameters (string)
%                 e.g.: 'LW50'
%    V: vector with wind speeds [m/s]

% required parameters
[P1,P2,P3,P4]=feval(windturbine);
% rotor radius
R=P2(1);
% transmission ratio [-]
nu=P2(8);
% nominal wind speed [m/s]
Vn=P4(1);
% nominal tip speed ratio [-]
lambdan=P4(2);
% nominal blade pitch angle [degrees]
thetan=P4(3);

% stationary conditions: flap speed and tower top speed equal zero
betad=0;
xd=0;

% nominal rotor angular velocity
omrn=lambdan*Vn/R;
% nominal (mechanical) generator angular velocity 
omgn=nu*omrn;
% nominal mechanical power Pn (wind speed equal to nominal wind speed; blade pitch angle equal to
%              nominal blade pitch angle; rotor angular velocity equal to nominal rotor angular velocity)
[Dax,Mbeta,Mr,Pn,Cdax,Cp,a]=bem(Vn,thetan,betad,omrn,xd,P1,P2,P3);

N=length(V);
% calculation of aerodynamic forces, moments etc. for each wind speed
for i=1:N
  if V(i) <= Vn
     % partial load conditions (wind speed smaller or equal nominal wind speed)
     % the tip speed ratio equals nominal tip speed ratio, so the rotor angular velocity equals:
     omr(i)=lambdan*V(i)/R;
     % the blade pitch angle equals nominal blade pitch angle
     theta(i)=thetan;
     % calculation of the aerodynamic forces, moments etc. by means of blade element-momentum method (BEM)
     [Dax(i),Mbeta(i),Mr(i),P(i),Cdax(i),Cp(i),a(i)]=bem(V(i),theta(i),betad,omr(i),xd,P1,P2,P3);
  else
     % ful load conditions (wind speed larger than nominal wind speed)
     % the rotor angular velocity is kept constant at nominal value
     omr(i)=lambdan*Vn/R;
     % the blade pitch angle should be such that the power equals nominal power;
     % it is assumed that the blade pitch control is to zero-lift
     % Use is made of the standard Matlab routine 'fzero' to find a zero of the function 'fun_power.m'; 'fzero' varies
     % the blade pitch angle (in the range thetan to 50) until 'fun_power' equals (about) zero.
     warning off
     options=optimset('Display','off');
     theta(i)=fzero('fun_power',[thetan 50],options,V(i),Pn,P1,P2,P3,P4);
     warning on  
     % since the blade pitch angle is determined, the aerodynamic forces, moments and power
     % can be calculated by means of the blade element - momentum method (BEM)
     [Dax(i),Mbeta(i),Mr(i),P(i),Cdax(i),Cp(i),a(i)]=bem(V(i),theta(i),betad,omr(i),xd,P1,P2,P3);
  end
end
