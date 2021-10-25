function [beta0,x0,omr0,eps0,omg0,a0,theta,Dax0,Mbeta0,Mr0]=equi(windturbine,V)
% syntax: function [beta0,x0,omr0,eps0,omg0,a0,theta,Dax0,Mbeta0,Mr0]=equi(windturbine,V)
% Determination of the operating point of the wind turbine for known wind speed;
% this is the steady state after equilibrium between all acting forces on the wind turbine
%
%    Partial load conditions (V<=Vn): theta=thetan.
%        Note: it is not assumed that the wind turbine automatically operates at optimal tip speed ratio
%    Full load conditions (V>Vn): omr=omrn; theta such that power equals nominal power
%
% Inputs:
%    windturbine: name of file with wind turbine parameters (string)
%                 e.g.: 'LW50'
%    V: undisturbed wind speed [m/s]
% Outputs:
%    beta0: stationary flap angle [rad]
%    x0: stationary tower top displacement [m]
%    omr0: stationary rotor angular velocity [rad/s]
%    eps0: stationary torsion angle transmission [rad]
%    omg0; stationary generator angular velocity [rad/s]
%    a0: stationary induction factor [-]
%    theta: blade pitch angle [degrees]

% required parameters
[P1,P2,P3,P4]=eval(windturbine);
% rotor radius [m]
R=P2(1);
% inertia blade (with respect to flapping hinge) [kg m^2]
Jb=P2(3);
% stifness flap spring [Nm/rad]
kb=P2(4);
% stifness tower [N/m]
kt=P2(7);
% transmission ratio [-]
nu=P2(8);
% stiffness transmission [Nm/rad]
kr=P2(11);
% nominal wind speed [m/s]
Vn=P4(1);
% nominal tip speed ratio [-]
lambdan=P4(2);
% nominal blade pitch angle [degrees]
thetan=P4(3);

% stationary conditions: flap velocity and tower top velocity are equal zero
betad=0;
xd=0;

% nominal rotor angular velocity
omrn=lambdan*Vn/R;
% nominal mechanical power Pn (wind speed equal to nominal wind speed; blade pitch angle equal to
%                    nominal blade pitch angle; rotor angular velocity equal to nominal rotor angular velocity)
[Dax,Mbeta,Mr,Pn,Cdax,Cp,a]=bem(Vn,thetan,betad,omrn,xd,P1,P2,P3);

if V <= Vn
  % partial load conditions (wind speed smaller or equal nominal wind speed)
  % blade pitch angle equals nominal blade pitch angle
  theta=thetan;  
  % operating point: equilibrium between aerodynamic rotor torque and generator torque
  % Use is made of the standard Matlab routine 'fzero' to find a zero of the function 'fun_equi.m'; 'fzero' varies
  % the rotor angular velocity (in the range 5*V/R to 10*V/R; corresponding with a tip speed ratio between 5 and 10)
  % until 'fun_equi' equals (about) zero.
  warning off
  options=optimset('Display','off');
  omr0=fzero('fun_equi',[5*V/R 10*V/R],options,V,theta,P1,P2,P3);
  warning on
else
  % ful load conditions (wind speed larger than nominal wind speed)
  % rotor angular velocity equals nominal rotor angular velocity
  omr0=lambdan*Vn/R;
  % the blade pitch angle should be such that the power equals nominal power;
  % it is assumed that the blade pitch control is to zero-lift
  % Use is made of the standard Matlab routine 'fzero' to find a zero of the function 'fun_power.m'; 'fzero' varies
  % the blade pitch angle (in the range thetan to 50) until 'fun_power' equals (about) zero.
  warning off
  options=optimset('Display','off');
  theta=fzero('fun_power',[thetan 50],options,V,Pn,P1,P2,P3,P4);
  warning on  
end

% since the blade pitch angle and the stationary rotor angular velocity are determined, the stationary
% aerodynamic forces, moments and induction factor can be calculated by means of
% the blade element - momentum method (BEM)
[Dax0,Mbeta0,Mr0,P,Cdax,Cp,a0]=bem(V,theta,betad,omr0,xd,P1,P2,P3);

% equilibrium equations of the turbine: the equations of motion (see listing 'dynmod.m')
% without time dependent terms
% stationary flap angle
beta0=Mbeta0/(kb+Jb*omr0^2);
% stationary tower top displacement
x0=Dax0/kt;
% stationary torsion angle transmission
eps0=Mr0/kr;
% stationary generator angular velocity
omg0=nu*omr0;
