
function [CPM_Result] = xic_CPM_corr(all_mats,brain_subj,phenotype,phenotype_subject)



if size(all_mats,3)>100
all_mats = reshape(all_mats,[],size(all_mats,3));
all_mats= all_mats';
end

[all brain beha] = intersect(brain_subj,phenotype_subject);

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
      
end


% end


