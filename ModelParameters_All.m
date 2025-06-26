% Copyright © 2020 Dale Huffman, Walter Boron
% SPDX-License-Identifier: GPL-3.0-or-later
% Original file this is derived from Copyright © 2015 Rossana Occhipinti

% Model parameters for setting up the experiments and the model for the
% paper with Daniela and Erkki. We will consider only a Tris oocyte at 1.5%
% CO2
%
% To run an experiment you need to choose the oocyte type and the percentage of CO2
%
fprintf(' -> *********************************************\n')
fprintf('    * In ModelParameters_All.m *\n')
fprintf('    *********************************************\n')
%User_ModelCalcs
% 1. Geometry

%(deh INPUT) R      = 0.13/2;   % Radius of the cell in cm
%(deh INPUT) R_inf  = 0.15/2;   % Radius of the computational domain in cm
%(deh NOTES: Walter wanted Ds in mm - not centemeter - so changeing it here )
D
D_inf
thickness
R      = (D/10)/2       % Radius of the cell in cm
R_inf  = (D_inf/10)/2   % Radius of the computational domain in cm
%(deh INPUT) n_in   = 80;       % Discretization inside the cell
%(deh INPUT) n_out  = 100;      % Discretization outside the cell (you need to change it depending on the size of R_inf)
N      = n_in + n_out + 1;
%(deh_INPUT) n_buff = 2;
rad_in  =     ( R       / n_in  )*[0:n_in ];
rad_out = R + ((R_inf-R)/(n_out))*[0:n_out]; 

% Choose oocyte type
%oocyte_type = 'Tris';  % 'Tris', 'H2O', 'CAII', 'CAIV'

%(deh INPUT) CO2_pc = 1.5;  % CO2 percent 1.5, 5, 10

% Choose CO2 permeability (perm_alpha) across membrane
%(rxo ???) % hm = 5*10^-7;  % membrane thickness (cm)
%(deh INPUT) SA = 1;  % surface amplification factor

%##########DALE
rSA = 9  % surface amplification factor
rhm= 5*10^-7
rPm_CO2 = rSA*(1.71e-5/rhm) /100000;   % JTB 34.2 
%(deh INPUT) Pm_CO2 = SA*(1.71e-5/hm);%/100000;   # JTB 34.2 
Pm_CO2 = SA *Pm_CO2_input;%/100000;               # 

% Choose % of Immobile Buffer HA1/A1
%(deh INPUT) Buff_pc = 99/100; % this value could be taken from input parameter

% Flags to control the implementation of some features
%(deh INPUT) CAII_flag = 1; % addition (1) or not (0) of carbonic anhydrase II (CAII) 
%(deh INPUT) CAIV_flag = 1; % addition (1) or not (0) of carbonic anhydrase IV (CAIV) 
%(deh INPUT) layer_in_mem = 0; % mobility below the membrane (vesicles) smaller

% Implement CAII and CAIV activity
%(deh INPUT) A_CAII = 1;
CAII_in  = A_CAII * CAII_in; % Acceleration factor for CAII activity
CAIV_out = A_CAIV * CAIV_out; % Acceleration factor for CAIV activity
%(deh INPUT) A_CAIV = 1;

% 2. Mobility profile
% Mobility outside the cell. Units in cm2/s
% Order: CO2, H+, H2CO3, HCO3-
% Add buffers: HA1, A1, HA2, A2, ...
% Piecewise constant background profile
%(deh NEW) kappa_out = [1.71e-5;  8.69e-5; 1.11e-5; 1.11e-5];
%(deh NEW) kappa_out = kappa_out*ones(1,n_out);
%Note that HA2 has the same mobility as HA1
kappa_out = [kappa_out_co2;kappa_out_hp;kappa_out_h2co3;kappa_out_hco3m];

% Mobility inside the cell
%(deh NEW) kappa_in  = [1.71e-5;  8.69e-5; 1.11e-5; 1.11e-5];
%(deh NEW) kappa_in  = kappa_in*ones(1,n_in+1);
kappa_in  = [kappa_in_co2;kappa_in_hp;kappa_in_h2co3;kappa_in_hco3m];

% Mobility of buffers
if n_buff >= 2
    kappaBuff1_out = [buf_mob_out_ha1; buf_mob_out_a1];
    kappaBuff1_in  = [buf_mob_in_ha1 ; buf_mob_in_a1 ];

    kappa_out = [kappa_out; kappaBuff1_out];
    if sim_type == 'JTB'
        kappa_in  = [kappa_in;  kappaBuff1_in ]; 
    elseif sim_type == 'AJP'
        kappa_in  = 0.5*[kappa_in;  kappaBuff1_in ]; 
    end
end

if n_buff >= 3
%(deh INPUT)   kappaBuff_in  = [1.56e-5; 1.56e-5]; 
%(deh INPUT)   kappaBuff_out = [1.56e-5; 1.56e-5]; 
   kappaBuff2_out = [buf_mob_out_ha2; buf_mob_out_a2]
   kappaBuff2_in  = [buf_mob_in_ha2 ; buf_mob_in_a2 ]

   kappa_out = [kappa_out; kappaBuff2_out];
   kappa_in  = [kappa_in ; kappaBuff2_in ]; 
end
kappa_in  = kappa_in *ones(1, n_in+1);
kappa_out = kappa_out*ones(1, n_out );

if sim_type == 'AJP'
    if vit_mem == 1
        %(deh INPUT)tort_gamma = .03; % reduction factor
        kappa_out(:,1) = tort_gamma*kappa_out(:,1); % implement vitelline membrane
    end
end

% Adding a layer of lower mobility (vesicles)
if layer_in_mem == 1
%(deh INPUT)    d1 = 10;      %  distance of the layer from the surface (membrane) in microns
    d1 = 1e-4*d1;  % d in centimeters
    ind1 = find(rad_in <= R-d1);
%(deh INPUT)    d2 = 50;      % depth of the layer in microns
    d2 = 1e-4*d2; % (deh THICKNESS ???) d in centimeters
    ind2 = find(rad_in < R-(d1+d2));
    ind = setdiff(ind1,ind2);
%(deh INPUT)    oos_tort_lambda = .125;  % reduce mobility in the layer
    kappa_in(1:end,ind) = oos_tort_lambda*kappa_in(1:end,ind);
end

% 3. Reaction rate profiles. Order
% kb(1) : CO2   + H2O -> H2CO3             , background value
% kb(2) : H2CO3       -> CO2   + H2O
% kb(3) : H2CO3       -> HCO3- + H+
% kb(4) : HCO3- + H+  -> H2CO3
% Add buffers :
% k(5)    HA1         -> A1-   + H+
% k(6)    A1- + H+    -> HA1

% Constant background
kb = NaN(2*(1+n_buff),1);
kb(1) = kb_1; %(deh INPUT) 0.0302;        % Reaction rate of CO2 + H2O --> H2CO3  (s^-1)
kb(2) = kb_2; %(deh INPUT) 10.9631;       % Reaction velocity of H2CO3 --> CO2 + H2O  (s^-1)
K1=kb(1)/kb(2);           
%(deh INPUT) pK2 = 3.618357367951740;   % Dissociation const for carbonic acid
K2   = 10^(-pK2+3);   % Units in mM
kb(3) = kb_3; %(deh INPUT) 1e16;         % This value is a guess chosen to satisfy the equilibrium
kb(4) = kb(3)/K2;
pK_CO2 = pK1+pK2; % overall pK for CO2/HCO3m

% For HA1
if n_buff >= 2
%(deh INPUT)   pKHA1_out = 7.5; 
    KHA1_out  = 10^(-pKHA1_out+3);
    kb(5) = kb_5; %(deh INPUT)1e10
    kb(6) = kb(5)/KHA1_out;
end

% For HA2
% reaction rate constants of HA2 and HA1 are the same
if n_buff >= 3
    %(deh INPUT) pKHA2_out = 7.5;
    KHA2_out  = 10^(-pKHA2_out+3);
    kb(7) = kb_5;
    kb(8) = kb(7)/KHA2_out;
end
k = kb*ones(1,N);

% Adding carbonic anhydrase II everywhere inside the oocyte
if CAII_in_flag == 1
    ind_in = find(rad_in<=R);
    k(1:2,ind_in) = CAII_in*k(1:2,ind_in); 
end

% Adding carbonic anhydrase IV at 5nm above the membrane
if CAIV_out_flag == 1
    d = d_CAIV; %(deh INPUT) .005;      %  CAIV layer in microns
    d = 1e-4*d;  % d in centimeters
    ind_out = min(n_in+find(rad_out > R+d));  %outside
    k(1:2,ind_out) = CAIV_out*k(1:2,ind_out); 
end

% Adding carbonic anhydrase II everywhere outside
if sim_type == 'AJP'
    if CAII_out_flag == 1
        k(1:2,ind_out+1:end) = CAII_out*k(1:2,ind_out+1:end);
    end
end

% 4. Transmembrane mobility
% ------------------- (deh INPUT) THESE ARE THE PERMEABILITES the input is the denominator for both
%THERE WILL BE ONE FOR EACH OF THE MOBILITIES 
%FOR INSTANCE
%    PmCO2  PmHp PmH2CO3 etc
perm_alpha      = (1/1e-20)*ones(2+2*n_buff,1); %(deh INPUT) - THIS WAS A BAD VARIABLE NAME (alpha) WHICH IS A KEYWORD IN MATLAB
%TESTING
% TESTtPm_CO2= 0.030780000000000002
perm_alpha(1)   =  1/Pm_CO2; %  1/Permeability of CO2
% (deh FUTURE )perm_alpha = [ Pm_CO2 Pm_H Pm_H2CO3 Pm_HCO3 Pm_HA Pm_A ] 
% General Constants @ 22C (room temperature)
%(deh INPUT) PB     = 760;   % mmHg
%(deh INPUT) PH2O   = 35;  % mmHg
%(deh INPUT) sCO2   = 0.0434; % mM/mmHg CO2 solubility @ 22C
PCO2   = CO2_pc*(PB-PH2O)/100;  % vapor pressure

% 5. Initial concentrations. Outside the cell the concentration is assumed to
% be equal to the boundary value

CO2_out    = sCO2*PCO2; %mM
%(deh INPUT) pH_out     = 7.5;
Hplus_out  = 10^(-pH_out+3); % mM
H2CO3_out  = K1*CO2_out;
HCO3m_out  = (K2*H2CO3_out)/Hplus_out;

if n_buff >= 2
    %(deh INPUT) A1tot_out   = 5; % mM
    HA1_out     = Hplus_out*A1tot_out/(KHA1_out + Hplus_out);
    A1m_out     = A1tot_out - HA1_out;
end

if n_buff >= 3
    %(deh INPUT) A2tot_out   = 0; % mM
    HA2_out     = Hplus_out*A2tot_out/(KHA2_out + Hplus_out);
    A2m_out     = A2tot_out - HA2_out;
end

%(deh INPUT) CO2_in = 0;
%(deh INPUT) pH_in = 7.2;

% Select the correct initial intracellular pH (pH_in_i) using Raif mean
% values for pH_in_i and pH_in_fin
%if sim_type == 'AJP'
%    if CO2_pc == 1.5
%        if strcmp(oocyte_type, 'Tris')
%            pH_in_init = 7.22; 
%            pH_in_acid = 6.99; 
%        elseif strcmp(oocyte_type, 'H2O')
%            pH_in_init = 7.28;
%            pH_in_acid = 7.01; 
%        elseif strcmp(oocyte_type, 'CAII')
%            pH_in_init = 7.21;
%            pH_in_acid = 6.98; 
%        elseif strcmp(oocyte_type, 'CAIV')
%            pH_in_init = 7.40;
%            pH_in_acid = 7.06; 
%        end
%    elseif CO2_pc == 5
%        if strcmp(oocyte_type, 'Tris')
%            pH_in_init = 7.24;
%            pH_in_acid = 6.79; 
%        elseif strcmp(oocyte_type, 'H2O')
%            pH_in_init = 7.23;
%            pH_in_acid = 6.84; 
%        elseif strcmp(oocyte_type, 'CAII')
%            pH_in_init = 7.21;
%            pH_in_acid = 6.77; 
%        elseif strcmp(oocyte_type, 'CAIV')
%            pH_in_init = 7.37;
%            pH_in_acid = 6.79; 
%        end
%    elseif CO2_pc == 10
%        if strcmp(oocyte_type, 'Tris')
%            pH_in_init = 7.18;
%            pH_in_acid = 6.67; 
%        elseif strcmp(oocyte_type, 'H2O')
%            pH_in_init = 7.16;
%            pH_in_acid = 6.69; 
%        elseif strcmp(oocyte_type, 'CAII')
%            pH_in_init = 7.21;
%            pH_in_acid = 6.66; 
%        elseif strcmp(oocyte_type, 'CAIV')
%            pH_in_init = 7.40;
%            pH_in_acid = 6.61; 
%        end
%    end
%end

Hplus_in = 10^(-pH_in_init+3);
H2CO3_in = K1*CO2_in;
HCO3m_in = K2*H2CO3_in/Hplus_in;

% rxo fig6    7.23
%(deh INPUT) pKHA1_in = 7.10;  % (Corresponds to a pH_fin = 7.00) ??? pHi vs pH in 3v2 files

if n_buff >= 2
    if sim_type == 'AJP'
        [A1tot_in pKHA1_in beta_mean] = CalculateTotalBuffer(pH_in_init,pH_in_acid,HCO3m_in,CO2_out,pK_CO2);
%                                                                7.22       6.99     0       0.471975   6.1783
    end
%deh 5.8884e-05                7.23 in .mat files
%rxo 5.8884e-05                7.23 in .mat files
    KHA1_in = 10 ^(-pKHA1_in+3);

    %(deh INPUT) kb_HA1_in_plus = 1e10;
    %(deh INPUT) kb_HA1_in_minus = kb_HA1_in_plus/KHA1_in;
    % TESTING
    %kb_HA1_in_minus=125892541179416.62
    k(5,1:n_in+1) = kb_HA1_in_plus;
    k(6,1:n_in+1) = kb_HA1_in_minus;

    % A1tot_in = 27.312560103865501; % mM  (Buffer power of 15.65 mM/pH)
    %(deh INPUT) A1tot_in = (Buff_pc/100)*A1tot_in; % Immobile Buffer       

    HA1_in = Hplus_in*A1tot_in/(KHA1_in + Hplus_in);
    A1m_in = A1tot_in - HA1_in;
end

if n_buff >= 3
    % KHA2_in is equal to KHA1_in
    %(deh INPUT) pKHA2_in = 7.10;  % (Corresponds to a pH_fin = 7.0)
    KHA2_in = 10^(-pKHA2_in+3);
    %(deh INPUT) kb_HA2_in_plus = 1e10;
    %(deh INPUT) kb_HA2_in_minus = kb_HA2_in_plus/KHA2_in;
    k(7,1:n_in+1) = kb_HA2_in_plus;
    k(8,1:n_in+1) = kb_HA2_in_minus;
    
    %(deh INPUT) A2tot_in = (1 - Buff_pc / 100) * A1tot_in; %mM  Mobile Buffer
    HA2_in = Hplus_in * A2tot_in / (KHA2_in + Hplus_in);
    A2m_in = A2tot_in - HA2_in;    
end

% Setting up an initial value vector
% 

    u0_in  = CO2_in    *ones(n_in+1,1);
if sim_type == 'JTB'
    u0_out = CO2_out   * ones(n_out,1);
elseif sim_type == 'AJP'
    u0_out = CO2_out   *zeros(n_out,1);
end

    u1_in  = H2CO3_in  *ones(n_in+1,1);
if sim_type == 'JTB'
    u1_out = H2CO3_out * ones(n_out,1);
elseif sim_type == 'AJP'
    u1_out = H2CO3_out *zeros(n_out,1);
end

    v0_in  = Hplus_in  *ones(n_in+1,1);
    v0_out = Hplus_out *ones(n_out ,1);

    v1_in  = HCO3m_in  *ones(n_in+1,1);
if sim_type == 'JTB'
    v1_out = HCO3m_out * ones(n_out,1);
elseif sim_type == 'AJP'
    v1_out = HCO3m_out *zeros(n_out,1);
end

if n_buff >= 2
    u2_in  = HA1_in    *ones(n_in+1,1);
    u2_out = HA1_out   *ones(n_out ,1);
    v2_in  = A1m_in    *ones(n_in+1,1);
    v2_out = A1m_out   *ones(n_out ,1);
end
if n_buff >= 3
    u3_in  = HA2_in    *ones(n_in+1,1);
    u3_out = HA2_out   *ones(n_out ,1);
    v3_in  = A2m_in    *ones(n_in+1,1);
    v3_out = A2m_out   *ones(n_out ,1);
end

u0     = [u0_in; u0_out]; % CO2
u1     = [u1_in; u1_out]; % H2CO3
v0     = [v0_in; v0_out]; % Hplus
v1     = [v1_in; v1_out]; % HCO3m
if n_buff >= 2
    u2 = [u2_in; u2_out]; % HA1
    v2 = [v2_in; v2_out]; % A1m
end
if n_buff >= 3
    u3 = [u3_in; u3_out]; % HA2
    v3 = [v3_in; v3_out]; % A2m
end

u     = [u0;u1];
v     = [v0;v1];
if n_buff >= 2
    u = [u;u2];
    v = [v;v2];
end
if n_buff >= 3
    u = [u;u3];
    v = [v;v3];
end

X0 = [u;v];

% Boundary values
if sim_type == 'JTB'
    u_inf = [u0_out(1); u1_out(1)];
    v_inf = [v0_out(1); v1_out(1)];
elseif sim_type == 'AJP'
    u_inf = [CO2_out;   H2CO3_out];
    v_inf = [Hplus_out; HCO3m_out];
end

if n_buff >= 2
    if sim_type == 'JTB'
        u_inf = [u_inf; u2_out(1)];
        v_inf = [v_inf; v2_out(1)];
    elseif sim_type == 'AJP'
        u_inf = [u_inf; HA1_out];
        v_inf = [v_inf; A1m_out];
    end
end

if n_buff >= 3
    u_inf = [u_inf;u3_out(1)];
    v_inf = [v_inf;v3_out(1)];
end

X_inf = [u_inf;v_inf];

%COMPARISON DUMMYS
CAII_flag = CAII_in_flag
CAIV_flag = CAIV_out_flag
alpha = perm_alpha
pKHA_out=pKHA1_out
pKHA_in=pKHA1_in
KHA_out=KHA1_out
KHA_in=KHA1_in
Atot_in=A1tot_in
Atot_out=A1tot_out
Am_in=A1m_in
Am_out=A1m_out
HA_in=HA1_in
HA_out=HA1_out
kb_HA_in_plus=kb_HA1_in_plus
kb_HA_in_minus=kb_HA1_in_minus

if sim_type == 'AJP'
  CAII_flag_out = CAII_out_flag
  Red_factor = tort_gamma
  tiny = oos_tort_lambda
end
