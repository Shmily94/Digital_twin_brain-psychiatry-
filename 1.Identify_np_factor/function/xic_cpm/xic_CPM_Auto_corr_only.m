
function [CPM_Corr] = xic_CPM_Auto_corr_only(phenotype,phenotype_name,phenotype_subject)

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
disp('sst')
all_mats  = all_stop_sucess;
CPM_Corr.sst_su = xic_CPM_corr(all_mats,all_behav);


% sst failure
all_mats  = all_stop_failure;
CPM_Corr.sst_fai = xic_CPM_corr(all_mats,all_behav);


%  go wrong
load(fullfile(path,'SST_all_go_wrong.mat'))

[a b] = intersect(subject_name_go_worng,phenotype_subject);
all_go_wrong = all_go_wrong(:,:,b);
all_go_wrong = reshape(all_go_wrong,[],length(b))';

[a b] = intersect(phenotype_subject,subject_name_go_worng);
behavi = sum(phenotype(b,:),2);
all_behav = behavi;

all_mats  = all_go_wrong;
CPM_Corr.sst_gowro = xic_CPM_corr(all_mats,all_behav);


close all
%% mid
disp('mid')
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
CPM_Corr.mid_ant = xic_CPM_corr(all_mats,all_behav);


% feedback_hit
all_mats  = all_mean_feedback_hit;
CPM_Corr.mid_feed_h = xic_CPM_corr(all_mats,all_behav);

% feedback_miss
all_mats  = all_mean_feedback_miss;
CPM_Corr.mid_feed_m  = xic_CPM_corr(all_mats,all_behav);

close all

%% ft
disp('eft')
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
all_mats  = all_neutral;
CPM_Corr.eft_n = xic_CPM_corr(all_mats,all_behav);

% hayppy
all_mats  = all_happy;
CPM_Corr.eft_h = xic_CPM_corr(all_mats,all_behav);

% angry
all_mats  = all_angry;
CPM_Corr.eft_a = xic_CPM_corr(all_mats,all_behav);
% R_pos_all(9) = CPM_Result.R_pos;
close all
end
