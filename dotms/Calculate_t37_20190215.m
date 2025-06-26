% This file calculates the t37 of the HbSat curve using 
% (1) integrated concentrations of HbO2 and Hb (in units of mM) as:
% ..............
% (2) linear interpolation for t37..............

%clc
%clear all

%load Sims/test

% %load Sims/sim_1p01um_18p73Hb_WT_P50
% %load Sims/sim_1p04um_17p71Hb_AQP1_KO_P50
% %load Sims/sim_1p09um_17p87Hb_RhAG_KO_P50
%load Sims/sim3_WT_Pm_0p005

r_in   = (R/n_in)*[0:n_in]; % n_in+1 = 102 = @PM
r_out  = R + ((R_inf-R)/(n_out))*[0:n_out];

%tk = R/n_in; % shell tickness...1e-6 cm

r_plot = [r_in,r_out(2:end)];  % do not change this!!! r_in(end) = r_out(1)!!!

% Extract concentration of solutes (mM) from output matrix X

% X_O2 = X(:,1:N);     % O2  (time,space)
X_HbO2 = X(:,N+1:2*N); % HbO2(time,space)
X_Hb = X(:,2*N+1:3*N); % Hb  (time,space)

X_HbO2_in = X_HbO2(:,1:n_in+1); % HbO2 (time, (shell 0(@center): shell 102(@PM))
X_Hb_in = X_Hb(:,1:n_in+1); % Hb   (time, (shell 0(@center): shell 102(@PM))

% Calculate Vshell = volume of each shell. We have n_in shells
% Calculate moles of HbO2 per shell (moles_HbO2_pershell). Here we have a matrix with same
% dimension of X_HbO2_in ... do same calculation for X_Hb_in  

Vshell = zeros(1,length(X_HbO2_in(1,:))); % units of cm^3
moles_HbO2_pershell = zeros(length(X_HbO2_in(:,1)),length(X_HbO2_in(1,:))); % units of umol
moles_Hb_pershell   = zeros(length(X_Hb_in  (:,1)),length(X_Hb_in  (1,:))); % units of umol

for j = 1:n_in
    Vshell(j+1) = ((4/3)*pi)*((r_in(j+1)^3)-(r_in(j)^3)); % units of cm^3
    moles_HbO2_pershell(:,j+1) =  X_HbO2_in(:,j+1).*Vshell(j+1); % mM x cm^3 = umol. Remember that 1 mM = 1 umol/cm^3  
    moles_Hb_pershell(:,j+1) =  X_Hb_in(:,j+1).*Vshell(j+1); % mM x cm^3 = umol. Remember that 1 mM = 1 umol/cm^3  
end

% Calculate total moles of HbO2 in the RBC....this is a column vector with
% length equal to the rows of X ....that is equal to the discretization of
% time (i.e, it is time-dependent). Do the same for total moles of Hb

moles_HbO2_total = sum(moles_HbO2_pershell,2); % units of umol
moles_Hb_total = sum(moles_Hb_pershell,2); % units of umol

Vsphere = (4/3)*pi*(r_in(end)^3); % cm^3

% Check calculation...ok!
total_HbO2_conc = moles_HbO2_total./Vsphere; % units mM
% 
total_Hb_conc = moles_Hb_total./Vsphere; % units mM
% 
Hb_Sat = total_HbO2_conc./(total_HbO2_conc+total_Hb_conc);

figure()
plot(time, Hb_Sat,'LineWidth', 2) % OK 
title('HbSat')
hold all

% figure(101)
% plot(time, total_HbO2_conc,'LineWidth', 2) % OK 
% title('HbO2')
% hold all
% 
% figure(102)
% plot(time, total_Hb_conc,'LineWidth', 2) % OK 
% title('Hb')
% hold all

y = Hb_Sat;
t = time;

y_37 = exp(-1)*y(1); % this is the "exact" value of y at time t = t37 

myaux1 = find(y >= y_37,1,'last'); % find the values of y that are greater or equal than the y_37pc and identify the largest index in the vector ( see RO notes ...page XXXX) 
myaux2 = myaux1+1;
% myaux2 = max(find(y >= exp(-1)*y(1)));

% Coordinates of point A
t1 = t(myaux1);
y1 = y(myaux1);

% Coordinates of point B
t2 = t(myaux2);
y2 = y(myaux2);
% 
% t_37 = (y_37*(t2-t1)-(t2*y1-t1*y2))/(y2-y1)
% k37 = 1/t_37
% 
% % Old calculation
% fprintf('Old calculation')
% 
% time_37pc = t(myaux1) % time to decay by 36.79 % (i.e. time constant for a single exponential decay)
% k37 = 1/time_37pc
% 

% New calculation
fprintf('New calculation')
Pm_O2
t_37 = (y_37*(t2-t1)-(t2*y1-t1*y2))/(y2-y1)
k37 = 1/t_37


    
