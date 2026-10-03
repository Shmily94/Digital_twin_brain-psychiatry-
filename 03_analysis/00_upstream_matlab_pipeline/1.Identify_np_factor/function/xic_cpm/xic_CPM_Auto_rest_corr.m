%% Rest

function xic_CPM_Auto_rest_corr(phenotype,phenotype_name,phenotype_subject,thresh)


%% Rest
load('/share/home1/xic_fdu/project/IMAGEN_Rest_FU2/rest_shen_withoutgs_fu2_matrix.mat')
load(fullfile('/home1/xic_fdu/IMAGEN_Download/--IMAGEN-REST-FSL--/RS_FU2_IMAGEN_shen_name.mat'))


% -----------------------
file_name = Rest_fu2_name;
matrix_shen_withoutgs = Re_FU2_IMAGEN;

fu2_adsr_subject = phenotype_subject;

[a b] = intersect(file_name,fu2_adsr_subject);
matrix_shen_withoutgs = matrix_shen_withoutgs(:,:,b);

matrix_shen_withoutgs = reshape(matrix_shen_withoutgs,[],length(b))';


[a b] = intersect(fu2_adsr_subject,file_name);

depression = phenotype; depression = depression(b);

all_mats  = matrix_shen_withoutgs;

all_behav = depression;
% all_mats(out,:)=[];
% all_behav(out,:)=[];
% threshold for feature selection
% thresh = 0.01;

% ---------------------------------------
CPM_Result = xic_CPM_corr(all_mats,all_behav,thresh);
CPM_Result.subjet =a;

% [CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

% save Depression_CPM_Rest.mat CPM_Result CPM_mask


out_name = [phenotype_name,'_CPM_Rest.mat'];
save(out_name,'CPM_Result');

end
