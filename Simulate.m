% Copyright © 2015 Dale Huffman, Walter Boron
% SPDX-License-Identifier: GPL-3.0-or-later
% Original files this is derived from Copyright © 2015,2024 Rossana Occhipinti

% % This file runs simulations for CO2 addition 
% % Moreover it computes:
% % 1) delta_pHs = changes in steady-state pHs
% % 2) delta_pHi = changes in steady-state pHi
% % 3) dpHi/dt = initial rate of pHi change 
% % 4) tau_p = time to peak for pHs
% % 5) t_d = time delay for pHi changes (if we have it)
% 
% % R. Occhipinti
%
% Setting up the model, computing the parameter structure for the rhs in
% the ODE solver

% By Hand in Matlab
%run('rbc2024a/rbc2024a_paramsIn.m')
%Simulate('RBCO2','Blah','rbc2024a','rbc2024a')

% Simulate 
%  --> DiffusionMatrixDistr [ _RBC]
%       --> SingleSpeciesDiffMatDistr [ _RBC]
%            --> DiffusionMatrixInsideDistr
%            --> DiffusionMatrixOutsideDistr
%  
function [time,X] = Simulate(sim_type,prog_title,sim_dir,sim_filename_base)
fprintf('*******************************************\n')
fprintf('* In Simulate.m *\n')
fprintf('*******************************************\n')

% Read in user parameters from gui equivalent file
gui_param_file = strcat(sim_dir,'/',sim_filename_base,'_paramsIn.m');
fprintf('* GUI Param File =\n  %s *\n', gui_param_file )
fprintf('*** Running GUI Param File *\n')
run(gui_param_file);
fprintf('*** Successfully Ran GUI Param File *\n')

fprintf('*******************************************\n')
fprintf('\n*** SimType= %s ***\n', sim_type)

if strcmp(sim_type, 'JTB') || strcmp(sim_type, 'AJP')
    ModelParameters_All;
    %ModelParametersDistr_DE_paper_3_buff
    %Raif_ModelParametersDistr_Different_IC_Flow % Model parameters for the distributed model
elseif strcmp(sim_type, 'RBCO2')
    ModelParameters_RBC;
end

if strcmp(sim_type, 'JTB') || strcmp(sim_type, 'AJP')
    fprintf('* Calling DiffusionMatrixDistr *\n')
    [A W] = DiffusionMatrixDistr(n_in,n_out,R,R_inf, ...
                 kappa_in,kappa_out,perm_alpha,n_buff);

elseif strcmp(sim_type, 'RBCO2')
    fprintf('* Calling DiffusionMatrixDistr_RBC *\n')
    [A W] = DiffusionMatrixDistr_RBC(n_in,n_out,R,R_inf, ...
                     kappa_in,kappa_out,perm_alpha);
end

fprintf('* Setting Parms.X *\n')
Params.DiffusionMatrix = A;
Params.BoundaryVector  = W;
Params.ReactionRates   = k;
Params.BoundaryValues  = X_inf;
Params.N               = N;
Params.n_out           = n_out;
Params.n_in            = n_in;

if strcmp(sim_type, 'JTB') || strcmp(sim_type, 'AJP')
    Params.NumberOfBuffers = n_buff;

elseif strcmp(sim_type, 'RBCO2')
    Params.HillCoeff       = n_Hill; 
    Params.O2_50           = O2_50;
end

USE_MATLAB=1;
USE_OCTAVE=~USE_MATLAB;
USE_ODSTIME=1;

% Solving the system 
tic
%DALE tmax = 0.01;
%tmax=0.1;
fprintf('* Calling odeset *\n')
if USE_MATLAB
    %options = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','on','OutputFcn',@dale_odeprint);
    fprintf('Using MATLAB\n')
    %options = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','on');%,'OutputFcn',@(t,y,flag,outputArgs,dummy) dale_odeprint(t,y,flag,outputArgs,prog_title,tmax,11));
    options = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','off');% ,'OutputFcn',@(t,y,flag,outputArgs,dummy) dale_odeprint(t,y,flag,outputArgs,prog_title,tmax,11));
elseif USE_OCTAVE 
    fprintf('Using OCTAVE\n')
    options = odeset('RelTol',1e-15,'AbsTol',1e-15,'Stats','on');%,'OutputFcn',@(t,y,flag,outputArgs,dummy) dale_odeprint(t,y,flag,outputArgs,prog_title,tmax,11));
    %options = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','on','OutputFcn',@(t,y,flag,outputArgs) dale_odeprint(t,y,flag,outputArgs,prog_title,tmax,11));
end

if USE_OCTAVE 
    tin=[0,tmax];
end
fprintf('simtype=%s\n',sim_type)

if strcmp(sim_type, 'JTB')
    fprintf('*************************************************\n')
    fprintf('* Calling ode15s with ReactionDiffusionDistrRHS *\n')
    fprintf('*************************************************\n')
    if USE_MATLAB
        [time,X] = ode15s(@ReactionDiffusionDistrRHS,[0,tmax],X0,options,Params);
    elseif USE_OCTAVE 
        rdfunc = @(tin,X0) ReactionDiffusionDistrRHS(tin,X0,Params);
        [time,X] = ode15s(rdfunc,tin,X0,options);
    end
elseif strcmp(sim_type, 'AJP')
    %f_CO2on = 10000;%tmax;
    %tmax = 1000;
    fprintf('***************************************************************\n')
    fprintf('* Calling ode15s with ReactionDiffusionDistrRHS_React_ExpRamp *\n')
    fprintf('***************************************************************\n')
    if USE_MATLAB
        [time,X] = ode15s(@ReactionDiffusionDistrRHS_React_ExpRamp,[0,tmax],X0,options,Params,tf_CO2on);
    elseif USE_OCTAVE 
        rdfunc = @(tin,X0) ReactionDiffusionDistrRHS_React_ExpRamp(tin,X0,Params,tf_CO2on);
        [time,X] = ode15s(rdfunc,tin,X0,options);
    end
elseif strcmp(sim_type, 'RBCO2')
    %f_CO2on = 10000;%tmax;
    %tmax = 1000;
    fprintf('***************************************************************\n')
    fprintf('* Calling ode15s with ReactionDiffusionDistrRHS_RBC *\n')
    fprintf('***************************************************************\n')
    if USE_MATLAB
        if USE_ODSTIME
            [time,X] = ode15s(@ReactionDiffusionDistrRHS_RBC,[0,tmax],X0,options,Params);
            %[time,X] = ode15s(@ReactionDiffusionDistrRHS_RBC,linspace(0,2.0,4001),X0,options,Params);
        else
            [time,X] = ode15s(@ReactionDiffusionDistrRHS_RBC,linspace(0,tmax,4001),X0,options,Params);
            %time,X] = ode15s(@ReactionDiffusionDistrRHS_RBC,linspace(0,tmax,401),X0,options,Params);
            %[time,X] = ode15s(@ReactionDiffusionDistrRHS_RBC,linspace(0,tmax,101),X0,options,Params);
        end
    elseif USE_OCTAVE 
        rdfunc = @(tin,X0) ReactionDiffusionDistrRHS_RBC(tin,X0,Params);
        [time,X] = ode15s(rdfunc,tin,X0,options);
    end
%    Dale_Test_SI_FigVals
%    Dale_Test_SI_Figs
    %Calculate_t37_20190215
else
    fprintf('No sim_type match\n')
end

toc

outparams=strcat(sim_dir,'/',sim_filename_base,'_paramsOut')
matlab.io.saveVariablesToScript(outparams)
save(strcat(sim_dir,'/',sim_filename_base,'.mat'))

return

% save Simulations/PCO2m_water34/Delta100um/PlayingWithPCO2m_water/simulation_CAII20_CAIV20_PmCO2_34p2_dividedby_75000_nin325.mat

% break
% pH near the membrane

%n1 = (1+n_buff)*N + n_in; % one shell below membrane; n1+1 = @membrane
%tf_i = 100;
%tf_s = 100;
%depth = 50;      %  depth of electrode inside (in microns)
%depth = 1e-4*depth;  % d in centimeters
%rad_in = (R/n_in)*[0:n_in];
%ind_electrode = find(rad_in >= R-depth,1); % inside

%variable columns
%membrane_dist= n_in+1;
%col_CO2_at_membrane  = N*(0 + 0*n_buff) + membrane_dist;
%col_H2CO3_at_membrane= N*(1 + 0*n_buff) + membrane_dist;
%col_HA_at_membrane   = N*(2 + 0*n_buff) + membrane_dist;
%col_HCO3m_at_membrane= N*(3 + 0*n_buff) + membrane_dist;
%col_Am_at_membrane   = N*(4 + 0*n_buff) + membrane_dist;
%col_b2a_at_membrane  = N*(4 + 0*n_buff) + membrane_dist;
%col_b2b_at_membrane  = N*(4 + 0*n_buff) + membrane_dist;

%set(0,'defaultaxesfontsize',16)

%figure(1)
%thisshell= n1-(n_in-ind_electrode)
%plot(time,3-log10(X(:, n1-(n_in-ind_electrode))),'LineWidth',2)
%xlim([0 time(end)])
%title('Intracellular pH vs Time @ 50\mum')
%xlabel('Time (s)')
%ylabel('pH_i')
%hold all
%savefig( strcat(sim_dir,'/',sim_filename_base, '.pH_i.fig') )

%figure(2)
%thisshell=n1+2
%plot(time,3-log10(X(:,n1+2)),'LineWidth',2)
%xlim([0 time(end)])
%ylim([7.5 7.515])
%title('Extracellular pH vs Time')
%xlabel('Time (s)')
%ylabel('pH_s')
%hold all
%savefig( strcat(sim_dir,'/',sim_filename_base, '.pH_s.fig') )
% Calculations
%-------------------------------------------------------
% delta_pHs
%DALEpHs = 3-log10(X(:,n1+2));
%DALEaux = find(pHs==max(pHs));
%DALEtau_p = time(aux)
%DALEdelta_pHs = max(pHs)-pH_out
% figure(30)
% plot(time, pHs,'LineWidth',2)
% hold on
%plot(time_p,max(pHs),'r*')

%--------------------------------------------------------------
% delta_pHi
%DALEpHi = 3-log10(X(:,n1-(n_in-ind_electrode)));
%DALEdelta_pHi = min(pHi)-pH_in
%DALEbreak
%--------------------------------------------------------------

