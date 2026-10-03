
function [CPM_Result] = xic_CPM_train_test(all_mats,brain_sub,phenotype,phenotype_subject,thresh)



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


[r p] = corr(all_mats,all_behav);
mask(mask_nan) = r;
mask_p(mask_nan)= p;

CPM_Result.corrmatrix = reshape(mask,size_matrix,size_matrix);
CPM_Result.pmatrix = reshape(mask_p,size_matrix,size_matrix);

%% train parameter
 [r_mat,p_mat] = corr(all_mats,all_behav);
 
  r_mat(isnan(r_mat))= 0;
  p_mat(isnan(p_mat))= 0;
    
    % set threshold and define masks
    
    pos_mask = zeros(size(all_mats,2),1);
    neg_mask = zeros(size(all_mats,2),1);
   
%     
%     pos_edges = find(r_mat > 0 & p_mat < thresh);
%     neg_edges = find(r_mat < 0 & p_mat < thresh);
    
    pos_mask(r_mat > 0 & p_mat < thresh) = 1;
    neg_mask(r_mat < 0 & p_mat < thresh) = 1;
       
 
    mask_pos_final =pos_mask;
    mask_neg_final =neg_mask;
    mask_both_final =neg_mask+pos_mask;

    train_sumpos = sum(all_mats(:,pos_mask==1),2);
    train_sumneg = sum(all_mats(:,neg_mask==1),2);
    
    
    % build model on TRAIN subs
    fit_pos = polyfit(train_sumpos, all_behav,1);
    fit_neg = polyfit(train_sumneg, all_behav,1);
    
    fit_both = polyfit(train_sumpos-train_sumneg, all_behav,1);
  
    CPM_Result.fit_pos = fit_pos;
    CPM_Result.fit_neg = fit_neg;
    CPM_Result.fit_both = fit_both;
    
    CPM_Result.mask_pos = mask_pos_final;
    CPM_Result.mask_neg = mask_neg_final;
    CPM_Result.mask_both = mask_both_final;
    CPM_Result.thresh = thresh;
    

end
