%% predict drug-related mid fcs changes from mid fcs of placebo

%baseline_290=mid_fcs;
%outcome_290=diff_mid;
%baseline_27=placebo;
%outcome_27_true=diff_drug;

valid_idx = ~any(isnan([baseline_290 outcome_290]), 2);
baseline_290_clean = baseline_290(valid_idx);
outcome_290_clean  = outcome_290(valid_idx, :);

%train model using dtb data

mdl_reg1 = fitlm(baseline_290_clean, outcome_290_clean(:,1)); % ampa
mdl_reg2 = fitlm(baseline_290_clean, outcome_290_clean(:,2)); % gaba-a

% predict test outcome using drug-related data
pred_outcome1 = predict(mdl_reg1, baseline_27); % predict ketamine
pred_outcome2 = predict(mdl_reg2, baseline_27); % predict midazolam
pred_outcome  = [pred_outcome1 pred_outcome2];

%predict change direction
pred_sign = sign(pred_outcome);       % -1, 0, or +1
true_sign = sign(outcome_27_true);

%classification accuracy
acc_1 = mean(pred_sign(:,1) == true_sign(:,1));
acc_2 = mean(pred_sign(:,2) == true_sign(:,2));

fprintf('Outcome 1 sign prediction accuracy: %.2f%%\n', acc_1*100);
fprintf('Outcome 2 sign prediction accuracy: %.2f%%\n', acc_2*100);

%Significance testing - permutation
n_perm = 1000;
n_test = length(true_sign(:,1));

r_pred1 = corr(pred_outcome1, outcome_27_true(:,1));
r_pred2 = corr(pred_outcome2, outcome_27_true(:,2));

r_perm1 = zeros(n_perm,1);
r_perm2 = zeros(n_perm,1);
for i = 1:n_perm
    perm_idx = randperm(n_test);
    r_perm1(i) = corr(pred_outcome1, outcome_27_true(perm_idx,1));
    r_perm2(i) = corr(pred_outcome2, outcome_27_true(perm_idx,2));
end

p_perm1 = mean(r_perm1 >= r_pred1);
p_perm2 = mean(r_perm2 >= r_pred2);
fprintf('Regression permutation test p-values: Outcome1 %.4f, Outcome2 %.4f\n', p_perm1, p_perm2);


