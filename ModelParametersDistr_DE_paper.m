% Model parameters for setting up the experiments and the model for the
% paper with Daniela and Erkki. We will consider only a Tris oocyte at 1.5%
% CO2
%
% To run an experiment you need to choose the oocyte type and the percentage of CO2
%
fprintf(' -> **************************************\n')
fprintf('    * In ModelParametersDistr_DE_paper.m *\n')
fprintf('    **************************************\n')
%User_ModelCalcs
% 1. Geometry

%(deh INPUT) R      = 0.13/2;   % Radius of the cell in cm
%(deh INPUT) R_inf  = 0.15/2;   % Radius of the computational domain in cm
%(deh INPUT) NOTES: Walter wanted Ds in mm - not centemeter - so changeing it here
R      = (D/10)/2;       % Radius of the cell in cm
R_inf  = (D_inf/10)/2;   % Radius of the computational domain in cm
%(deh INPUT) n_in   = 80;       % Discretization inside the cell
%(deh INPUT) n_out  = 100;      % Discretization outside the cell (you need to change it depending on the size of R_inf)
N      = n_in + n_out + 1;
%(deh INPUT) n_buff = 2;
rad_in = (R/n_in)*[0:n_in];
rad_out  = R + ((R_inf-R)/(n_out))*[0:n_out];

% Choose oocyte type
% oocyte_type = 'Tris';  % 'Tris', 'H2O', 'CAII', 'CAIV'

%(deh INPUT) CO2_pc = 1.5;  % CO2 percent 1.5, 5, 10

% Choose CO2 permeability (perm_alpha) across membrane
%RXOhm = 5*10^-7;  % membrane thickness (cm)
%(deh INPUT) SA = 1;  % surface amplification factor

%(deh INPUT) = SA*(1.71e-5/hm);%/100000; 
Pm_CO2 = SA*Pm_CO2_input;%/100000; 




% Flags to control the implementation of some features
%(deh INPUT) CAII_flag = 1; % addition (1) or not (0) of carbonic anhydrase II (CAII) 
%(deh INPUT) CAIV_flag = 1; % addition (1) or not (0) of carbonic anhydrase IV (CAIV) 
%(deh INPUT) layer_in_mem = 0; % mobility below the membrane (vesicles) smaller

% Implement CAII and CAIV activity
%(deh INPUT) A_CAII = 1;
CAII_in = A_CAII; % Acceleration factor for CAII activity
%(deh INPUT) A_CAIV = 1;
CAIV_out = A_CAIV; % Acceleration factor for CAIV activity

% 2. Mobility profile
% Mobility outside the cell. Units in cm2/s
% Order: CO2, H+, H2CO3, HCO3-
% Add buffers: HA1, A1, HA2, A2, ...
% Piecewise constant background profile
%(deh INPUT) kappa_out = [1.71e-5;  8.69e-5; 1.11e-5; 1.11e-5];
%(deh INPUT) NEW SPLIT OUTkappa_out = kappa_out*ones(1,n_out);

kappa_out = [kappa_out_co2;kappa_out_hp;kappa_out_h2co3;kappa_out_hco3m]*ones(1,n_out);

% Mobility inside the cell
%(deh INPUT) kappa_in  = [1.71e-5;  8.69e-5; 1.11e-5; 1.11e-5];
%(deh INPUT) NEW SPLIT OUT kappa_in  = kappa_in*ones(1,n_in+1);
kappa_in  = [kappa_in_co2;kappa_in_hp;kappa_in_h2co3;kappa_in_hco3m]*ones(1,n_in+1);

% Mobility of buffers
if n_buff == 2
%(deh INPUT)   kappaBuff_in  = [1.56e-5; 1.56e-5]; 
%(deh INPUT)   kappaBuff_out = [1.56e-5; 1.56e-5]; 
%(deh INPUT) NEW SPLIT OUT   kappaBuff_in  = kappaBuff_in*ones(1,n_in+1);
   kappaBuff_in  = [buf_mob_in_ha1;buf_mob_in_a1]*ones(1,n_in+1);
%(deh INPUT) NEW SPLIT OUT   kappaBuff_out = kappaBuff_out*ones(1,n_out);
   kappaBuff_out = [buf_mob_out_ha1;buf_mob_out_a1]*ones(1,n_out);
   kappa_in  = [kappa_in;kappaBuff_in]; 
   kappa_out = [kappa_out;kappaBuff_out];
end

% Adding a layer of lower mobility (vesicles)
if layer_in_mem == 1
%(deh INPUT)    d1 = 10;      %  distance of the layer from the surface (membrane) in microns
    d1 = 1e-4*d1;  % d in centimeters
    ind1 = find(rad_in <= R-d1);
%(deh INPUT)    d2 = 50;      % depth of the layer in microns
    d2 = 1e-4*d2; % d in centimeters
    ind2 = find(rad_in < R-(d1+d2));
    ind = setdiff(ind1,ind2);
%(deh INPUT)    tiny = .125;  % reduce mobility in the layer
    kappa_in(1:end,ind) = tiny*kappa_in(1:end,ind);
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
if n_buff == 2
%(deh INPUT)   pKHA_out = 7.5; 
    KHA1_out  = 10^(-pKHA_out+3);
    kb(5) = kb_5; %(deh INPUT);
    kb(6) = kb(5)/KHA1_out;
end









k = kb*ones(1,N);

% Adding carbonic anhydrase II everywhere inside the oocyte
if CAII_flag == 1
    ind_in = find(rad_in<=R);
    k(1:2,ind_in) = CAII_in*k(1:2,ind_in); 
end

% Adding carbonic anhydrase IV at 5nm above the membrane
if CAIV_flag == 1
    d = d_CAIV; %(deh INPUT) .005;      %  CAIV layer in microns
    d = 1e-4*d;  % d in centimeters
    ind_out = min(n_in+find(rad_out > R+d));  %outside
    k(1:2,ind_out) = CAIV_out*k(1:2,ind_out); 
end

% 4. Transmembrane mobility
% ------------------- DALE THESE ARE THE PERMEABILITES the input is the denominator for both
%THERE WILL BE ONE FOR EACH OF THE MOBILITIES 
%FOR INSTANCE
%    PmCO2  PmHp PmH2CO3 etc
perm_alpha      = (1/1e-20)*ones(2+2*n_buff,1); %DALE - THIS WAS A BAD VARIABLE NAME (alpha) WHICH IS A KEYWORD IN MATLAB
perm_alpha(1)   =  1/Pm_CO2; %  1/Permeability of CO2
% DALE FUTURE perm_alpha = [ Pm_CO2 Pm_H Pm_H2CO3 Pm_HCO3 Pm_HA Pm_A ] 
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







%(deh INPUT) CO2_in = 0;
%(deh INPUT) pH_in = 7.2;

        
Hplus_in = 10^(-pH_in_init+3);
H2CO3_in = K1*CO2_in;
HCO3m_in = K2*H2CO3_in/Hplus_in;

%(deh INPUT) pKHA1_in = 7.10;  % (Corresponds to a pHi_fin = 7.00)
KHA1_in = 10^(-pKHA1_in+3);

if n_buff >= 2
    %(deh INPUT) kb_HA1_in_plus = 1e10;
    %(deh INPUT) kb_HA1_in_minus = kb_HA1_in_plus/KHA1_in;
    k(5,1:n_in+1) = kb_HA1_in_plus;
    k(6,1:n_in+1) = kb_HA1_in_minus;
    
    % A1tot_in = 27.312560103865501; %mM  (Buffer power of 15.653274417833229 mM/pH)
    %(deh INPUT) A1tot_in = (Buff_pc/100)*A1tot_in; % Immobile Buffer       
    HA1_in = Hplus_in*A1tot_in/(KHA1_in + Hplus_in);
    A1m_in = A1tot_in - HA1_in;
end














% Setting up an initial value vector

u0_in  = CO2_in*ones(n_in+1,1);
u0_out = CO2_out*ones(n_out,1);
u1_in  = H2CO3_in*ones(n_in+1,1);
u1_out = H2CO3_out*ones(n_out,1);
v0_in  = Hplus_in*ones(n_in+1,1);
v0_out = Hplus_out*ones(n_out,1);
v1_in  = HCO3m_in*ones(n_in+1,1);
v1_out = HCO3m_out*ones(n_out,1);

if n_buff == 2
    u2_in  = HA1_in*ones(n_in+1,1);
    u2_out = HA1_out*ones(n_out,1);
    v2_in  = A1m_in*ones(n_in+1,1);
    v2_out = A1m_out*ones(n_out,1);
end

u0     = [u0_in;u0_out]; % CO2
u1     = [u1_in;u1_out]; % H2CO3
v0     = [v0_in;v0_out]; % Hplus
v1     = [v1_in;v1_out]; % HCO3m

if n_buff == 2
    u2     = [u2_in;u2_out]; % HA
    v2     = [v2_in;v2_out]; % Am
end

u = [u0;u1];
v = [v0;v1];
if n_buff == 2
    u = [u;u2];
    v = [v;v2];
end

X0 = [u;v];

% Boundary values
u_inf = [u0_out(1);u1_out(1)];
v_inf = [v0_out(1);v1_out(1)];

if n_buff == 2
    u_inf = [u_inf;u2_out(1)];
    v_inf = [v_inf;v2_out(1)];
end

X_inf = [u_inf;v_inf];

