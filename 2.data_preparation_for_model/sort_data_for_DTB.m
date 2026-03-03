% 结构连接 “dti_net_full” —— n*n
% 灰质体积 “grey_matter_size” —— n*1
% 静息态BOLD “rest_state_bold” —— t*n
% 任务态BOLD “XX_task_bold” XX为该任务的缩写如 “MID_task_bold” —— t*n
% 体素所属脑区 “atlas_region” —— n*1
% 所有脑区编号 “uni_region” —— N*1
% 脑区是否属于皮层 “is_cortex” —— N*1
% 体素在原mask中的编号 “voxel_label” （原mask标记的是灰白质交接的体素，但未必所有体素都会被纳入模型）—— n*1
clear;

%% 数据读取
tic
% DTI image
dti_net_full = load("000030374303_voxel_connectome.mat");
dti_net_full = dti_net_full.sc;
toc

tic
% T1 image
gmV = load("sub-000030374303_gmv.mat");
grey_matter_size = gmV.gmv_indi';
toc

tic
% fMRI image
load("sub-000030374303_fmri_bold.mat");
MID_task_bold = Func_bold{1};
SST_task_bold = Func_bold{2};
rest_state_bold = Func_bold{3};
toc

%% mask与atlas
atlas_table = readtable("D:\postdoc\Work\Computer-Brain-Project\Code\for_model\shen_268.csv");
% voxel_location = niftiread("IMAGEN_FU2\MNI3mm_gmwmi_bin_shen268_label.nii");
% atlas_image = niftiread("IMAGEN_FU2\shen_3mm_268_parcellation.nii");
voxel_location = niftiread("MNI152_T1_3mm_gmwmi_shen268_label.nii");
atlas_image = niftiread("D:\postdoc\Work\Computer-Brain-Project\Code\Mask\shen_3mm_268_parcellation.nii");

assert(max(voxel_location,[],'all') == length(grey_matter_size),'mask file have different voxel numbers with data')

% 得到体素的脑区分布
atlas_region = zeros([length(unique(voxel_location))-1, 1]);
for i=1:length(atlas_region)
    atlas_region(i) = atlas_image(voxel_location(:) == i);
end
sum(atlas_region == 0)

%% 去除小脑和脑干，并区分皮层和皮层下

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

%% bold计算z-score

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

%% bold滤波
fs = 1/2.2;
fpass = [0.01,0.1];
rest_state_bold = bandpass(rest_state_bold,fpass,fs);
MID_task_bold = bandpass(MID_task_bold,fpass,fs);
SST_task_bold = bandpass(SST_task_bold,fpass,fs);

subplot(2,1,2)
plot(rest_state_bold(:,1:10))

save("DTI_voxel_network_IMAGEN_sample_bot","dti_net_full","atlas_region","uni_region","is_cortex","voxel_label","grey_matter_size","MID_task_bold","rest_state_bold","SST_task_bold")


a = readtable("D:\postdoc\Work\Computer-Brain-Project\Code\for_model\Shen_268_ymx.csv");
disp(a.ROI(a.MID==1)')
disp(a.ROI(a.SST==2)')