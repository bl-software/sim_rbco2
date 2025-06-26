% This file computes the total amount of intracellular buffer (TA) needed
% to get the measured delta_pHi. 
% Inputs: pH_in_i = initial intracellular pH
%         pH_in_fin = final (acidic) intracellular pH
%         HCO3m_in = intracellular [HCO3m]
%         CO2_out = CO2 concentration outside the cell
%         pK_CO2 = overall pK for the CO2/HCO3m buffer
% Outputs: TA
%          pK
%          beta_mean = intrinsic buffer power 


function [TA pK beta_mean] = CalculateTotalBuffer(pH_in_i,pH_in_fin,HCO3m_in,CO2_out,pK_CO2)

HCO3m_in_fin =  CO2_out*10.^(pH_in_fin-pK_CO2); % @ pHi_fin
slope = (HCO3m_in_fin-HCO3m_in)/(pH_in_fin-pH_in_i);
beta_mean  = -slope;  % mean intrinsic buffer (HA/Am) power
a = pH_in_i;
b = pH_in_fin;

pK = (a+b)/2; 
% as mean between initial and final (acidic) pHi
K = 10^(-pK);
Q = (1/(1+K*10^a))-(1/(1+K*10^b));
TA = ((b-a)*beta_mean)/Q;


