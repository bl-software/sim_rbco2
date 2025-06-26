% The RHS for ode solver corresponding to a distributed model, i.e., the
% diffusion and reaction velocities need not be constants. 
% In this file we implement the effect of the volume fraction (Vf) in the
% model by scaling the reaction term of the RHS describing the cell (inside
% and boundary) by Vf. 
% We also implement BC at infinity that change exponentially with time to simulate the CO2/HCO3
% addition and removal 
%
% D. Calvetti, R. Occhipinti, E. Somersalo
%
function Y = ReactionDiffusionDistrRHS_React_ExpRamp(t,X,Params,tf_CO2on)

%disp(['time = ' num2str(t)]);
%Params;
% Disentangling the model parameters
A      = Params.DiffusionMatrix;
W      = Params.BoundaryVector;
k      = Params.ReactionRates;
X_inf_ss  = Params.BoundaryValues;
N      = Params.N;
n_buff = Params.NumberOfBuffers;
n_in   = Params.n_in;
n_out  = Params.n_out;

% Give flow
       
t1 = tf_CO2on;
tau_valve1 = 4;  % Time constant for flow delivery/removal 
tau_valve2 = 4;  %6

if t<t1  % Delivery CO2/HCO3m solution
    X_inf = X_inf_ss.*(1-exp(-t/tau_valve1));
    X_inf(3) = X_inf_ss(3); % HA
    X_inf(4) = X_inf_ss(4); % Hplus
    X_inf(6) = X_inf_ss(6); % Am
elseif t>=t1 % Remove CO2/HCO3m solution
    X_inf = X_inf_ss.*(exp(-(t-t1)/tau_valve2));
    X_inf(3) = X_inf_ss(3); % HA
    X_inf(4) = X_inf_ss(4); % Hplus
    X_inf(6) = X_inf_ss(6); % Am
end

% Diffusion part, including dirichlet boundary values at outer boundary
Y = A*X + W*X_inf;     

% Scaling the reaction term by Vf
% n_in = 80;
% n_out = 50;
H2O_pc = (1/.40);
k(:,1:n_in+1) = H2O_pc*k(:,1:n_in+1);

% %Scaling the Diffusion term only
% for jj = 1:6
%     Y((jj-1)*N+1:jj*N-n_out) = (.40)*Y((jj-1)*N+1:jj*N-n_out);
%          end

% Adding the CO2 feed
Y(1:N)     = Y(1:N)     - k(1,:)'.*X(1:N) + k(2,:)'.*X(N+1:2*N);
Y(N+1:2*N) = Y(N+1:2*N) + k(1,:)'.*X(1:N) - k(2,:)'.*X(N+1:2*N);

% Adding the equilibrium reactions

indj = 2; 
XH = X(N*(n_buff+1)+1:N*(n_buff+2));     % H+ concentration
for j = 1:n_buff
    indj = indj + 1;
    aux = -k(indj,:)'.*X(N*j+1:N*(j+1));
    indj = indj + 1;
    aux = aux + k(indj,:)'.*XH.*X(N*(n_buff+1+j)+1:N*(n_buff+2+j));
    Y(N*j+1:N*(j+1)) = Y(N*j+1:N*(j+1)) + aux;
    Y(N*(n_buff+1+j)+1:N*(n_buff+2+j)) =  ...
        Y(N*(n_buff+1+j)+1:N*(n_buff+2+j)) - aux;
    Y(N*(n_buff+1)+1:N*(n_buff+2)) = Y(N*(n_buff+1)+1:N*(n_buff+2)) - aux;
end
   
% n_out = 50;
% %water_pc = .40;
% 
% Scaling the RHS (both diffusion and reaction terms)
% for jj = 1:6
%     Y((jj-1)*N+1:jj*N-n_out) = (1/.40)*Y((jj-1)*N+1:jj*N-n_out);
% end

