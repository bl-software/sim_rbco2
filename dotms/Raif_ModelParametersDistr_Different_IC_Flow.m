% Model parameters for setting up the experiments and the model for Raif
% CAII and CAIV papers
%
% To run an experiment you need to choose the oocyte type and the percentage of CO2
%
fprintf(' -> **************************************\n')
fprintf('    * In Raif_ModelParametersDistr_....m *\n')
fprintf('    **************************************\n')
% 1. Geometry

%R      = 0.13/2;   % Radius of the cell in cm
%(deh DEFAULT)
%R_inf  = 0.132/2;   % Radius of the computational domain in cm
%n_in   = 80;       % Discretization inside the cell
%n_out  = 10;       % Discretization outside the cell (you need to change it depending on the size of R_inf)
%N      = n_in + n_out + 1;
%n_buff = 2;
%rad_in = (R/n_in)*[0:n_in];
%rad_out  = R + ((R_inf-R)/(n_out))*[0:n_out];

% Choose oocyte type
%oocyte_type = 'Tris';  % 'Tris', 'H2O', 'CAII', 'CAIV'

% Choose experiment
%CO2_pc = 1.5;  % CO2 percent 1.5, 5, 10

% Choose CO2 permeability (alpha) across membrane
%hm = 5*10^-7;  % membrane thickness (cm)
%SA = 9;  % surface amplification factor
%Pm_CO2 = (SA*(1.71e-5/hm))/10000; 

% Flags to control the implementation of some features
%ADD CAII_flag_out = 0; % addition (1) or not (0) of extracellular carbonic anhydrase II (CAII) 
%CAII_flag = 1; % addition (1) or not (0) of carbonic anhydrase II (CAII) 
%CAIV_flag = 1; % addition (1) or not (0) of carbonic anhydrase IV (CAIV) 
%layer_in_mem = 1; % mobility below the membrane (vesicles) smaller
%(deh ADD DONE) vit_mem = 1;  % vitelline membrane

% Implement CAII and CAIV activity
%A_CAII = 1;
%(deh DEFAULT)
%CAII_in =A_CAII*5; % Acceleration factor for CAII activity
%A_CAIV = 1;
%(deh DEFAULT)
%CAIV_out = A_CAIV*150; % Acceleration factor for CAIV activity

%(deh ADD DONE) CAII_out = 0;

% 2. Mobility profile
% Mobility outside the cell. Units in cm2/s
% Order: CO2, H+, H2CO3, HCO3-
% Add buffers: HA1, A1, HA2, A2, ...
% Piecewise constant background profile
%kappa_out = [1.71e-5;  8.69e-5; 1.11e-5; 1.11e-5];
%kappa_out = kappa_out*ones(1,n_out);

% Mobility inside the cell
%kappa_in  = [1.71e-5;  8.69e-5; 1.11e-5; 1.11e-5];
%kappa_in  = kappa_in*ones(1,n_in+1);

% Mobility of buffers
%if n_buff == 2
%   kappaBuff_in  = [1.56e-5; 1.56e-5]; 
%   kappaBuff_out = [1.56e-5; 1.56e-5]; 
%   kappaBuff_in = kappaBuff_in*ones(1,n_in+1);
%   kappaBuff_out = kappaBuff_out*ones(1,n_out);
%(deh DEFAULT or PARAM)
%   kappa_in  = .5*[kappa_in;kappaBuff_in]; % Correction for cytoplasm (see Vaughan-Jones 2005)
%   kappa_out = [kappa_out;kappaBuff_out];
%end

%if vit_mem == 1
%    Red_factor = .03; % reduction factor
%    kappa_out(:,1) = Red_factor*kappa_out(:,1); % implement vitelline membrane
%end

% Adding a layer of lower mobility (vesicles)
%if layer_in_mem == 1
%    d1 = 10;      %  distance of the layer from the surface (membrane) in microns
%    d1 = 1e-4*d1;  % d in centimeters
%    ind1 = find(rad_in <= R-d1);
%(deh DEFAULT)
%    d2 = 30;      % depth of the layer in microns
%    d2 = 1e-4*d2; % d in centimeters
%    ind2 = find(rad_in < R-(d1+d2));
%    ind = setdiff(ind1,ind2);
%(deh DEFAULT)
%    tiny = .10;  % reduce mobility in the layer
%    kappa_in(1:end,ind) = tiny*kappa_in(1:end,ind);
%end

% 3. Reaction rate profiles. Order
% kb(1) : CO2 + H2O -> H2CO3  , background value
% kb(2) : H2CO3 -> CO2 + H2O
% kb(3) : H2CO3 -> HCO3- + H+
% kb(4) : HCO3- + H+ -> H2CO3
% Add buffers : k(5) HA1 -> A1- + H+
%               k(6) A1- + H+ -> HA1    etc.
% Constant background
%kb = NaN(2*(1+n_buff),1);
%kb(1) = 0.0302;        % Reaction rate of CO2 + H2O --> H2CO3  (s^-1)
%kb(2) = 10.9631;       % Reaction velocity of H2CO3 --> CO2 + H2O  (s^-1)
%K1=kb(1)/kb(2);           
%pK2 = 3.618357367951740;   % Dissociation const for carbonic acid
%K2   = 10^(-pK2+3);   % Units in mM
%kb(3) = 1e16;         % This value is a guess chosen to satisfy the equilibrium
%kb(4) = kb(3)/K2;
%pK_CO2 = -log10(K1)+pK2; % overall pK for CO2/HCO3m

%if n_buff == 2
%   pKHA_out = 7.5; 
%   KHA_out  = 10^(-pKHA_out+3);
%   kb(5) = 1e10;
%   kb(6) = kb(5)/KHA_out;
%end
%k = kb*ones(1,N);

% Adding carbonic anhydrase II everywhere inside the oocyte
%if CAII_flag == 1
%    ind_in = find(rad_in<=R);
%    k(1:2,ind_in) = CAII_in*k(1:2,ind_in); 
%end
%
% Adding carbonic anhydrase IV at 5nm above the membrane
%if CAIV_flag == 1
%    d = .005;      %  CAIV layer in microns
%    d = 1e-4*d;  % d in centimeters
%    ind_out = min(n_in+find(rad_out > R+d));  %outside
%    k(1:2,ind_out) = CAIV_out*k(1:2,ind_out); 
%end

% Adding carbonic anhydrase II everywhere outside
%if CAII_flag_out == 1
%    k(1:2,ind_out+1:end) = CAII_out*k(1:2,ind_out+1:end);
%end

% 4. Transmembrane mobility

%perm_alpha      = (1/1e-20)*ones(2+2*n_buff,1);
%perm_alpha(1)   =  1/Pm_CO2; %  1/Permeability of CO2

% General Constants @ 22C (room temperature)
%PB     = 760;   % mmHg
%PH2O   = 35;  % mmHg
%sCO2   = 0.0434; % mM/mmHg CO2 solubility @ 22C
%PCO2   = CO2_pc*(PB-PH2O)/100;

% 5. Initial concentrations. Outside the cell the concentration is assumed to
% be equal to the boundary value

%CO2_out    = sCO2*PCO2; %mM
%pH_out     = 7.5;
%Hplus_out  = 10^(-pH_out+3); % mM
%H2CO3_out  = K1*CO2_out;
%HCO3m_out  = (K2*H2CO3_out)/Hplus_out;

%if n_buff == 2
%    Atot_out   = 5; % mM
%    HA_out     = Hplus_out*Atot_out/(KHA_out + Hplus_out);
%    Am_out     = Atot_out - HA_out;
%end

%CO2_in = 0;

% Select the correct initial intracellular pH (pH_in_i) using Raif mean
% values for pH_in_i and pH_in_fin
if CO2_pc == 1.5
    if strcmp(oocyte_type, 'Tris')
        pH_in_init = 7.22; 
        pH_in_acid = 6.99; 
    elseif strcmp(oocyte_type, 'H2O')
        pH_in_init = 7.28;
        pH_in_acid = 7.01; 
    elseif strcmp(oocyte_type, 'CAII')
        pH_in_init = 7.21;
        pH_in_acid = 6.98; 
    elseif strcmp(oocyte_type, 'CAIV')
        pH_in_init = 7.40;
        pH_in_acid = 7.06; 
    end
elseif CO2_pc == 5
    if strcmp(oocyte_type, 'Tris')
        pH_in_init = 7.24;
        pH_in_acid = 6.79; 
    elseif strcmp(oocyte_type, 'H2O')
        pH_in_init = 7.23;
        pH_in_acid = 6.84; 
    elseif strcmp(oocyte_type, 'CAII')
        pH_in_init = 7.21;
        pH_in_acid = 6.77; 
    elseif strcmp(oocyte_type, 'CAIV')
        pH_in_init = 7.37;
        pH_in_acid = 6.79; 
    end
elseif CO2_pc == 10
    if strcmp(oocyte_type, 'Tris')
        pH_in_init = 7.18;
        pH_in_acid = 6.67; 
    elseif strcmp(oocyte_type, 'H2O')
        pH_in_init = 7.16;
        pH_in_acid = 6.69; 
    elseif strcmp(oocyte_type, 'CAII')
        pH_in_init = 7.21;
        pH_in_acid = 6.66; 
    elseif strcmp(oocyte_type, 'CAIV')
        pH_in_init = 7.40;
        pH_in_acid = 6.61; 
    end
end
        
%Hplus_in = 10^(-pH_in_init+3);
%H2CO3_in = K1*CO2_in;
%HCO3m_in = K2*H2CO3_in/Hplus_in;

if n_buff == 2
    [A1tot_in pKHA1_in beta_mean] = CalculateTotalBuffer(pH_in_init,pH_in_acid,HCO3m_in,CO2_out,pK_CO2);
    KHA1_in = 10^(-pKHA1_in+3);
    
    %kb_HA1_in_plus = 1e10;
    %kb_HA1_in_minus = kb_HA1_in_plus/KHA1_in;
    k(5,1:n_in+1) = kb_HA1_in_plus;
    k(6,1:n_in+1) = kb_HA1_in_minus;
    
    HA1_in = Hplus_in*A1tot_in/(KHA1_in + Hplus_in);
    A1m_in = A1tot_in - HA1_in;
end

























































% Setting up an initial value vector for simulations with zero CO2, HCO3-
% and H2CO3 in the eUL

u0_in      = CO2_in    *ones(n_in+1,1);
u0_out     = CO2_out   *zeros(n_out,1);
u1_in      = H2CO3_in  *ones(n_in+1,1);
u1_out     = H2CO3_out *zeros(n_out,1);
v0_in      = Hplus_in  *ones(n_in+1,1);
v0_out     = Hplus_out *ones(n_out ,1);
v1_in      = HCO3m_in  *ones(n_in+1,1);
v1_out     = HCO3m_out *zeros(n_out,1);
if n_buff == 2
    u2_in  = HA1_in    *ones(n_in+1,1);
    u2_out = HA1_out   *ones(n_out ,1);
    v2_in  = A1m_in    *ones(n_in+1,1);
    v2_out = A1m_out   *ones(n_out ,1);
end







u0     = [u0_in; u0_out]; % CO2
u1     = [u1_in; u1_out]; % H2CO3
v0     = [v0_in; v0_out]; % Hplus
v1     = [v1_in; v1_out]; % HCO3m

if n_buff == 2
    u2 = [u2_in; u2_out]; % HA
    v2 = [v2_in; v2_out]; % Am
end

u = [u0;u1];
v = [v0;v1];
if n_buff == 2
    u = [u;u2];
    v = [v;v2];
end

X0 = [u;v];

% Boundary values
u_inf = [CO2_out;   H2CO3_out];
v_inf = [Hplus_out; HCO3m_out];

if n_buff == 2
    u_inf = [u_inf; HA_out];
    v_inf = [v_inf; Am_out];
end

X_inf = [u_inf;v_inf];

