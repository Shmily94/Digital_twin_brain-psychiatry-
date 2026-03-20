
clear;clc
% cal NP fcs in STRATIFY 
load('\make_mask_across_fc.mat','oppo_nn_dimen_ind');
load('\STRATIFY_MID_SST_same_id_FC.mat');
for n=1:length(C)
FC1_neg=SST_stop_suces(:,:,n);
FC2_neg=SST_stop_failure(:,:,n);
FC3_neg=MID_feedhit(:,:,n);
FC4_neg=MID_antici_hit(:,:,n);
FCS_neg(n,:)=[FC1_neg(oppo_nn_dimen_ind{1})',FC2_neg(oppo_nn_dimen_ind{2})',FC3_neg(oppo_nn_dimen_ind{3})',FC4_neg(oppo_nn_dimen_ind{4})'];
end
save FCS_neg_STRA FCS_neg


% t-test NP fcs between control and diseased
clear;clc
X=cova_data; % age,sex,site,mean fd
Y=NP_fcs; 
Y_resi = xic_cpm_regress(Y,X(:,2:end));
for i = 1:size(Y,2)
    [h,p,ci,stats] = ttest2(Y_resi(1:225,i),Y_resi(226:end,i));  % healthy vs diseased
    compare_hc_dis(i,1) = stats.tstat;
    compare_hc_dis(i,2) = p;
end

% t-test NP fcs between control and specific disorders, e.g.,mdd
X=cova_data(diseased_label.MDD==1,:);
Y_resi = xic_cpm_regress(Y(diseased_label.MDD==1,:),X(:,2:end));
for i = 1:size(Y,2)
    [h,p,ci,stats] = ttest2(Y_resi(1:225,i),Y_resi(226:end,i)); 
    compare_hc_dis(i,1) = stats.tstat;
    compare_hc_dis(i,2) = p;

end


