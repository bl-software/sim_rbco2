% This is the main file to run simulations of CO2 addition 

% This file computes:
% 1) delta_pHs = changes in steady-state pHs
% 2) delta_pHi = changes in steady-state pHi

% R. Occhipinti

% Setting up the model, computing the parameter structure for the rhs in
% the ODE solver
function [time,X] = Simulate_CO2_JTB_type1_addition_only(prog_title,sim_dir,sim_filename_base)
fprintf('*******************************************\n')
fprintf('* In Simulate_CO2_addition_ONLY_cleaned.m *\n')
fprintf('*******************************************\n')

% Read in user parameters from gui equivalent file
gui_param_file = strcat(sim_dir,'/',sim_filename_base,'.m');
fprintf('* GUI Param File = %s *\n', gui_param_file )
fprintf('* Running GUI Param File *\n')
run(gui_param_file)

ModelParametersDistr_DE_paper_3_buff

%if n_buff==2
%    ModelParametersDistr_DE_paper % Model parameters for the distributed model
%elseif n_buff==3
%    ModelParametersDistr_DE_paper_3_buff
%end

%[A W] = DiffusionMatrixDistr(n_in,n_out,R,R_inf, ...
%                 kappa_in,kappa_out,[1;1;1;1;1;1],n_buff);
[A W] = DiffusionMatrixDistr(n_in,n_out,R,R_inf, ...
                 kappa_in,kappa_out,perm_alpha,n_buff);

Params.DiffusionMatrix = A;
Params.BoundaryVector  = W;
Params.ReactionRates   = k;
Params.BoundaryValues  = X_inf;
Params.N               = N;
Params.NumberOfBuffers = n_buff;
Params.n_out           = n_out;
Params.n_in            = n_in;
% Solving the system 
tic
%DALE tmax = 0.01;
%options = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','on','OutputFcn',@dale_odeprint);
options = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','on','OutputFcn',@(t,y,flag,outputArgs) dale_odeprint(t,y,flag,outputArgs,prog_title,tmax,11));
[time,X] = ode15s(@ReactionDiffusionDistrRHS,[0,tmax],X0,options,Params);
toc
% save Simulations/PCO2m_water34/Delta100um/PlayingWithPCO2m_water/simulation_CAII20_CAIV20_PmCO2_34p2_dividedby_75000_nin325.mat

% break
% pH near the membrane

n1 = (1+n_buff)*N + n_in; % one shell below membrane; n1+1 = @membrane
tf_i = 100;
tf_s = 100;
depth = 50;      %  depth of electrode inside (in microns)
depth = 1e-4*depth;  % d in centimeters
rad_in = (R/n_in)*[0:n_in];
ind_electrode = find(rad_in >= R-depth,1); % inside

%variable columns
membrane_dist= n_in+1;
col_CO2_at_membrane  = N*(0 + 0*n_buff) + membrane_dist;
col_H2CO3_at_membrane= N*(1 + 0*n_buff) + membrane_dist;
col_HA_at_membrane   = N*(2 + 0*n_buff) + membrane_dist;
col_HCO3m_at_membrane= N*(3 + 0*n_buff) + membrane_dist;
col_Am_at_membrane   = N*(4 + 0*n_buff) + membrane_dist;
col_b2a_at_membrane  = N*(4 + 0*n_buff) + membrane_dist;
col_b2b_at_membrane  = N*(4 + 0*n_buff) + membrane_dist;



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
save(strcat(sim_dir,'/',sim_filename_base,'.mat'))

return
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

