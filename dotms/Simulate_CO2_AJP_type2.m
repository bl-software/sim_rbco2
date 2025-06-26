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
% % Setting up the model

% clc
clear all
% close all

Raif_ModelParametersDistr_Different_IC_Flow % Model parameters for the distributed model

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
tf_CO2on = 1000;
tmax = 1000;
options = odeset('RelTol',1e-12,'AbsTol',1e-12,'Stats','on');
[time,X] = ode15s(@ReactionDiffusionDistrRHS_React_ExpRamp,[0,tmax],X0,options,Params,tf_CO2on);
toc

% save 20101130_Simulations/10um/Vesicles_VitellineMembrane/15CO2/simulation_CAII500_CAIV1000_Vesicles_tiny006_VitMembrane_RedFact006_VfON_delta10um.mat
%break
 
% depth of pHi electrode 
depth = 50;  % um

% pH near the membrane

n1 = (1+n_buff)*N + n_in; % one shell below membrane; n1+1 = @membrane

pHs = 3-log10(X(:,n1+2));

depth = 1e-4*depth;  % depth in centimeters
rad_in = (R/n_in)*[0:n_in];
ind_electrode = find(rad_in >= R-depth,1); % index corresponding to the chosen depth for pHi
pHi = 3-log10(X(:,n1-(n_in-ind_electrode))); % pHi at chosen depth

set(0,'defaultaxesfontsize',16)

figure(1)
plot(time,pHi,'LineWidth',3)
xlim([0 time(end)])
%title('Intracellular pH vs Time @ 50\mum')
xlabel('Time (s)')
ylabel('pH_i')
hold all

figure(2)
plot(time,pHs,'LineWidth',3)
xlim([0 time(end)])
%ylim([7.5 7.515])
%title('Extracellular pH vs Time')
xlabel('Time (s)')
ylabel('pH_s')
hold all

%break
% Calculations

%-------------------------------------------
%% delta_pHS

myaux1 = find(pHs == max(pHs));
tau_p = time(myaux1)  % time to peak
delta_pHs = max(pHs)-pH_out

%--------------------------------------------------------------
%% delta_pHi

delta_pHi = min(pHi)- pH_in_init

%--------------------------------------------------------------
% Find the slope dpHi_dt
for j = 1:size(time,1)-1
    
    time_minus = time(j);
    time_plus = time(j+1);
    pHi_minus = pHi(j);
    pHi_plus = pHi(j+1);
    dt = time_plus-time_minus;
    dpHi = pHi_plus-pHi_minus;
    dpHi_dt(j) = dpHi/dt;
    
end

% Calculate time delay for pHi using dpHi_dt
myaux2 = find(dpHi_dt == min(dpHi_dt));
td_dpHidt = time(myaux2)

% Calculate time delay as the time needed for pHi to deacrease of 0.01
diff_pHi = pH_in_init-pHi;
myaux3 = find(diff_pHi<=0.01, 1, 'last' );
diff_pHi(myaux2);
diff_pHi(myaux3);
td_001 = time(myaux3)

% Plot dpHi_dt
figure(3)
plot(time,[dpHi_dt dpHi_dt(end)],'LineWidth',3)
title('dpH_i/dt')
hold all

min_dpHidt = min(dpHi_dt)
%break


% pHi_baseline = pH_in_init*ones(length(time),1);
% myaux4 = find(time<=12,1,'last');
% tg_pHi = pHi(myaux2)+min_dpHidt.*(time - td_dpHidt);
% 
% figure(100)
% plot(time(1:myaux4),pHi(1:myaux4),'LineWidth',3)
% hold on
% plot(time(1:myaux4),tg_pHi(1:myaux4),'c','LineWidth',1.5)
% hold on
% plot(time(1:myaux4),pHi_baseline(1:myaux4),'--m','LineWidth',1.5)
% hold on 
% plot(td_dpHidt,pHi(myaux2),'.r','MarkerSize',30)
% 
% myaux5 = find(tg_pHi>=pH_in_init,1,'last');
% time_delay = time(myaux5)
% %---------------------------------------------------------------
% % table = [delta_pHi;dpHi_dt];
% % clc
% % fprintf('delta_pHi \t dpHi_dt\n')
% % fprintf('%6.4f\t %6.4f\n',table)
