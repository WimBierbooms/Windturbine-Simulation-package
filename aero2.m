function [Dax,Mbeta,Mr,P,Cdax,Cp]=aero2(a,V,theta,betad,omr,xd,P1,P2,P3)
% syntax: function [Dax,Mbeta,Mr,P,Cdax,Cp]=aero2(a,V,theta,betad,omr,xd,P1,P2,P3);
% 'Vector version' of the function 'aero.m'; vector calculations are in Matlab much faster than for-loops
% See the listing of 'aero.m' for comments

rho=P1(1);
kp=P1(2);
R=P2(1);
Nb=P2(2);
Ns=length(P3)-1;
r=P3(1,:);
c=P3(2,:);
thetat=P3(3,:);

ri=(r(1:Ns)+r(2:Ns+1))/2;
ci=(c(1:Ns)+c(2:Ns+1))/2;
thetati=(thetat(1:Ns)+thetat(2:Ns+1))/2;
dr=r(2:Ns+1)-r(1:Ns);
Vp=V*(1-a).*ones(1,Ns)-betad.*ri-xd.*ones(1,Ns);
Vt=omr*ri;
W=sqrt(Vp.^2+Vt.^2);
phi=atan(Vp./Vt);
alpha=180/pi.*phi-(theta.*ones(1,Ns)+thetati);

Cl=lift(alpha);
dL=Cl.*0.5*rho.*W.^2.*ci.*dr;
Cd=drag(alpha);
dD=Cd.*0.5*rho.*W.^2.*ci.*dr;
dDax=Nb*(dL.*cos(phi)+dD.*sin(phi));
dMbeta=ri.*(dL.*cos(phi)+dD.*sin(phi));
dMr=Nb*ri.*(kp.*dL.*sin(phi)-dD.*cos(phi));

Dax=sum(dDax);
Mbeta=sum(dMbeta);
Mr=sum(dMr);

Cdax=Dax/(0.5*rho*pi*R^2*V^2);
P=omr*Mr;
Cp=P/(0.5*rho*pi*R^2*V^3);
