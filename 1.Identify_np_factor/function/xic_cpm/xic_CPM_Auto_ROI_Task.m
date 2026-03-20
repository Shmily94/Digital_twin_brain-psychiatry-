
function xic_CPM_Auto_ROI_Task(phenotype,phenotype_name,phenotype_subject,mask_input)

%% sst

disp('sst')

path = '/share/home1/xic_fdu/project/IMAGEN_FU2_CONN/SST_Condition_matrix_shen_GLM_band_pass'; 
load(fullfile(path,'SST_all_stop_failure.mat'))
load(fullfile(path,'SST_all_stop_sucess.mat'))

load('/share/home1/xic_fdu/project/IMAGEN_FU2_CONN/subject_reward.mat')


% ------------ INPUTS -------------------

clear mask_template_all
% sst sucess ; sst failure ; go wrong
mask_template_all{1} = fullfile(mask_input(9).folder,mask_input(9).name);
mask_template_all{2} = fullfile(mask_input(7).folder,mask_input(7).name);
mask_template_all{3} = fullfile(mask_input(8).folder,mask_input(8).name);


subject_name = cellfun(@str2double,subject_name);

[a b] = intersect(subject_name,phenotype_subject);
all_stop_failure = all_stop_failure(:,:,b);
all_stop_sucess = all_stop_sucess(:,:,b);
all_stop_failure = reshape(all_stop_failure,[],length(b))';
all_stop_sucess = reshape(all_stop_sucess,[],length(b))';

[a b] = intersect(phenotype_subject,subject_name);
behavi = sum(phenotype(b,:),2);

subject1 = a;
all_behav1 = behavi;
all_mats1  = all_stop_sucess;

% sst failure

subject2 = a;
all_behav1 = behavi;
all_mats2  = all_stop_failure;

% go wrong

load(fullfile(path,'SST_all_go_wrong.mat'))

[a b] = intersect(subject_name_go_worng,phenotype_subject);
all_go_wrong = all_go_wrong(:,:,b);
all_go_wrong = reshape(all_go_wrong,[],length(b))';

[a b] = intersect(phenotype_subject,subject_name_go_worng);
behavi = sum(phenotype(b,:),2);
all_behav3 = behavi;

all_mats3  = all_go_wrong;
subject3 = a;

% intersect all

[a,b] = intersect(subject1,intersect(subject2,subject3));
all_behav_all = all_behav1(b);
all_mats_all(:,:,1) = all_mats1(b,:);

[a,b] = intersect(subject2,intersect(subject1,subject3));
all_mats_all(:,:,2) = all_mats2(b,:);

[a,b] = intersect(subject3,intersect(subject2,subject1));
all_mats_all(:,:,3) = all_mats3(b,:);

CPM_Result = xic_CPM_roi_task_square(all_mats_all,all_behav_all,mask_template_all);

out_name = [phenotype_name,'_CPM_SST.mat'];
save(out_name,'CPM_Result');



all_mats_sst = all_mats_all;
all_subjects_sst = a;
all_phnoetype_sst = all_behav_all;
mask_template_sst = mask_template_all;

%% mid


disp('mid')

path = '/share/home1/xic_fdu/project/IMAGEN_FU2_CONN/MID_Condition_matrix_shen_GLM';
load(fullfile(path,'/all_mean_anticip_hit.mat'))
load(fullfile(path,'/all_mean_feedback_hit.mat'))
load(fullfile(path,'/all_mean_feedback_miss.mat'))

% ------------ INPUTS -------------------



% anticip ;  feedback_hit ; feedback miss

clear mask_template_all all_mats_all

mask_template_all{1} = fullfile(mask_input(4).folder,mask_input(4).name);
mask_template_all{2} = fullfile(mask_input(5).folder,mask_input(5).name);
mask_template_all{3} = fullfile(mask_input(6).folder,mask_input(6).name);

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
subject1 = a;
all_mats1  = all_mean_anticip_hit;

all_mats2  = all_mean_feedback_hit;
subject2 =a;

all_mats3  = all_mean_feedback_miss;
subject3 = a;
 
% intersect all

[a,b] = intersect(subject1,intersect(subject2,subject3));
all_behav_all = all_behav(b);
all_mats_all(:,:,1) = all_mats1(b,:);

[a,b] = intersect(subject2,intersect(subject1,subject3));
all_mats_all(:,:,2) = all_mats2(b,:);

[a,b] = intersect(subject3,intersect(subject2,subject1));
all_mats_all(:,:,3) = all_mats3(b,:);

CPM_Result = xic_CPM_roi_task_square(all_mats_all,all_behav_all,mask_template_all);

out_name = [phenotype_name,'_CPM_MID.mat'];
save(out_name,'CPM_Result');


all_mats_mid = all_mats_all;
all_subjects_mid = a;
all_phnoetype_mid = all_behav_all;
mask_template_mid = mask_template_all;



%% ft
disp('ft')

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


clear mask_template_all all_mats_all
% neutral happy angry
mask_template_all{1} = fullfile(mask_input(3).folder,mask_input(3).name);
mask_template_all{2} = fullfile(mask_input(3).folder,mask_input(2).name);
mask_template_all{3} = fullfile(mask_input(3).folder,mask_input(1).name);



all_mats1  = all_neutral;
all_mats2  = all_happy;
all_mats3  = all_angry;

subject1 = a;
subject2 = a;
subject3 = a;


% intersect all

[a,b] = intersect(subject1,intersect(subject2,subject3));
all_behav_all = all_behav(b);
all_mats_all(:,:,1) = all_mats1(b,:);

[a,b] = intersect(subject2,intersect(subject1,subject3));
all_mats_all(:,:,2) = all_mats2(b,:);

[a,b] = intersect(subject3,intersect(subject2,subject1));
all_mats_all(:,:,3) = all_mats3(b,:);


CPM_Result = xic_CPM_roi_task_square(all_mats_all,all_behav_all,mask_template_all);

out_name = [phenotype_name,'_CPM_EFT.mat'];
save(out_name,'CPM_Result');



all_mats_eft = all_mats_all;
all_subjects_eft = a;
all_phnoetype_eft = all_behav_all;
mask_template_eft = mask_template_all;

%% all task

all_template_task = [mask_template_sst,mask_template_mid,mask_template_eft];

[a b] = intersect(all_subjects_sst,intersect(all_subjects_mid,all_subjects_eft));
all_mats_sst = all_mats_sst(b,:,:);
all_phnoetype_task = all_phnoetype_eft(b);


[a b] = intersect(all_subjects_mid,intersect(all_subjects_sst,all_subjects_eft));
all_mats_mid = all_mats_mid(b,:,:);

[a b] = intersect(all_subjects_eft,intersect(all_subjects_sst,all_subjects_mid));
all_mats_eft = all_mats_eft(b,:,:);

all_mats_task = cat(3,all_mats_sst,all_mats_mid,all_mats_eft);


CPM_Result = xic_CPM_roi_task_square_all(all_mats_task,all_phnoetype_task,all_template_task);

out_name = [phenotype_name,'_CPM_All_tasks.mat'];
save(out_name,'CPM_Result');


end
