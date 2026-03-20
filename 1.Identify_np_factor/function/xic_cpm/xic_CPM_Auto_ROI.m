
function xic_CPM_Auto_ROI(phenotype,phenotype_name,phenotype_subject,mask_input)

%% sst
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
mask_template = fullfile(mask_input(9).folder,mask_input(9).name);

all_mats  = all_stop_sucess;
CPM_Result = xic_CPM_roi_square(all_mats,all_behav,mask_template);


out_name = [phenotype_name,'_CPM_SST_sucess.mat'];
save(out_name,'CPM_Result');

% sst failure
mask_template = fullfile(mask_input(7).folder,mask_input(7).name);

all_mats  = all_stop_failure;
CPM_Result = xic_CPM_roi_square(all_mats,all_behav,mask_template);

out_name = [phenotype_name,'_CPM_SST_failure.mat'];
save(out_name,'CPM_Result');

% go wrong
mask_template = fullfile(mask_input(8).folder,mask_input(8).name);

load(fullfile(path,'SST_all_go_wrong.mat'))

[a b] = intersect(subject_name_go_worng,phenotype_subject);
all_go_wrong = all_go_wrong(:,:,b);
all_go_wrong = reshape(all_go_wrong,[],length(b))';

[a b] = intersect(phenotype_subject,subject_name_go_worng);
behavi = sum(phenotype(b,:),2);
all_behav = behavi;

all_mats  = all_go_wrong;
CPM_Result = xic_CPM_roi_square(all_mats,all_behav,mask_template);

out_name = [phenotype_name,'_CPM_SST_go_wrong.mat'];
save(out_name,'CPM_Result');



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


[a b] = intersect(phenotype_subject,subject_reward);
behavi = sum(phenotype(b,:),2);


all_behav = behavi;

% anticip
mask_template = fullfile(mask_input(4).folder,mask_input(4).name);

all_mats  = all_mean_anticip_hit;
CPM_Result = xic_CPM_roi_square(all_mats,all_behav,mask_template);

out_name = [phenotype_name,'_CPM_MID_anticip.mat'];
save(out_name,'CPM_Result');


% feedback_hit
mask_template = fullfile(mask_input(5).folder,mask_input(5).name);


all_mats  = all_mean_feedback_hit;
CPM_Result = xic_CPM_roi_square(all_mats,all_behav,mask_template);

out_name = [phenotype_name,'_CPM_MID_feedback_hit.mat'];
save(out_name,'CPM_Result');


% feedback miss
mask_template = fullfile(mask_input(6).folder,mask_input(6).name);

all_mats  = all_mean_feedback_miss;
CPM_Result = xic_CPM_roi_square(all_mats,all_behav,mask_template);

out_name = [phenotype_name,'_CPM_MID_feedback_miss.mat'];
save(out_name,'CPM_Result');

close all

%% ft
path = '/home1/xic_fdu/project/IMAGEN_FU2_CONN/FT_Condition_matrix_shen_GLM_band_pass/';
load(fullfile(path,'FT_all_neutral_new.mat'))
load(fullfile(path,'FT_all_happy_new.mat'))
load(fullfile(path,'FT_all_angry_new.mat'))

% ------------ INPUTS -------------------
subject_name = cellfun(@str2double,subject_name);
[a b] = intersect(subject_name,phenotype_subject);
% 
network_a_subject = network_a_subject(:,:,b);
network_h_subject = network_h_subject(:,:,b);
network_n_subject = network_n_subject(:,:,b);
all_angry = reshape(network_a_subject,[],length(b))';
all_happy = reshape(network_h_subject,[],length(b))';
all_neutral = reshape(network_n_subject,[],length(b))';


[a b] = intersect(phenotype_subject,subject_name);
behavi = sum(phenotype(b,:),2);
all_behav = behavi;


% neutral
mask_template = fullfile(mask_input(3).folder,mask_input(3).name);

all_mats  = all_neutral;
CPM_Result = xic_CPM_roi_square(all_mats,all_behav,mask_template);

out_name = [phenotype_name,'_CPM_FT_neutral.mat'];
save(out_name,'CPM_Result');

% happy
mask_template = fullfile(mask_input(2).folder,mask_input(2).name);

all_mats  = all_happy;
CPM_Result = xic_CPM_roi_square(all_mats,all_behav,mask_template);

out_name = [phenotype_name,'_CPM_FT_happy.mat'];
save(out_name,'CPM_Result');


% angry
mask_template = fullfile(mask_input(1).folder,mask_input(1).name);

all_mats  = all_angry;
CPM_Result = xic_CPM_roi_square(all_mats,all_behav,mask_template);

out_name = [phenotype_name,'_CPM_FT_angry.mat'];
save(out_name,'CPM_Result');
close all
end
