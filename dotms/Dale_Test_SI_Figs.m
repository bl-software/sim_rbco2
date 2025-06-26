
mygreen = [0/255 128/255 0]; % WT
mypurple = [153/255 51/255 1]; % dKO + pCMBS

mycolor = mypurple;

set(0,'defaultaxesfontsize',20)
set(0,'defaultAxesFontName', 'Arial Narrow')

figure(200)
plot([-0.05; time], [Hb_Sat(1); Hb_Sat],'LineWidth', 2,'Color', mycolor) % OK 
xlim([-0.05 1])
%title('HbSat')
hold on
box off

figure(201)
plot([-0.05; time], [total_O2_conc(1);total_O2_conc] ,'LineWidth', 2,'Color', mycolor) % OK 
xlim([-0.05 1])
%title('O2')
hold on
box off

figure(202)
plot([-0.05; time], [total_HbO2_conc(1); total_HbO2_conc],'LineWidth', 2,'Color', mycolor) % OK 
xlim([-0.05 1])
%title('HbO2')
hold on
box off

figure(203)
plot([-0.05; time], [total_Hb_conc(1); total_Hb_conc],'LineWidth', 2,'Color', mycolor) % OK 
xlim([-0.05 1])
%title('Hb')
hold on
box off

figure(204)
plot([-0.05; time], [total_O2_HbO2(1); total_O2_HbO2],'LineWidth', 2,'Color', mycolor) % OK 
xlim([-0.05 1])
%title('O2+HbO2')
hold on
box off

figure(205)
plot([-0.05; time], [JO2_PM(1); JO2_PM], 'LineWidth',2,'Color', mycolor)
xlim([-0.05 1])
%title('JO2_{iPM}')
%ylabel('(cm/sec)mM')
hold on
box off

