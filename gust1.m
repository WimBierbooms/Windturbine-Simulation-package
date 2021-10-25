function U=gust1(t)
% syntax: U=gust1(t)
% 'smooth' wind gust
%
% Output:
%    U: wind speed [m/s]; with respect to mean wind speed V
% Input:
%    t: time [s]

% gust amplitude
A=1;
% gust duration
T=12;
% starting time of gust
t0=5;

% gust
U=0.5*A*(1-cos(2*pi*(t-t0)/T));

% all values of U before or after the gust are put to zero
index=find(t<t0 | t>t0+T);
U(index)=zeros(size(index));
