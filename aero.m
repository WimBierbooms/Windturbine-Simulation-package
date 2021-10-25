function [Dax,Mbeta,Mr,P,Cdax,Cp]=aero(a,V,theta,betad,omr,xd,P1,P2,P3)
% syntax: function [Dax,Mbeta,Mr,P,Cdax,Cp]=aero(a,V,theta,betad,omr,xd,P1,P2,P3);
% Determination of the aerodynamic forces, moments and power by means of
% the blade element method; for known mean wind speed, induction factor etc.
% Simplifications:
%    - uniform flow (i.e. wind speed constant over rotor plane; no yawed flow, windshear or tower shadow)
%    - no wake rotation (i.e. no tangential induction factor)
%    - no blade tip loss factor
%
% Output:
%    Dax: axial force [N]
%    Mbeta: aerodynamic flap moment [Nm]
%    Mr: aerodynamic rotor torque [Nm]
%    P: aerodynamic power [W]
%    Cdax: thrust coefficient [-]
%    Cp: power coefficient [-]
% Input:
%    a: induction factor [-]
%    V: undisturbed wind speed [m/s]
%    theta: pitch angle [degrees]
%    betad: flap velocity [rad/s]
%    omr: rotor angular velocity [rad/s]
%    xd: tower top velocity [m/s]
%    P1: aerodynamic parameters
%    P2: turbine parameters
%    P3: blade geometry

% air density [kg/m3]
rho=P1(1);
% power loss factor; correction factor for the above mentioned simplifications [-]
kp=P1(2);
% rotor radius [m]
R=P2(1);
% number of blades [-]
Nb=P2(2);
% number of blade elements [-]
Ns=length(P3)-1;
% radial position blade elements [m]
r=P3(1,:);
% chord blade elements [m]
c=P3(2,:);
% twist blade elements [degrees];
thetat=P3(3,:);

% calculation of aerodynamic forces/moments for each blade section
for i=1:Ns
   % use mean value for the radial position of blade element
   ri=(r(i)+r(i+1))/2;
   % idem chord
   ci=(c(i)+c(i+1))/2;
   % idem twist
   thetati=(thetat(i)+thetat(i+1))/2;
   % length blade element
   dr=r(i+1)-r(i);
   % perpendicular velocity component
   Vp=V*(1-a)-betad*ri-xd;
   % tangential velocity component
   Vt=omr*ri;
   % resultant velocity
   W=sqrt(Vp^2+Vt^2);
   % angle of inflow
   phi=atan(Vp/Vt);
   % angle of attack (in degrees)
   alpha=180/pi*phi-(theta+thetati);
   % lift coefficient (from function 'lift.m')
   Cl=lift(alpha);
   % lift force blade element
   dL=Cl*0.5*rho*W^2*ci*dr;
   % drag coefficient (from function 'drag.m')
   Cd=drag(alpha);
   % drag force blade element
   dD=Cd*0.5*rho*W^2*ci*dr;
   % contribution to axial force
   dDax(i)=Nb*(dL*cos(phi)+dD*sin(phi));
   % contribution to aerodynamic flap moment
   dMbeta(i)=ri*(dL*cos(phi)+dD*sin(phi));
   % contribution to aerodynamic rotor torque
   dMr(i)=Nb*ri*(kp*dL*sin(phi)-dD*cos(phi));
end

% total forces and moments; sommation over all blade elements
Dax=sum(dDax);
Mbeta=sum(dMbeta);
Mr=sum(dMr);

% thrust coefficient
Cdax=Dax/(0.5*rho*pi*R^2*V^2);

% aerodynamic power
P=omr*Mr;

% power coefficient
Cp=P/(0.5*rho*pi*R^2*V^3);
