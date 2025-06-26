% Setting up the model, computing the parameter structure for the rhs in
% the ODE solver

% R. Occhipinti

clc
clear all
%close all

%run("rbc2024/rbc2024_paramsIn.m")
%run("ModelParameters_RBC.m")
%[A W] = DiffusionMatrixDistr_RBC(n_in,n_out,R,R_inf, ...
%                 kappa_in,kappa_out,perm_alpha);
ModelParameters_RBC_ok_PmO2_Params_ok_DiffSpecies % Model parameters for the distributed model
%fprintf('Sim O2 Efflux\n')
%fprintf(' .. Call Dff\n')
%[A W] = DiffusionMatrixDistr_RBC(n_in,n_out,R,R_inf, ...
%                 kappa_in,kappa_out,alpha);
%fprintf(' .. Ret Dff')

%TEMPParams.DiffusionMatrix = A;
%TEMPParams.BoundaryVector  = W;
%TEMPParams.ReactionRates   = k;
%TEMPParams.BoundaryValues  = X_inf;
%TEMPParams.N               = N;
%TEMPParams.n_out           = n_out;
%TEMPParams.n_in            = n_in;
%TEMPParams.HillCoeff       = n_Hill; 
%TEMPParams.O2_50           = O2_50;
%TEMP
%TEMP% Solving the system 
%TEMP
%TEMPtic
%TEMPtmax = 1.5;
%TEMPoptions = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','on');
%TEMP[time,X] = ode15s(@ReactionDiffusionDistrRHS_RBC,[0,tmax],X0,options,Params);
%TEMPtoc

%save Sims_ArithMean/sim3_WT_Pm_0p35
%save Sims_ArithMean/DiffSpecies/Sims_Human

