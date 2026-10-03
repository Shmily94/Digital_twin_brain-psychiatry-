
% fu2 empirical, simulate, manipulate np fcs
[C1,ia,ib]=intersect(simulate_id,fu2_id);
C_simulate_np=simulate_np(ia,:);

[C2,ia,ib]=intersect(ampa_id,fu2_id);
C_ampa_np=ampa_np(ia,:);

[C3,ia,ib]=intersect(gaba_id,fu2_id);
C_gaba_np=gaba_np(ia,:);

[C4,ia,ib]=intersect(empirical_id,C3);
C_empirical_np=empirical_np(ia,:);
C_C_simulate_np=C_simulate_np(ib,:);
C_C_ampa_np=C_ampa_np(ib,:);
C_C_gaba_np=C_gaba_np(ib,:);

[C5,ic,id]=intersect(beha_id,C4);
C_beha_data=beha_data(ic,:);
C_C_empirical_np=C_empirical_np(id,:);
C_C_C_simulate_np=C_C_simulate_np(id,:);
C_C_C_ampa_np=C_C_ampa_np(id,:);
C_C_C_gaba_np=C_C_gaba_np(id,:);

[C6,ic,id]=intersect(fu3_beha_id,C5);
C_fu3_beha_data=fu3_beha_data(ic,:);
C_C_beha_data=C_beha_data(id,:);
C_C_C_empirical_np=C_C_empirical_np(id,:);
C_C_C_C_simulate_np=C_C_C_simulate_np(id,:);
C_C_C_C_ampa_np=C_C_C_ampa_np(id,:);
C_C_C_C_gaba_np=C_C_C_gaba_np(id,:);

% 1.predict beha using empirical np
NP_real = C_C_empirical_np;   % ✅ 基线真实 np
NP_sim  = C_C_C_simulate_np;   % ✅ 模拟 np
NP_mod  = C_C_C_ampa_np;   % ✅ 调控 np
NP_mod_gaba  = C_C_C_gaba_np;  

Behav_base   = C_beha_data;   % 基线行为
Behav_follow = C_fu3_beha_data;   % 随访行为

X_train = NP_real;   % [N × 13]
y_train = sum(Behav_base(:,3:6),2);              % 预测基线行为adhd，cd，eat，dep，gad，sp

mdl_base = fitlm(X_train, y_train);

disp(mdl_base);

% 2.虚拟调控行为改善分数
% --- 用模拟 NP ---
X_sim = NP_sim;
Behav_pred_sim = predict(mdl_base, X_sim);

% --- 用调控 NP ---
X_mod = NP_mod;
X_mod_gaba = NP_mod_gaba;

Behav_pred_mod = predict(mdl_base, X_mod);
Behav_pred_mod_gaba = predict(mdl_base, X_mod_gaba);

Delta_Behav_mod = Behav_pred_mod - Behav_pred_sim; % 负值代表症状改善
Delta_Behav_mod_gaba = Behav_pred_mod_gaba - Behav_pred_sim; % 负值代表症状改善

% 3.predicte real beha changes using virtual changes
Delta_Behav_real = sum(C_fu3_beha_data(:,3:6),2) - sum(C_C_beha_data(:,3:6),2);
C_Delta_Behav_mod = Delta_Behav_mod(id,:);
C_Delta_Behav_mod_gaba = Delta_Behav_mod_gaba(id,:);

Delta_Behav_real(64,:)=[];
C_Delta_Behav_mod(64,:)=[];
C_Delta_Behav_mod_gaba(64,:)=[];
C_C_C_empirical_np(64,:)=[];
C_C_beha_data(64,:)=[];

%X_final = [C_C_beha_data(:,3:6)];   % 1 + 12 = 13 维
X_final = [C_Delta_Behav_mod_gaba,C_C_beha_data(:,3:6)];   % 1 + 12 = 13 维

%X_final = [C_Delta_Behav_mod, C_C_C_empirical_np];   % 1 + 12 = 13 维
%X_final = [C_Delta_Behav_mod, C_C_beha_data(:,3:6), C_C_C_empirical_np];   % 1 + 12 = 13 维

y_final = Delta_Behav_real;
mdl_final = fitlm(X_final, y_final);
disp(mdl_final);
R2  = mdl_final.Rsquared.Ordinary;
p_gain = mdl_final.Coefficients.pValue(2);      % ΔBehav_mod 的 p 值
fprintf('Final model R² = %.3f\n', R2);
fprintf('DTB-predicted behavioral gain p = %.6f\n', p_gain);

R2_real  = mdl_final.Rsquared.Ordinary;
beta_real = mdl_final.Coefficients.Estimate(2);
p_real    = mdl_final.Coefficients.pValue(2);
%%
% 简化模型
X1 = C_C_beha_data(:,3:6);
mdl_reduced = fitlm(X1, y_final);

% 完整模型
X2 = [C_Delta_Behav_mod, C_C_beha_data(:,3:6)];
mdl_full = fitlm(X2, y_final);

% 嵌套模型显著性比较（F-test）
R2_reduced = mdl_reduced.Rsquared.Ordinary; 
R2_full    = mdl_full.Rsquared.Ordinary;

n  = length(y_final);        % 样本量
p1 = size(X1,2);             % 简化模型自变量个数
p2 = size(X2,2);             % 完整模型自变量个数

F_change = ((R2_full - R2_reduced)/(p2 - p1)) / ...
           ((1 - R2_full)/(n - p2 - 1));

p_change = 1 - fcdf(F_change, p2-p1, n-p2-1);

fprintf('ΔR² = %.4f\n', R2_full - R2_reduced);
fprintf('F-change = %.4f, p = %.6f\n', F_change, p_change);



%% ================================
%  Permutation Test for DTB Effect
% ================================

Nperm = 5000;   % ✅ 1000 可跑，5000 更稳
R2_perm = zeros(Nperm,1);
beta_perm = zeros(Nperm,1);

rng(1);  % 固定随机种子，保证可复现

for p = 1:Nperm

    % 1️⃣ 打乱真实行为改变（破坏因果关系）
    y_perm = y_final(randperm(length(y_final)));

    % 2️⃣ 在"完全相同的特征矩阵"上重新拟合模型
    mdl_perm = fitlm(X_final, y_perm);

    % 3️⃣ 记录 null 分布中的统计量
    R2_perm(p)   = mdl_perm.Rsquared.Ordinary;
    beta_perm(p) = mdl_perm.Coefficients.Estimate(2);

end

% 4️⃣ 计算 permutation p 值（R² 版本）
p_perm_R2 = mean(R2_perm >= R2_real);

% 5️⃣ 计算 permutation p 值（回归系数版本）
p_perm_beta = mean(abs(beta_perm) >= abs(beta_real));

fprintf('\n===== Permutation Test Results =====\n');
fprintf('Empirical R² = %.4f\n', R2_real);
fprintf('Permutation p (R²) = %.5f\n', p_perm_R2);

fprintf('Empirical beta = %.4f\n', beta_real);
fprintf('Permutation p (beta) = %.5f\n', p_perm_beta);