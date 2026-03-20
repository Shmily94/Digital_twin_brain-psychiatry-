%% predict empirical behavioral symptom changes after 4 years

%empirical, simulate, manipulate np fcs at 19 years old

NP_real = empirical_np;  
NP_sim  = simulate_np;   
NP_mod  = ampa_np;  
NP_mod_gaba  = gaba_np;  

Behav_base   = beha_data;   % behavioral symptom score at 19
Behav_follow = fu3_beha_data;   % internalizing symptom score at 23

X_train = NP_real; 
y_train = sum(Behav_base(:,3:6),2);    % internalizing symptom score at 19
mdl_base = fitlm(X_train, y_train);
disp(mdl_base);

%predict behavioral symptom changes after virtual modulations
X_sim = NP_sim;
Behav_pred_sim = predict(mdl_base, X_sim);

X_mod = NP_mod;
Behav_pred_mod = predict(mdl_base, X_mod);

X_mod_gaba = NP_mod_gaba;
Behav_pred_mod_gaba = predict(mdl_base, X_mod_gaba);

Delta_Behav_mod = Behav_pred_mod - Behav_pred_sim; % negative value means symptom get lower
Delta_Behav_mod_gaba = Behav_pred_mod_gaba - Behav_pred_sim; 

%predicte empirical beha changes using virtual symptom changes index

Delta_Behav_real = sum(fu3_beha_data(:,3:6),2) - sum(beha_data(:,3:6),2);

X_final = [Delta_Behav_mod,beha_data(:,3:6)];   % restoration index + baseline symptom
y_final = Delta_Behav_real;
mdl_final = fitlm(X_final, y_final);
disp(mdl_final);
R2  = mdl_final.Rsquared.Ordinary;
p_gain = mdl_final.Coefficients.pValue(2);      % ΔBehav_mod p value
fprintf('Final model R² = %.3f\n', R2);
fprintf('DTB-predicted behavioral gain p = %.6f\n', p_gain);

R2_real  = mdl_final.Rsquared.Ordinary;
beta_real = mdl_final.Coefficients.Estimate(2);
p_real    = mdl_final.Coefficients.pValue(2);

% compare model
X1 = beha_data(:,3:6);
mdl_reduced = fitlm(X1, y_final);

X2 = [Delta_Behav_mod, beha_data(:,3:6)];
mdl_full = fitlm(X2, y_final);

%F-test
R2_reduced = mdl_reduced.Rsquared.Ordinary; 
R2_full    = mdl_full.Rsquared.Ordinary;
n  = length(y_final);        
p1 = size(X1,2);             
p2 = size(X2,2);             

F_change = ((R2_full - R2_reduced)/(p2 - p1)) / ...
           ((1 - R2_full)/(n - p2 - 1));

p_change = 1 - fcdf(F_change, p2-p1, n-p2-1);

fprintf('ΔR² = %.4f\n', R2_full - R2_reduced);
fprintf('F-change = %.4f, p = %.6f\n', F_change, p_change);

%Permutation Test 
Nperm = 5000; 
R2_perm = zeros(Nperm,1);
beta_perm = zeros(Nperm,1);

rng(1); 

for p = 1:Nperm
  y_perm = y_final(randperm(length(y_final)));
  mdl_perm = fitlm(X_final, y_perm);
  R2_perm(p)   = mdl_perm.Rsquared.Ordinary;
  beta_perm(p) = mdl_perm.Coefficients.Estimate(2);
end

p_perm_R2 = mean(R2_perm >= R2_real);

%
p_perm_beta = mean(abs(beta_perm) >= abs(beta_real));

fprintf('\n===== Permutation Test Results =====\n');
fprintf('Empirical R² = %.4f\n', R2_real);
fprintf('Permutation p (R²) = %.5f\n', p_perm_R2);

fprintf('Empirical beta = %.4f\n', beta_real);
fprintf('Permutation p (beta) = %.5f\n', p_perm_beta);