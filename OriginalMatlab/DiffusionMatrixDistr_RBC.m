% Diffusion matrix for the RBC model including O2, HbO2 and Hb. 
%
% Structure of the output sparse matrices:
%
%        [ Du0  0    0  0  ]         
%   Du = [      Du1  0  0  ]
%        [       ..  ..    ]          
%        [              Dun]         
%   
%   A =  Du 
%
%  W is constructed similarly, but the matrices Duj are replaced by 
%  the vectors buj.
%
% R. Occhipinti (based on the original script by D. Calvetti & E. Somersalo, 2012)

function [A W] = DiffusionMatrixDistr_RBC(n_in,n_out,R,R_inf, ...
                 kappa_in,kappa_out,alpha)

N = n_in + n_out + 1;
A = sparse(3*N,3*N);
W = sparse(3*N,3);

% O2:

[Du0 bu0] = SingleSpeciesDiffMatDistr(n_in,n_out,R,R_inf,kappa_in(1,:), ...
    kappa_out(1,:),alpha(1));

A(1:N,1:N) = Du0;
W(1:N,1) = bu0;

% HbO2:

[Du1 bu1] = SingleSpeciesDiffMatDistr(n_in,n_out,R,R_inf,kappa_in(2,:), ...
    kappa_out(2,:),alpha(2));

% Substituting in the matrices
A(N+1:2*N,N+1:2*N) = Du1;
W(N+1:2*N,2) = bu1;

% Hb

[Du2 bu2] = SingleSpeciesDiffMatDistr(n_in,n_out,R,R_inf,kappa_in(3,:), ...
    kappa_out(3,:),alpha(3));

% Substituting in the matrices
A(2*N+1:3*N,2*N+1:3*N) = Du2;
W(2*N+1:3*N,3) = bu2;


    