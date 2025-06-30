% Setting up the model, computing the parameter structure for the rhs in
% the ODE solver

% R. Occhipinti

clc
clear all
%close all

ModelParameters_RBC_ok_PmO2_Params_ok_JP % Model parameters for the distributed model
%ModelParameters_RBC_ok_PmO2_Params_ok_klysate_JP

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
[time,X] = ode15s(@ReactionDiffusionDistrRHS_RBC,[0,tmax],X0,options,Params);
toc

%save Sims_ArithMean/sim3_1p07um_18p17Hb_10p44klys_dKO
%save Sims_ArithMean/sim3_1p09um_17p87Hb_12p03klys_RhAG_KO
%save Sims_ArithMean/sim3_1p04um_17p71Hb_12p31klys_AQP1_KO
%save Sims_ArithMean/sim3_1p01um_18p73Hb_11p60klys_WT
%save Sims_ArithMean/sim3_WT_DO2in_0_2025


