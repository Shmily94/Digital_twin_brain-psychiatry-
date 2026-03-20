
% baselineNP: Nx1 vector of baseline NP factor (per region or voxel)
% deltaNP:   Nx1 vector of NP change (ΔNP) after perturbation

baselineNP=data(:,1); 
deltaNP=data(:,3);

%Compute real correlation
corr_real = corr(baselineNP, deltaNP, 'type','Pearson');

%Permutation test
n_perm = 10000;  
corr_perm = zeros(n_perm,1);

for i = 1:n_perm
    delta_shuffled = deltaNP(randperm(length(deltaNP))); % randomly shuffle ΔNP
    corr_perm(i) = corr(baselineNP, delta_shuffled, 'type','Pearson');
end

%Compute two-tailed p-value
p_value = (sum(abs(corr_perm) >= abs(corr_real)) + 1) / (n_perm + 1);

%Display results
fprintf('Real correlation: %.3f\n', corr_real);
fprintf('Permutation p-value: %.4f\n', p_value);
