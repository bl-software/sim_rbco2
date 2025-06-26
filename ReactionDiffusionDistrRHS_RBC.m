% The RHS for ode solver corresponding to a distributed model, i.e., the
% diffusion and reaction velocities need not be constants
%
% R. Occhipinti
%
function Y = ReactionDiffusionDistrRHS_RBC(t,X,Params)

%disp(['time = ' num2str(t)]);

% Dissentangling the model parameters
A      = Params.DiffusionMatrix;
W      = Params.BoundaryVector;
k      = Params.ReactionRates;
X_inf  = Params.BoundaryValues;
N      = Params.N;
n_Hill = Params.HillCoeff; 
O2_50  = Params.O2_50;

% Diffusion part, including dirichlet boundary values at outer boundary
Y = A*X + W*X_inf;     
   
X_O2 = X(1:N); % O2 concentration
X_HbO2 = X(N+1:2*N); % HbO2 concetration
X_Hb = X(2*N+1:3*N); % Hb concentration

% Variable rate coefficient model 
k_calc(2,:) = k(1,:).*(((X_O2').^(n_Hill-1))./(O2_50^n_Hill)); 
%k_calc(2,:) = k(2,:);

% plot(k_calc(2,30),'*')
% hold on
% %size(k_calc(2,:))
% 
% %test = k_calc(2,:)-k(2,:)
% %pause

% Adding equilibrium reactions

Y(1:N)       = Y(1:N)       + k(1,:)'.*X_HbO2 - k_calc(2,:)'.*X_Hb.*X_O2; % O2
Y(N+1:2*N)   = Y(N+1:2*N)   - k(1,:)'.*X_HbO2 + k_calc(2,:)'.*X_Hb.*X_O2; % HbO2
Y(2*N+1:3*N) = Y(2*N+1:3*N) + k(1,:)'.*X_HbO2 - k_calc(2,:)'.*X_Hb.*X_O2; % Hb
    
