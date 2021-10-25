function [Mg,Pg,Ef,I1,V1,I2,eta]=gener(omg,Pref,P2,V2)
% syntax: function [Mg,Pg,Ef,I1,V1,I2,eta]=gener(omg,Pref,P2,V2)
% Torque-rpm characteristics of a synchronous generator with AC/DC/AC converter
%
% Output:
%    Mg: generator torque [Nm]
%    Pg: generator power [W]
%    Ef: field induced voltage [V]
%    I1: stator current [A]
%    V1: terminal voltage [V]
%    I2: grid current [A]
%    eta: efficiency generator [-]
% Inputs:
%    omg: generator shaft angular velocity [rad/s]
%    Pref: reference power (setpoint) [W]
%    P2: turbine parameters
%    V2: grid (line-to-line) voltage [V]

% nominal line-to-line voltage of generator (at terminals) [V]
VLLn=P2(13);
% nominal phase voltage of generator [V]
V1n=VLLn/sqrt(3);
% nominal generator power [W]
Pn=P2(14);
% nominal generator shaft angular velocity [rad/s]
omgn=P2(15);
% field current generator [A]
If=P2(16);
% number of pole pairs [-]
p=P2(17);

% nominal electrical angular velocity [rad/s]
omeln=p*omgn;
% per unit (pu) values
Rs_pu=0.02;
Xs_pu=1.1;
Xm_pu=70;
% conversion to actual values
% stator resistance
Rs=Rs_pu*3*V1n^2/Pn;
% stator reactance
Xs=Xs_pu*3*V1n^2/Pn;
% stator induction
Ls=Xs/omeln;
% mutual rotor-stator reactance
Xm=Xm_pu*3*V1n^2/Pn;
% mutual rotor-stator inductance
M=Xm/omeln;

% electrical angular velocity [rad/s]
omel=p*omg;

Ifmin=sqrt(4*Pref.*(Rs+sqrt(Rs^2+omel.^2*Ls^2))./(3*omel.^2*M^2));
if If < Ifmin error('field current too small');end

% field induced voltage
Ef=M/sqrt(2)*omel*If;

% Combinations of the requirements:
% 1) Phasor diagram (=Kirchhoffs voltage law) (assumption: by means of power electronics cos phi=1 is realised at the generator terminals):
%    (V1+I1*Rs)^2+(omel*Ls*I1)^2=Ef^2
% 2) Electrical power should equal the set point: 3*V1*I1=P
% Elemination of V1 from these equations leads to a quadratic equation in  I^2: 
% a*Isq^2+b*Isq+c=0 with:
a=Rs^2+omel.^2*Ls^2;
b=2*Rs*Pref./3-Ef.^2;
c=Pref.^(2)/9;
Isq=(-b-sqrt(b.^2-4.*a.*c))./(2*a);
% stator current
I1=sqrt(Isq);
% terminal voltage
V1=sqrt(Ef.^2-omel.^2.*Ls^2.*I1.^2)-I1.*Rs;

% electrical generator power
Pg=3*V1.*I1;

% mechanical power: electrical power plus losses
Pmech=Pg+3*I1.^2*Rs;

% generator torque
Mg=Pmech./omg;

% efficiency power electronic converter
eta_conv=0.98;
% efficiency generator
eta_gen=Pg/Pmech;
% efficiency generator plus power electronic converter
eta=eta_gen*eta_conv;

% grid side of converter (assumption: by means of power elektronics cos phi=1 is realised)
Pgrid=eta_conv*Pg;
I2=Pgrid/(sqrt(3)*V2);
