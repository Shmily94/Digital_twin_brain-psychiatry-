
function [CPM_Result] = xic_CPM_Auto_corr_perm(inputdata,subject_name,phenotype,phenotype_subject)

%% sst

 phenotype_subject(isnan(phenotype))=[];
 phenotype(isnan(phenotype))=[];

% ------------ INPUTS -------------------

[a b] = intersect(subject_name,phenotype_subject);

all_stop_sucess_mask = inputdata(:,:,b);


all_stop_sucess_mask = reshape(all_stop_sucess_mask,[],length(b))';

[a b] = intersect(phenotype_subject,subject_name);

behavi = phenotype(b);

size1 = size(behavi);

if size1(1) ==1
    behavi =behavi';
    
end

all_behav = behavi;


% sst sucess
all_mats  = all_stop_sucess_mask;
CPM_Result = xic_CPM_corr_perm(all_mats,all_behav);


end

function [CPM_Result2] = xic_CPM_corr_perm(all_mats,all_behav)


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
mask(mask_nan) =r;
mask_p(mask_nan) =p;


% CPM_Result2 = reshape(mask,size_matrix,size_matrix);

CPM_Result2 = mask';
end
