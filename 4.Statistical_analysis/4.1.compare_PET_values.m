%% real differences between np and non-np regions
clear;clc

values=x(:,2:40); % regions * PET receptor maps 
all_idx = 1:length(values);
np_idx;
non_np_idx=setdiff(all_idx,np_idx);
real_diff = mean(values(np_idx,:)) - mean(values(non_np_idx,:));

%bootstrap
n_perm = 10000;
perm_diffs = zeros(n_perm,39);

for j=1:39 % n of maps
for i = 1:n_perm
    perm_np_idx = randsample(all_idx, length(np_idx));
    perm_non_np_idx = setdiff(all_idx, perm_np_idx);
    perm_diffs(i,j) = mean(values(perm_np_idx,j)) - mean(values(perm_non_np_idx,j));
end
end

for j=1:39
p_value = (sum(abs(perm_diffs(:,j)) >= abs(real_diff(1,j))) + 1) / (n_perm + 1);
p_value_39(j)=p_value;
end

% FDR
fdr_pvals = mafdr(p_value_39, 'BHFDR', true);
disp(fdr_pvals);
map_name(fdr_pvals<0.05)



