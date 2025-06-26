% This file plots the 6 panels of SI Fig 7
% Note that the mat file for dKO + pCMBS is sim_WT_Pm_0p014 (Pm,O2 = 0.014
% cm/sec)

%clc
%clear all

mygreen = [0/255 128/255 0]; % WT
mypurple = [153/255 51/255 1]; % dKO + pCMBS

if strcmp(fig4_sim_type, 'WT')
    load Sims_ArithMean/sim3_1p01um_18p73Hb_WT   % WT
    mycolor = mygreen;

elseif strcmp(fig4_sim_type, 'dKO')
    load Sims_ArithMean/sim3_WT_Pm_0p01365        % dKO + pCMBS
    mycolor = mypurple;
end


r_in   = (R/n_in)*[0:n_in]; % n_in+1 = 102 = @PM
r_out  = R + ((R_inf-R)/(n_out))*[0:n_out];

tk = R/n_in; % shell tickness...1e-6 cm

r_plot = [r_in,r_out(2:end)];  % do not change this!!! r_in(end) = r_out(1)!!!

% Extract concentration of solutes (mM) from output matrix X

X_O2 = X(:,1:N);         % O2  (time,space)
X_HbO2 = X(:,N+1:2*N); % HbO2(time,space)
X_Hb = X(:,2*N+1:3*N); % Hb  (time,space)

X_O2_in = X_O2(:,1:n_in+1); % O2 (time, (shell 0(@center): shell 102(@PM))
X_HbO2_in = X_HbO2(:,1:n_in+1); % HbO2 (time, (shell 0(@center): shell 102(@PM))
X_Hb_in = X_Hb(:,1:n_in+1); % Hb (time, (shell 0(@center): shell 102(@PM))

% Calculate Vshell = volume of each shell. We have n_in shells
% Calculate moles of HbO2 per shell (moles_HbO2_pershell). Here we have a matrix with same
% dimension of X_HbO2_in ... do same calculation for X_Hb_in  

Vshell = zeros(1,length(X_HbO2_in(1,:))); % units of cm^3
moles_O2_pershell = zeros(length(X_O2_in(:,1)),length(X_O2_in(1,:))); % units of umol
moles_HbO2_pershell = zeros(length(X_HbO2_in(:,1)),length(X_HbO2_in(1,:))); % units of umol
moles_Hb_pershell = zeros(length(X_Hb_in(:,1)),length(X_Hb_in(1,:))); % units of umol

for j = 1:n_in
    Vshell(j+1) = ((4/3)*pi)*((r_in(j+1)^3)-(r_in(j)^3)); % units of cm^3
    moles_O2_pershell(:,j+1) =  X_O2_in(:,j+1).*Vshell(j+1); % mM x cm^3 = umol. Remember that 1 mM = 1 umol/cm^3  
    moles_HbO2_pershell(:,j+1) =  X_HbO2_in(:,j+1).*Vshell(j+1); % mM x cm^3 = umol. Remember that 1 mM = 1 umol/cm^3  
    moles_Hb_pershell(:,j+1) =  X_Hb_in(:,j+1).*Vshell(j+1); % mM x cm^3 = umol. Remember that 1 mM = 1 umol/cm^3  
end

% Calculate total moles of HbO2 in the RBC....this is a column vector with
% length equal to the rows of X ....that is equal to the discretization of
% time (i.e, it is time-dependent). Do the same for total moles of Hb

moles_O2_total = sum(moles_O2_pershell,2); % units of umol
moles_HbO2_total = sum(moles_HbO2_pershell,2); % units of umol
moles_Hb_total = sum(moles_Hb_pershell,2); % units of umol

Vsphere = (4/3)*pi*(r_in(end)^3); % cm^3

% Check calculation...ok!
total_O2_conc = moles_O2_total./Vsphere; % units mM
%
total_HbO2_conc = moles_HbO2_total./Vsphere; % units mM
% 
total_Hb_conc = moles_Hb_total./Vsphere; % units mM
%
total_O2_HbO2 = total_O2_conc + total_HbO2_conc;
% 
Hb_Sat = total_HbO2_conc./(total_HbO2_conc+total_Hb_conc);

set(0,'defaultaxesfontsize',20)
set(0,'defaultAxesFontName', 'Arial Narrow')

%fa=figure(100)
%plot([-0.05; time], [total_O2_conc(1);total_O2_conc] ,'LineWidth', 2,'Color', mycolor) % OK 
%xlim([-0.05 1])
%title('a: O2')
%hold on
%box off
%
%faz=figure(110)
%cutofftime=0.001								% +1 ms
%starttime=-0.0001								% -0.5 ms
%zoomt=time(find(time<cutofftime))
%zoomo=total_O2_conc(find(time<cutofftime))
%plot([starttime; zoomt], [total_O2_conc(1);zoomo] ,'LineWidth', 2,'Color', mycolor) % OK 
% %xlim([-0.05 zoomt(end)])
% %xlim([-0.05 1])
% %ylim([0,1])
%title('a: [O2]i Zoomed')
%hold on
%box off
%
%
%fb=figure(101)
%plot([-0.05; time], [total_HbO2_conc(1); total_HbO2_conc],'LineWidth', 2,'Color', mycolor) % OK 
%xlim([-0.05 1])
%title('b: HbO2')
%hold on
%box off
%
%fc=figure(102)
%plot([-0.05; time], [total_O2_HbO2(1); total_O2_HbO2],'LineWidth', 2,'Color', mycolor) % OK 
%xlim([-0.05 1])
%title('c: O2+HbO2')
%hold on
%box off
%
%fd=figure(103)
%plot([-0.05; time], [Hb_Sat(1); Hb_Sat],'LineWidth', 2,'Color', mycolor) % OK 
%xlim([-0.05 1])
%title('d: HbSat')
%hold on
%box off
%
%fe=figure(104)
%plot([-0.05; time], [total_Hb_conc(1); total_Hb_conc],'LineWidth', 2,'Color', mycolor) % OK 
%xlim([-0.05 1])
%title('e: Hb')
%hold on
%box off

% Flux across PM
JO2_PM = Pm_O2.*(X_O2(:,n_in+1)-X_O2(:,n_in+2));

ff=figure(105)
% old plot([-0.05; time], [JO2_PM(1); JO2_PM], 'LineWidth',2,'Color', mycolor)
plot([-0.05; 0.0; time], [0.0; 0.0; JO2_PM], 'LineWidth',2,'Color', mycolor)
xlim([-0.05 1])
title('f: JO2_{iPM}')
ylabel('(cm/sec)mM')
hold on
box off

ffz=figure(115)
cutofftime=0.001								% +1 ms
starttime=-0.0001								% -0.5 ms
%nexttile
zoomt=time(find(time<cutofftime))
zoomj=JO2_PM(find(time<cutofftime))
% OLD with line up top
% plot([starttime; zoomt], [JO2_PM(1); zoomj] ,'LineWidth', 2,'Color', mycolor) % OK 
plot([starttime; 0.0; zoomt], [0.0; 0.0; zoomj] ,'LineWidth', 2,'Color', mycolor) % OK 
%xlim([-0.05 zoomt(end)])
%xlim([-0.05 1])
%ylim([0,1])
title('f: JO2_{iPM} Zoomed')
hold on
box off


