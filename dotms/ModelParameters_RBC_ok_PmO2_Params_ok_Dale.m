% Model parameters for setting up the experiments and the model for the
% RBC model with paramenter values obtained for ALL Cell types (RBCs +
% precursors)

% Notes: 
% 20200513: RO corrected value for DO2 in water and changed kb(1) to Pan's
% measured value of 11.60

% R. Occhipinti 

% 0. Mouse Type

Mouse_Type = 'WT'; % WT, AQP1-KO, RhAG-KO, dKO

% Choose O2 permeability (alpha) across membrane
%Pm_O2 = 0.15; % 0.15 is Gros value for PCO2 in RBCs
%Pm_O2 = 0.15313;
%Pm_O2 = 0.15314;
%Pm_O2 = 0.15315;
%Pm_O2 = 0.153155;
%Pm_O2 = 0.15315533333333334;
%Pm_O2 = 0.15315566666666666;
%Pm_O2 = 0.15315600000000001;
%Pm_O2 = 0.15315633333333334;
%Pm_O2 = 0.15315666666666666;
%Pm_O2 = 0.153157
%Pm_O2 = 0.15316
%Pm_O2 = 0.15317
Pm_O2 = 0.15318

%0.153155,0.153157
%DALES Pm_O2s:[0.153155, 0.15315533333333334, 0.15315566666666666, 0.15315600000000001, 0.15315633333333334, 0.15315666666666666, 0.153157]
%DALES k_37s:[4.03773607121584, 4.037736259031572, 4.037737124261113, 4.037751623744254, 4.037746402260763, 4.037756753073575, 4.037753769241803]

% hm = 5*10^-7;  % membrane thickness (cm)
% SA = 1;  % surface amplification factor
% Pm_O2 = SA*(1.3313e-5/hm); % equivalent film of water

% Below are the experimental data for each mouse type

if strcmp(Mouse_Type,'WT')
    % Original WT
    R = 1.01e-4;   % Radius of the cell in cm 
    Hbtot_in = 18.73; % mM
    
elseif strcmp(Mouse_Type,'AQP1-KO')
    R = 1.04e-4;   % Radius of the cell in cm 
    Hbtot_in = 17.71; % mM
    
elseif strcmp(Mouse_Type,'RhAG-KO')
    R = 1.09e-4;   % Radius of the cell in cm 
    Hbtot_in = 17.87; % mM
 
elseif strcmp(Mouse_Type,'dKO')
    R = 1.07e-4;   % Radius of the cell in cm 
    Hbtot_in = 18.16; % mM
    
end

% 1. Geometry

% NOTE: For computational reasons you may want to have the units in um
% rather than in cm

R_inf  = R + 1e-4;  % Radius of the computational domain in cm
n_in   = round(R/1e-6); % Discretization inside the cell
R/n_in
n_out  = round((R_inf-R)/1e-6); % Discretization outside the cell 
(R_inf-R)/n_out
N      = n_in + n_out + 1;

O2_pc = 21;  % O2 percent 

n_Hill = 2.7;  % Hill coefficient

% 2. Mobility profile

% NOTE: For computational reasons you may want to have the units in um
% rather than in cm

% Mobility outside the cell. Units in cm2/s
% Order: O2, HbO2, Hb 
% NOTE: Think about D_HBO2 and D_Hb...should they be 0?
% Piecewise constant background profile
kappa_out = [1.3313e-5;  0; 0]; % 1.3313e-5 is DO2 in water
kappa_out = kappa_out*ones(1,n_out);

% Mobility inside the cell
kappa_in  = [2.7745e-6; 6.07e-8; 6.07e-8]; %5.09e-6 (RO); 2.7745e-6 (Arithmetic mean)
kappa_in  = kappa_in*ones(1,n_in+1);

% 3. Transmembrane mobility
% Order: O2, HbO2, Hb...alpha is now permeability
alpha      = zeros(3,1);
alpha(1)   =  Pm_O2; %  Permeability of O2

% General Constants @ 10C (temperature at which Pan does her SF experiments)
PB    = 760;   % mmHg  % UPDATE ???? it does not change
PH2O  = 9.2;   % mmHg  % at t = 10C
sO2   = 2.24e-3; % mM/mmHg O2 solubility @ 10C 
PO2   = O2_pc*(PB-PH2O)/100;  % vapor pressure

PO2_50 = 9.35; %mmHg NOTE: 9.35 according to Roughton 1936 (Fig 1 and Table1). P50 is temperature-dependent (see notebook #1 pp 116-117 for Van't Hoff isochore)

% 4. Initial concentrations. Outside the cell the concentration is assumed to
% be equal to the boundary value

O2_out   = 0; % mM
HbO2_out = 0; % mM
Hb_out = 0; % mM

O2_50 = sO2*PO2_50; % mM (This values is needed to calculate k' = k([O2]^n-1/([O2]_@50)^n)

O2_in = sO2*PO2; % mM

% 5. Reaction rate profiles. Order
% kb(1): HbO2 -> Hb + O2 
% kb(2): Hb + O2 -> HbO2

% NOTE: One rate constant will be constant and the other one will be chosen as a
% function of PO2

kb = NaN(2,1);
kb(1) = 11.60;  % Reaction rate of HbO2 -> Hb + O2  (units: sec^-1) % 35.11 was from literature. 11.60 is value measured by Pan;
kb(2) = kb(1)*(((O2_in).^(n_Hill-1))./(O2_50^n_Hill));%2.43e3;       % Reaction velocity of Hb + O2 -> HbO2  (units: (sec*mM)^-1)
KO2=kb(1)/kb(2);           

k = kb*ones(1,N);

k(:,n_in+2:N) = 0; % No reactions occur in the EUF

HbO2_in = Hbtot_in*((O2_in)^n_Hill)/((O2_in)^n_Hill+KO2); % mM
Hb_in   = Hbtot_in - HbO2_in; %mM

% Setting up an initial value vector
% Note: We assume that the BECF and EUF have no solutes at the beginning

u0_in  = O2_in*ones(n_in+1,1);
u0_out = O2_out*zeros(n_out,1);
u1_in  = HbO2_in*ones(n_in+1,1);
u1_out = HbO2_out*zeros(n_out,1);
u2_in  = Hb_in*ones(n_in+1,1);
u2_out = Hb_out*zeros(n_out,1);

u0     = [u0_in;u0_out]; % O2
u1     = [u1_in;u1_out]; % HbO2
u2     = [u2_in;u2_out]; % Hb

u = [u0;u1;u2];

X0 = u;

% Boundary values (BECF)
u_inf = [u0_out(1);u1_out(1);u2_out(1)];

X_inf = u_inf;
