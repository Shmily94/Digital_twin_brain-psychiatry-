%% file description

% structural connectome “dti_net_full” —— n*n
% gray matter “grey_matter_size” —— n*1
% resting-state BOLD “rest_state_bold” —— t*n
% task-state BOLD “XX_task_bold”  —— t*n
% regional_label of each voxel “atlas_region” —— n*1
% all regional label “uni_region” —— N*1
% Logical judgment of whether a brain region belongs to the cortex  “is_cortex” —— N*1
% original label of each voxel “voxel_label” （from MNI152_T1_3mm_gmwmi_shen268_label.nii）—— n*1


%% extract individual data
clear;clc

tic
% DTI image
dti_net_full = load("000000112288_voxel_connectome.mat");
dti_net_full = dti_net_full.sc;
toc

tic
% T1 image
gmV = load("sub-000000112288_gmv.mat");
grey_matter_size = gmV.gmv_indi';
toc

tic
% fMRI image
load("sub-000000112288_fmri_bold.mat");
MID_task_bold = Func_bold{1};
SST_task_bold = Func_bold{2};
rest_state_bold = Func_bold{3};
toc

%% construct mask atlas
atlas_table = readtable("shen_268.csv");
voxel_location = niftiread("MNI152_T1_3mm_gmwmi_shen268_label.nii");
atlas_image = niftiread("shen_3mm_268_parcellation.nii");

assert(max(voxel_location,[],'all') == length(grey_matter_size),'mask file have different voxel numbers with data')

atlas_region = zeros([length(unique(voxel_location))-1, 1]);
for i=1:length(atlas_region)
    atlas_region(i) = atlas_image(voxel_location(:) == i);
end
sum(atlas_region == 0)

%exclude BrainStem and Cerebellum
leave_out = {'Cerebellum', 'BrainStem'};
Sub_regions = {'n/a', 'Caudate', 'Putamen', 'Thalamus', 'Amygdala', 'Hippocampus'};
atlas_table = atlas_table(~ismember(atlas_table.BA, leave_out),:);
uni_region = atlas_table.ROI;
is_cortex = ~ismember(atlas_table.BA,Sub_regions);
voxel_label = 1:length(atlas_region);
voxel_label = voxel_label(ismember(atlas_region,uni_region))';

rest_state_bold = rest_state_bold(:,ismember(atlas_region,uni_region));
MID_task_bold = MID_task_bold(:,ismember(atlas_region,uni_region));
SST_task_bold = SST_task_bold(:,ismember(atlas_region,uni_region));
grey_matter_size = grey_matter_size(ismember(atlas_region,uni_region));
dti_net_full = dti_net_full(ismember(atlas_region,uni_region),ismember(atlas_region,uni_region));

atlas_region = atlas_region(ismember(atlas_region,uni_region));

%% normalize bold signals

rest_state = rest_state_bold;
for i=1:size(rest_state,2)
    rest_state_bold(:,i) = zscore(rest_state(:,i));
end
task_state = MID_task_bold;
for i=1:size(task_state,2)
    MID_task_bold(:,i) = zscore(task_state(:,i));
end
task_state = SST_task_bold;
for i=1:size(task_state,2)
    SST_task_bold(:,i) = zscore(task_state(:,i));
end

subplot(2,1,1)
plot(rest_state_bold(:,1:10))

%% filter bold signals

fs = 1/2.2;
fpass = [0.01,0.1];
rest_state_bold = bandpass(rest_state_bold,fpass,fs);
MID_task_bold = bandpass(MID_task_bold,fpass,fs);
SST_task_bold = bandpass(SST_task_bold,fpass,fs);

subplot(2,1,2)
plot(rest_state_bold(:,1:10))

save("individual_raw_mri_data","dti_net_full","atlas_region","uni_region","is_cortex","voxel_label","grey_matter_size","MID_task_bold","rest_state_bold","SST_task_bold")
