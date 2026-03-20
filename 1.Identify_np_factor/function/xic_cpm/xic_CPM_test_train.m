
function [CPM_Result] = xic_CPM_test_train(all_mats,brain_sub,...
                                  phenotype,phenotype_subject,CPM_train)




if size(all_mats,3)>100
all_mats = reshape(all_mats,[],size(all_mats,3));
all_mats= all_mats';
end

[all brain beha] = intersect(brain_sub,phenotype_subject);
all_mats = all_mats(brain,:);
all_behav = phenotype(beha);

size_matrix = sqrt(size(all_mats,2));
mask = zeros(1,size_matrix*size_matrix);
mask_p = zeros(1,size_matrix*size_matrix);


all_mats_nan_mask = all_mats(1,:);

mask_nan = find(isnan(all_mats_nan_mask)~=1);
all_mats(:,isnan(all_mats_nan_mask))=[];

all_mats_nan = all_mats(:,2);
all_mats(isnan(all_mats_nan),:)=[];
all_behav(isnan(all_mats_nan),:)=[];

%% test

    mask_pos_final = CPM_train.mask_pos;
    mask_neg_final = CPM_train.mask_neg;
    mask_both_final = CPM_train.mask_both;

    
    test_sumpos = sum(all_mats(:,mask_pos_final==1),2);
    test_sumneg = sum(all_mats(:,mask_neg_final==1),2);
    
    
    behav_pred_pos = CPM_train.fit_pos(1)*test_sumpos + CPM_train.fit_pos(2);
    behav_pred_neg = CPM_train.fit_neg(1)*test_sumneg + CPM_train.fit_neg(2);
    behav_pred_both = CPM_train.fit_both(1)*(test_sumpos-test_sumneg) + CPM_train.fit_both(2);
    
    [R_pos,p] = corr(behav_pred_pos,all_behav);
    [R_neg,p] = corr(behav_pred_neg,all_behav);
    [R_both,p] = corr(behav_pred_both,all_behav);
  
    CPM_Result.R_pos = R_pos; CPM_Result.Predict_pos = behav_pred_pos;
    CPM_Result.R_neg = R_neg; CPM_Result.Predict_neg = behav_pred_neg;
    CPM_Result.R_both = R_both;  CPM_Result.Predict_both = behav_pred_both;

end
