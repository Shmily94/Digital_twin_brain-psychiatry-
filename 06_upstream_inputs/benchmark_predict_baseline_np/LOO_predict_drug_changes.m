load('/Users/yunman/Desktop/submission/figures/fig4/predict_drug_response_use_placebo_mid/predict_drug_response2.mat');
X = baseline_27;
n = length(X);
y_pred_ket_loo = zeros(n, 1);
y_pred_mid_loo = zeros(n, 1);

for i = 1:n
    % 留出第i个被试
    idx = true(n, 1);
    idx(i) = false;
    
    % Ketamine
    mdl_ket_cv = fitlm(X(idx), outcome_27_true(idx,1));
    y_pred_ket_loo(i) = predict(mdl_ket_cv, X(i));
    
    % Midazolam
    mdl_mid_cv = fitlm(X(idx), outcome_27_true(idx,2));
    y_pred_mid_loo(i) = predict(mdl_mid_cv, X(i));
end

% 计算LOO的R²和相关
[r_ket, p_ket] = corr(y_pred_ket_loo, outcome_27_true(:,1));
[r_mid, p_mid] = corr(y_pred_mid_loo, outcome_27_true(:,2));

fprintf('Ketamine LOO: r=%.3f, R2=%.3f, p=%.3f\n', r_ket, r_ket^2, p_ket);
fprintf('Midazolam LOO: r=%.3f, R2=%.3f, p=%.3f\n', r_mid, r_mid^2, p_mid);

figure;

% Ketamine
subplot(1,2,1);
hold on;
scatter(outcome_27_true(:,1), y_pred_ket_loo, 60, 'filled', ...
    'MarkerFaceColor', [0.2 0.4 0.8], 'MarkerFaceAlpha', 0.7);
all_vals = [outcome_27_true(:,1); y_pred_ket_loo];
lims = [min(all_vals)-0.05*range(all_vals), max(all_vals)+0.05*range(all_vals)];
plot(lims, lims, 'k--', 'LineWidth', 1.5);
p = p_ket;
plot(linspace(lims(1),lims(2),100), polyval(p,linspace(lims(1),lims(2),100)), 'r-', 'LineWidth', 2);
text(0.05, 0.92, sprintf('R^2 = %.3f', mdl_ket_cv.Rsquared.Ordinary), 'Units','normalized','FontSize',11);
text(0.05, 0.84, sprintf('adj R^2 = %.3f', mdl_ket_cv.Rsquared.Adjusted), 'Units','normalized','FontSize',11);
text(0.05, 0.76, sprintf('p = %.3f', mdl_ket_cv.Coefficients.pValue(2)), 'Units','normalized','FontSize',11);
xlabel('Actual \DeltaBehavior','FontSize',12);
ylabel('Predicted \DeltaBehavior','FontSize',12);
title('Ketamine','FontSize',13);
xlim(lims); ylim(lims); axis square; box on;
hold off;

% Midazolam
subplot(1,2,2);
hold on;
scatter(outcome_27_true(:,2), y_pred_mid_loo, 60, 'filled', ...
    'MarkerFaceColor', [0.8 0.3 0.2], 'MarkerFaceAlpha', 0.7);
all_vals = [outcome_27_true(:,2); y_pred_mid_loo];
lims = [min(all_vals)-0.05*range(all_vals), max(all_vals)+0.05*range(all_vals)];
plot(lims, lims, 'k--', 'LineWidth', 1.5);
p = p_mid;
plot(linspace(lims(1),lims(2),100), polyval(p,linspace(lims(1),lims(2),100)), 'r-', 'LineWidth', 2);
text(0.05, 0.92, sprintf('R^2 = %.3f', mdl_mid_cv.Rsquared.Ordinary), 'Units','normalized','FontSize',11);
text(0.05, 0.84, sprintf('adj R^2 = %.3f', mdl_mid_cv.Rsquared.Adjusted), 'Units','normalized','FontSize',11);
text(0.05, 0.76, sprintf('p = %.3f', mdl_mid_cv.Coefficients.pValue(2)), 'Units','normalized','FontSize',11);
xlabel('Actual \DeltaBehavior','FontSize',12);
ylabel('Predicted \DeltaBehavior','FontSize',12);
title('Midazolam','FontSize',13);
xlim(lims); ylim(lims); axis square; box on;
hold off;

sgtitle('Baseline Placebo NP FCs → Behavioral Change', 'FontSize', 14);