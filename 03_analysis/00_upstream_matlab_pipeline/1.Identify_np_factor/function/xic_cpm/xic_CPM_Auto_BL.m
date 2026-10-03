
function xic_CPM_Auto_BL(phenotype,phenotype_name,phenotype_subject,thresh)



%% mid
path = '/share/home1/xic_fdu/project/IMAGEN_Estimate_XIC';

load(fullfile(path,'/BL_MID_CONN.mat'))

% ------------ INPUTS -------------------


[a b] = intersect(sub_name,phenotype_subject);

sub_antici_hit = sub_antici_hit(:,:,b);
sub_feed_hit = sub_feed_hit(:,:,b);
sub_feed_miss = sub_feed_miss(:,:,b);

sub_antici_hit = reshape(sub_antici_hit,[],length(b))';
sub_feed_hit = reshape(sub_feed_hit,[],length(b))';
sub_feed_miss = reshape(sub_feed_miss,[],length(b))';
% 

[a b] = intersect(phenotype_subject,sub_name);
behavi = sum(phenotype(b,:),2);


all_behav = behavi;

% anticip
all_mats  = sub_antici_hit;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
[CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_MID_anticip.mat'];
save(out_name,'CPM_Result','CPM_mask','-v7.3');
R_pos_all(4) = CPM_Result.R_pos;

% feedback_hit
all_mats  = sub_feed_hit;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
[CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_MID_feedback_hit.mat'];
save(out_name,'CPM_Result','CPM_mask','-v7.3');
R_pos_all(5) = CPM_Result.R_pos;

% feedback_miss
all_mats  = sub_feed_miss;
CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
[CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_MID_feedback_miss.mat'];
save(out_name,'CPM_Result','CPM_mask','-v7.3');
R_pos_all(6) = CPM_Result.R_pos;
close all


%% SST

path = '/share/home1/xic_fdu/project/IMAGEN_Estimate_XIC';

load(fullfile(path,'/BL_SST_CONN.mat'))

% ------------ INPUTS -------------------

% Gowrong


[a b] = intersect(go_wrong_subject,phenotype_subject);

go_wrong = go_wrong(:,:,b);

go_wrong = reshape(go_wrong,[],length(b))';

[a b] = intersect(phenotype_subject,go_wrong_subject);
behavi = sum(phenotype(b,:),2);

all_behav = behavi;
all_mats  = go_wrong;

CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
[CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_SST_gorong.mat'];
save(out_name,'CPM_Result','CPM_mask','-v7.3');

% stop_failure


[a b] = intersect(stop_failure_subject,phenotype_subject);

stop_failure = stop_failure(:,:,b);

stop_failure = reshape(stop_failure,[],length(b))';

[a b] = intersect(phenotype_subject,stop_failure_subject);
behavi = sum(phenotype(b,:),2);

all_behav = behavi;
all_mats  = stop_failure;

CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
[CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_SST_stop_fai.mat'];
save(out_name,'CPM_Result','CPM_mask','-v7.3');

% stop_suces


[a b] = intersect(stop_suces_subject,phenotype_subject);

stop_suces = stop_suces(:,:,b);

stop_suces = reshape(stop_suces,[],length(b))';

[a b] = intersect(phenotype_subject,stop_suces_subject);
behavi = sum(phenotype(b,:),2);

all_behav = behavi;
all_mats  = stop_suces;

CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
[CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_SST_stop_suce.mat'];
save(out_name,'CPM_Result','CPM_mask','-v7.3');

%% EFT


path = '/share/home1/xic_fdu/project/IMAGEN_Estimate_XIC';

load(fullfile(path,'/BL_EFT_CONN.mat'))

% ------------ INPUTS -------------------

% angry


[a b] = intersect(angry_subject,phenotype_subject);

angry = EFT_angry(:,:,b);

angry = reshape(angry,[],length(b))';

[a b] = intersect(phenotype_subject,angry_subject);
behavi = sum(phenotype(b,:),2);

all_behav = behavi;
all_mats  = angry;

CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
[CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_EFT_angry.mat'];
save(out_name,'CPM_Result','CPM_mask','-v7.3');

% neutral


[a b] = intersect(neutral_subject,phenotype_subject);

neutral = EFT_neutral(:,:,b);

neutral = reshape(neutral,[],length(b))';

[a b] = intersect(phenotype_subject,neutral_subject);
behavi = sum(phenotype(b,:),2);

all_behav = behavi;
all_mats  = neutral;

CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
[CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_EFT_neutral.mat'];
save(out_name,'CPM_Result','CPM_mask','-v7.3');

% stop_suces


[a b] = intersect(stop_suces_subject,phenotype_subject);

stop_suces = stop_suces(:,:,b);

stop_suces = reshape(stop_suces,[],length(b))';

[a b] = intersect(phenotype_subject,stop_suces_subject);
behavi = sum(phenotype(b,:),2);

all_behav = behavi;
all_mats  = stop_suces;

CPM_Result = xic_CPM_both(all_mats,all_behav,thresh);
CPM_Result.subject = a;
[CPM_mask] = xic_CPM_mask(all_mats,CPM_Result);

out_name = [phenotype_name,'_CPM_SST_stop_suce.mat'];
save(out_name,'CPM_Result','CPM_mask','-v7.3');

end
