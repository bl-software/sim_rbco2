% Volume of torus and radii (R,r)
%
clc
% Physiological data [WT AQP1_KO RhAG_KO dKO]
D = [6.80 6.69 6.53 6.55]
V_torus = [47.9 49.525 51 49.75]

j = 1;

a = 2*(pi^2)
b = -(pi^2)*D(j)
c = 0
d = V_torus(j)

p = [a b c d]
%DALE 
% p =        ax^3 +            bx^2 + cx + d
%   = 2*(pi^2) * x^3 + -(pi^2) * D(j) * x^2      + V_torus(j)
%   = 2*(pi^2) * x^3 + -(pi^2) * 6.55 * x^2      + 49.75

% Sidestep - solve for D to match rxo's sims
% 0 = 2*(pi^2) * x^3 + -(pi^2) * D(j) * x^2      + V_torus(j)
% (pi^2) * D(j) * x^2 = 2*(pi^2) * x^3 + V_torus(j)
% D(j) = (2*(pi^2) * x^3 + V_torus(j)) / (pi^2) * x^2
% D = (2*(pi^2) * x^3 + V_torus) / (pi^2) * x^2
% D = (2*(pi^2) * r^3 + Vt) / (pi^2) * r^2
%
%
%
%
%
% V = ( pi r^2 ) ( 2 pi R )
% r^2 = V / ( 2 pi pi R ) 
% R =  V / ( 2 pi pi r r )
%
% D= 2*R + 2 * r
% r = ( D - 2*R ) / 2
%
% r  = ( D - 2*R ) / 2
% 2r =   D - 2*R
% 2r =   D - 2  V
%            -------
%            2 pi pi r r
%
% 2r =   D -  V
%            -------
%            pi^2  r^2 
% 
% 2pi^2r^3 - Dpi^2r^2 + 0r + V = 0
% 
% solve for r 
%                        
%
%

r = roots(p)

R = (D(j)-2*r)/2
%break
V_torus_calc   = 2*(pi^2)*R.*(r.^2)
V_torus_calc_1 = 2*(pi^2)*R(1)*(r(1)^2)
V_torus_calc_2 = 2*(pi^2)*R(2)*(r(2)^2)
V_torus_calc_3 = 2*(pi^2)*R(3)*(r(3)^2)
