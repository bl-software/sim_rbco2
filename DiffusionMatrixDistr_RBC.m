% Diffusion matrix for the RBC model including O2, HbO2 and Hb. 
%
% (SHOULD BE OK)
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
% R. Occhipinti

function [A W] = DiffusionMatrixDistr_RBC(n_in,n_out,R,R_inf, ...
                 kappa_in,kappa_out,alpha)

fprintf('*    In DiffusionMatrixDistr_RBC.m *\n')
N = n_in + n_out + 1;
A = sparse(3*N,3*N);
W = sparse(3*N,3);

% O2:

[Du0 bu0] = SingleSpeciesDiffMatDistr_RBC(n_in,n_out,R,R_inf,kappa_in(1,:), ...
    kappa_out(1,:),alpha(1));

A(1:N,1:N) = Du0;
W(1:N,1) = bu0;

fprintf('*    In DiffusionMatrixDistr_RBC.m  O2 DONE *\n')
% HbO2:

[Du1 bu1] = SingleSpeciesDiffMatDistr_RBC(n_in,n_out,R,R_inf,kappa_in(2,:), ...
    kappa_out(2,:),alpha(2));
fprintf('here\n')
% Substituting in the matrices
A(N+1:2*N,N+1:2*N) = Du1;
W(N+1:2*N,2) = bu1;

% Hb

[Du2 bu2] = SingleSpeciesDiffMatDistr_RBC(n_in,n_out,R,R_inf,kappa_in(3,:), ...
    kappa_out(3,:),alpha(3));

% Substituting in the matrices
A(2*N+1:3*N,2*N+1:3*N) = Du2;
W(2*N+1:3*N,3) = bu2;


fprintf('*    Out DiffusionMatrixDistr_RBC.m *\n')
    
