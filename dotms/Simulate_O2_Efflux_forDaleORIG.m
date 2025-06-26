% Setting up the model, computing the parameter structure for the rhs in
% the ODE solver

% R. Occhipinti

clc
clear allexit
%close all

%ModelParameters_RBC_ok_PmO2_Params_ok_DiffSpecies % Model parameters for the distributed model
ModelParameters_RBC_ok_PmO2_Params_ok_Dale % Model parameters for the distributed model

[A W] = DiffusionMatrixDistr_RBC(n_in,n_out,R,R_inf, ...
                 kappa_in,kappa_out,alpha);

Params.DiffusionMatrix = A;
Params.BoundaryVector  = W;
Params.ReactionRates   = k;
Params.BoundaryValues  = X_inf;
Params.N               = N;
Params.n_out           = n_out;
Params.n_in            = n_in;
Params.HillCoeff       = n_Hill; 
Params.O2_50           = O2_50;

% Solving the system 

tic
tmax = 1.5;
options = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','on');
%[time,X] = ode15s(@ReactionDiffusionDistrRHS_RBC,[0,tmax],X0,options,Params);
[time,X] = ode15s(@ReactionDiffusionDistrRHS_RBC,linspace(0,2.0,4001),X0,options,Params);
toc

%save Sims_ArithMean/sim3_WT_Pm_0p35
%save Sims_ArithMean/DiffSpecies/Sims_Human
Calculate_t37_20190215

