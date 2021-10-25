function [sys_tf,sys_ss]=transfer(windturbine,V0)
% syntax: function [sys_tf,sys_ss]=transfer(windturbine,V0)
% Determination of the transfer function of the wind turbine
%
% Inputs:
%    windturbine: name of file with wind turbine parameters (string)
%                 e.g.: 'LW50'
%    V0: undisturbed wind velocity [m/s]
% Outputs:
%    sys_tf: the transfer function H(s) for all wind turbine inputs to all wind turbine outputs
%                   NUM(s)
%           H(s) = --------
%                   DEN(s)
%    inputs of wind turbine:
%      1) blade pitch angle theta [graden]
%      2) undisturbed wind speed V [m/s]
%    outputs of wind turbine:
%      1) axial force Dax [N]
%      2) aerodynamic flap moment Mbeta [Nm]
%      3) aerodynamic rotor torque Mr [Nm]
%      4) generator power Pg [W]
%      5) blade pitch angle theta [degrees]
%      6) undisturbed wind speed V [m/s]


% constants with respect to the linearisation of the equations of motion
% minimum variation
mindelta=1e-7;
% relative variation
reldelta=1e-2;

% required parameters
[P1,P2,P3,P4]=eval(windturbine);
% rotor radius
R=P2(1);
% transmission ratio [-]
nu=P2(8);
% nominal generator power [W]
Pn=P2(14);
% nominal generator shaft angular velocity [rad/s]
omgn=P2(15);
% nominal wind speed [m/s]
Vn=P4(1);
% nominal tip speed ratio [-]
lambdan=P4(2);
% nominal blade pitch angle [degrees]
thetan=P4(3);

% stationary conditions: flap speed, tower top speed and torsion speed transmission equal zero
betad=0;
xd=0;
epsd=0;
% nominal conditions
% nominal rotor angular velocity
omrn=lambdan*Vn/R;

% determination operating point (equilibrium state) of wind turbine for known V0
[beta,x,omr,eps,omg,a,theta,Dax,Mbeta,Mr]=equi(windturbine,V0);
% generator power
[Mg,Pg,Ef,I1,V1,I2,eta]=gener(omg,(omg/omgn)^3*Pn,P2,690);

% initial state (stationary)
X0=[beta;betad;x;xd;omr;eps;epsd];
U0=[theta;V0];
Y0=[Dax;Mbeta;Mr;Pg;theta;V0];

% numerical linearisation of the equations of motion (given in 'dynmod.m') into state space format:
%    XD = A X + B U
%     Y = C X + D U
%    with X states of the wind turbine: [beta;betad;x;xd;omr;eps;epsd]
%        XD time derivative of X
%        Y outputs of wind turbine: [Dax;Mbeta;Mr;Pg;theta;V]
%        U inputs of wind turbine: [theta;V]
% number of states
NX=length(X0);
% number of outputs
NY=length(Y0);
A=zeros(NX,NX);
C=zeros(NY,NX);
% variation around state X0
for i=1:NX
   delta=zeros(size(X0));
   delta(i)=max(reldelta*X0(i),mindelta);
   X1=X0+delta;
   [XD1,Y1]=dynmod(X1,U0,a,P1,P2,P3);
   X2=X0-delta;
   [XD2,Y2]=dynmod(X2,U0,a,P1,P2,P3);
   A(:,i)=(XD1-XD2)./(2*delta(i));
   C(:,i)=(Y1-Y2)./(2*delta(i));
end

% number of inputs
NU=length(U0);
B=zeros(NX,NU);
D=zeros(NY,NU);
% variation around input U0
for i=1:NU
   delta=zeros(size(U0));
   delta(i)=max(reldelta*U0(i),mindelta);
   U1=U0+delta;
   [XD1,Y1]=dynmod(X0,U1,a,P1,P2,P3);
   U2=U0-delta;
   [XD2,Y2]=dynmod(X0,U2,a,P1,P2,P3);
   B(:,i)=(XD1-XD2)./(2*delta(i));
   D(:,i)=(Y1-Y2)./(2*delta(i));
end

% conversion from state space to transfer function
states={'flap angle [rad]';'flap angular velocity [rad/s]';'tower top displacement [m]';'tower top speed [m/s]'; ...
 'rotor angular velocity [rad/s]';'torsion angle transmission [rad]';'torsion angular velocity transmission [rad/s]'};
inputs={'blade pitch angle [degrees]';'undisturbed wind speed [m/s]'};
outputs={'Dax [N]';'Mbeta [Nm]';'Mr [Nm]';'Pg [W]';'theta [degrees]';'V [m/s]'};
sys_ss=ss(A,B,C,D,'statename',states,'inputname',inputs,'outputname',outputs);
sys_tf=tf(sys_ss);
