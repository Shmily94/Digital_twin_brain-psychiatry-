%% ===============================

%baseline_290=mid_fcs;
%outcome_290=diff_mid;
%baseline_27=placebo;
%outcome_27_true=diff_drug;

%% ======== Step 1: 清洗数据（去掉 NaN 行）=========
%valid_idx = ~any(isnan([baseline_290 outcome_290]), 2);
%baseline_290_clean = baseline_290(valid_idx);
%outcome_290_clean  = outcome_290(valid_idx, :);

%% ======== Step 2: 训练回归模型（预测 outcome 数值） ========

mdl_reg1 = fitlm(baseline_290_clean, outcome_290_clean(:,1)); % outcome1
mdl_reg2 = fitlm(baseline_290_clean, outcome_290_clean(:,2)); % outcome2

% 预测 27 个新的 outcome
pred_outcome1 = predict(mdl_reg1, baseline_27); % predict ketamine
pred_outcome2 = predict(mdl_reg2, baseline_27); % predict midazolam
pred_outcome  = [pred_outcome1 pred_outcome2];

%% ======== Step 3: 预测 outcome 的正/负性 ========
pred_sign = sign(pred_outcome);       % -1, 0, or +1
true_sign = sign(outcome_27_true);

%% ======== Step 4: 评估分类准确率 ========
acc_1 = mean(pred_sign(:,1) == true_sign(:,1));
acc_2 = mean(pred_sign(:,2) == true_sign(:,2));

fprintf('Outcome 1 sign prediction accuracy: %.2f%%\n', acc_1*100);
fprintf('Outcome 2 sign prediction accuracy: %.2f%%\n', acc_2*100);

%% ======== Step 5: （可选）使用 SVM 做分类（正负）========
% 构建标签
label1 = sign(outcome_290_clean(:,1));  % 分类标签
label2 = sign(outcome_290_clean(:,2));  % 分类标签

% 去掉 sign = 0 的数据
idx1 = label1 ~= 0;
idx2 = label2 ~= 0;

% 训练 SVM（使用 Gaussian RBF 内核）
svm1 = fitcsvm(baseline_290_clean(idx1), label1(idx1), ...
               'KernelFunction', 'rbf', 'Standardize', true);

svm2 = fitcsvm(baseline_290_clean(idx2), label2(idx2), ...
               'KernelFunction', 'rbf', 'Standardize', true);

% 预测
svm_pred1 = predict(svm1, baseline_27);
svm_pred2 = predict(svm2, baseline_27);

% 准确率
svm_acc1 = mean(svm_pred1 == true_sign(:,1));
svm_acc2 = mean(svm_pred2 == true_sign(:,2));

fprintf('SVM Outcome 1 sign accuracy: %.2f%%\n', svm_acc1 * 100);
fprintf('SVM Outcome 2 sign accuracy: %.2f%%\n', svm_acc2 * 100);


%% ===== Step 4: Significance testing - permutation =====
n_perm = 1000;
n_test = length(true_sign(:,1));

% ---- Regression permutation test (correlation) ----
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

% ---- Classification permutation test (sign accuracy) ----
acc_perm1 = zeros(n_perm,1);
acc_perm2 = zeros(n_perm,1);
for i = 1:n_perm
    label_perm1 = true_sign(randperm(n_test),1);
    label_perm2 = true_sign(randperm(n_test),2);
    acc_perm1(i) = mean(svm_pred1 == label_perm1);
    acc_perm2(i) = mean(svm_pred2 == label_perm2);
end

p_acc1 = mean(acc_perm1 >= svm_acc1);
p_acc2 = mean(acc_perm2 >= svm_acc2);
fprintf('SVM permutation p-values: Outcome1 %.4f, Outcome2 %.4f\n', p_acc1, p_acc2);

%midazolam
scores = pred_outcome2;       % 27x1 连续预测值
true_sign = sign(outcome_27_true(:,2));  % -1 / 0 / +1
idx = true_sign ~= 0;  % 去掉 0 (neutral)
y_true = true_sign(idx);
y_true(y_true==-1) = 0;  % 负类 = 0, 正类 = 1
y_scores = scores(idx);  % 对应的预测分数
[X,Y,T,AUC] = perfcurve(y_true, y_scores, 1);  % 1 表示正类
figure;
plot(X,Y,'LineWidth',2);
hold on;
plot([0 1],[0 1],'--k'); % 对角线，表示随机预测
xlabel('False Positive Rate');
ylabel('True Positive Rate');
title(sprintf('ROC Curve (AUC = %.3f)', AUC));
grid on;


%ketamine
scores = pred_outcome1;       % 27x1 连续预测值
true_sign = sign(outcome_27_true(:,1));  % -1 / 0 / +1
idx = true_sign ~= 0;  % 去掉 0 (neutral)
y_true = true_sign(idx);
y_true(y_true==-1) = 0;  % 负类 = 0, 正类 = 1
y_scores = scores(idx);  % 对应的预测分数
[X,Y,T,AUC] = perfcurve(y_true, y_scores, 1);  % 1 表示正类
figure;
plot(X,Y,'LineWidth',2);
hold on;
plot([0 1],[0 1],'--k'); % 对角线，表示随机预测
xlabel('False Positive Rate');
ylabel('True Positive Rate');
title(sprintf('ROC Curve (AUC = %.3f)', AUC));
grid on;