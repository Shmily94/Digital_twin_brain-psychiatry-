%% Inputs
% baselineNP: Nx1 vector of baseline NP factor (per region or voxel)
% deltaNP:   Nx1 vector of NP change (ΔNP) after perturbation

baselineNP=data(:,1);
deltaNP=data(:,3);
%% 1. Compute real correlation
corr_real = corr(baselineNP, deltaNP, 'type','Pearson');

%% 2. Permutation test
n_perm = 10000;          % number of permutations
corr_perm = zeros(n_perm,1);

for i = 1:n_perm
    % randomly shuffle ΔNP
    delta_shuffled = deltaNP(randperm(length(deltaNP)));
    % compute correlation with baseline
    corr_perm(i) = corr(baselineNP, delta_shuffled, 'type','Pearson');
end

%% 3. Compute two-tailed p-value
p_value = (sum(abs(corr_perm) >= abs(corr_real)) + 1) / (n_perm + 1);

%% 4. Display results
fprintf('Real correlation: %.3f\n', corr_real);
fprintf('Permutation p-value: %.4f\n', p_value);

%% 5. Optional: visualize permutation distribution
figure;
histogram(corr_perm, 50);
hold on;
xline(corr_real, 'r', 'LineWidth', 2, 'Label','Observed corr');
xlabel('Correlation coefficient');
ylabel('Frequency');
title('Permutation test for baseline-dependent ΔNP');