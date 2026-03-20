
function xic_CPM_Auto_site(phenotype,phenotype_name,phenotype_subject,thresh)

% sst
path = '/share/home1/xic_fdu/project/IMAGEN_FU2_CONN/SST_Condition_matrix_shen_GLM_band_pass'; 
load(fullfile(path,'SST_all_stop_failure.mat'))
load(fullfile(path,'SST_all_stop_sucess.mat'))

load('/share/home1/xic_fdu/project/IMAGEN_FU2_CONN/subject_reward.mat')


% ------------ INPUTS -------------------

subject_name = cellfun(@str2double,subject_name);

[a b] = intersect(subject_name,phenotype_subject);
all_stop_failure = all_stop_failure(:,:,b);
all_stop_sucess = all_stop_sucess(:,:,b);
all_stop_failure = reshape(all_stop_failure,[],length(b))';
all_stop_sucess = reshape(all_stop_sucess,[],length(b))';

[a b] = intersect(phenotype_subject,subject_name);
behavi = sum(phenotype(b,:),2);

all_behav = behavi;


% sst sucess
all_mats  = all_stop_sucess;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM_SST_sucess.mat'];
save(out_name,'CPM_Result');

% sst failure
all_mats  = all_stop_failure;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM_SST_failure.mat'];
save(out_name,'CPM_Result');

%  go wrong
load(fullfile(path,'SST_all_go_wrong.mat'))

[a b] = intersect(subject_name_go_worng,phenotype_subject);
all_go_wrong = all_go_wrong(:,:,b);
all_go_wrong = reshape(all_go_wrong,[],length(b))';

[a b] = intersect(phenotype_subject,subject_name_go_worng);
behavi = sum(phenotype(b,:),2);
all_behav = behavi;

all_mats  = all_go_wrong;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM_SST_go_wrong.mat'];
save(out_name,'CPM_Result');


close all
%% mid
path = '/share/home1/xic_fdu/project/IMAGEN_FU2_CONN/MID_Condition_matrix_shen_GLM';
load(fullfile(path,'/all_mean_anticip_hit.mat'))
load(fullfile(path,'/all_mean_feedback_hit.mat'))
load(fullfile(path,'/all_mean_feedback_miss.mat'))

% ------------ INPUTS -------------------
[a b] = intersect(subject_reward,phenotype_subject);

all_mean_anticip_hit = all_mean_anticip_hit(:,:,b);
all_mean_feedback_hit = all_mean_feedback_hit(:,:,b);
all_mean_feedback_miss = all_mean_feedback_miss(:,:,b);

all_mean_anticip_hit = reshape(all_mean_anticip_hit,[],size(b,1))';
all_mean_feedback_hit = reshape(all_mean_feedback_hit,[],size(b,1))';
all_mean_feedback_miss = reshape(all_mean_feedback_miss,[],size(b,1))';
% 

[a b] = intersect(phenotype_subject,subject_reward);
behavi = sum(phenotype(b,:),2);


all_behav = behavi;

% anticip
all_mats  = all_mean_anticip_hit;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM_MID_anticip.mat'];
save(out_name,'CPM_Result');
R_pos_all(4) = CPM_Result.R_pos;
% feedback_hit
all_mats  = all_mean_feedback_hit;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM_MID_feedback_hit.mat'];
save(out_name,'CPM_Result');
R_pos_all(5) = CPM_Result.R_pos;
% feedback_miss
all_mats  = all_mean_feedback_miss;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
% [CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_MID_feedback_miss.mat'];
save(out_name,'CPM_Result');
R_pos_all(6) = CPM_Result.R_pos;
close all

% ft
path = '/home1/xic_fdu/project/IMAGEN_FU2_CONN/FT_Condition_matrix_shen_GLM_band_pass/';
load(fullfile(path,'FT_all_neutral_new.mat'))
load(fullfile(path,'FT_all_happy_new.mat'))
load(fullfile(path,'FT_all_angry_new.mat'))

% ------------ INPUTS -------------------
subject_name = cellfun(@str2double,subject_name);
[a b] = intersect(subject_name,phenotype_subject);

network_a_subject = network_a_subject(:,:,b);
network_h_subject = network_h_subject(:,:,b);
network_n_subject = network_n_subject(:,:,b);
all_angry = reshape(network_a_subject,[],length(b))';
all_happy = reshape(network_h_subject,[],length(b))';
all_neutral = reshape(network_n_subject,[],length(b))';


[a b] = intersect(phenotype_subject,subject_name);
behavi = sum(phenotype(b,:),2);
all_behav = behavi;


%neutral
all_mats  = all_neutral;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM_FT_neutral.mat'];
save(out_name,'CPM_Result');
R_pos_all(7) = CPM_Result.R_pos;
% hayppy
all_mats  = all_happy;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM_FT_happy.mat'];
save(out_name,'CPM_Result');
R_pos_all(8) = CPM_Result.R_pos;
% angry
all_mats  = all_angry;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM_FT_angry.mat'];
CPM_Result.subject = a;
save(out_name,'CPM_Result');
R_pos_all(9) = CPM_Result.R_pos;
close all
end
