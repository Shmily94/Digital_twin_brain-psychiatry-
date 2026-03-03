%% plot_cc
clear;clc
simulate_bold=dir('*gaba*');
% load('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\new_model\simu_validation\regional_data\000000112288_regional_data.mat');

for s=1:length(simulate_bold)
bold_assim_MID = readNPY([simulate_bold(s).folder,'\',simulate_bold(s).name,'\bold_after_assim.npy']);
bold_real_processed_MID = readNPY('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\MID_task_bold.npy');
bold_assim_MID = bold_assim_MID(5:end,:);
bold_real_processed_MID = bold_real_processed_MID(5:end-1,:);
for n=1:size(bold_assim_MID,2)
[r,p]=corrcoef(bold_assim_MID(:,n),bold_real_processed_MID(:,n));
r_all(n,s)=r(1,2);
end
histogram(r_all(:,s));
title(['mean value = ',num2str(mean(r_all(:,s)))]);
fig = figure(1);
saveas(fig,[simulate_bold(s).folder,'\',simulate_bold(s).name,'\MID_cc.png']);
end
save MID_cc r_all

clear;clc
simulate_bold=dir('*gaba*');
for s=1:length(simulate_bold)
bold_assim_SST = readNPY([simulate_bold(s).folder,'\',simulate_bold(s).name,'\bold_after_assim.npy']);
bold_real_processed_SST = readNPY('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\SST_task_bold.npy');
bold_assim_SST = bold_assim_SST(10:end,:);
bold_real_processed_SST = bold_real_processed_SST(9:end-2,:);
for n=1:size(bold_assim_SST,2)
[r,p]=corrcoef(bold_assim_SST(:,n),bold_real_processed_SST(:,n));
r_all(n,s)=r(1,2);
end
histogram(r_all(:,s));
title(['mean value = ',num2str(mean(r_all(:,s)))]);
fig = figure(1);
saveas(fig,[simulate_bold(s).folder,'\',simulate_bold(s).name,'\SST_cc.png']);
end
save SST_cc r_all

%% rescale nii
clear;clc
simulate_bold=dir('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\new_model\mani_gaba\mani_task_MID_gaba\*gaba*');
load('func_bold_mid_rest_sst.mat');
load("atlas_region.mat");
MID_bold_real = Func_bold_mid_rest_sst{1};

for s=1:length(simulate_bold)
MID_bold_sim = readNPY([simulate_bold(s).folder,'\',simulate_bold(s).name,'\bold_after_assim.npy']);
MID_bold_sim_rescale = zeros(size(MID_bold_sim));
for i=1:length(voxel_label)
    MID_bold_sim_rescale(:,i) = rescale_array(MID_bold_sim(:,i),MID_bold_real(:,voxel_label(i)));
end
mask_image = niftiread("MNI152_T1_3mm_gmwmi_shen268_label.nii");
mask_info = niftiinfo("MNI152_T1_3mm_gmwmi_shen268_label.nii");
MID_image = niftiread('Preprocessed_sub-000182136619_task-mid_space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii');
MID_info = niftiinfo('Preprocessed_sub-000182136619_task-mid_space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii');
MID_sim_image = zeros([61,73,61,190],"single");
MID_sim_info = MID_info;
MID_sim_info.ImageSize = [61,73,61,190];
for i=1:length(voxel_label)
    k = find(mask_image == voxel_label(i));
    [x,y,z] = ind2sub(size(mask_image),k);
    MID_sim_image(x,y,z,:) = MID_bold_sim_rescale(:,i);
end
niftiwrite(MID_sim_image,[simulate_bold(s).folder,'\',simulate_bold(s).name,'\MID_sim.nii'],MID_sim_info);
end

%% SST
clear;clc
simulate_bold=dir('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\new_model\mani_gaba\mani_task_SST_gaba\*gaba*');
load('func_bold_mid_rest_sst.mat');
load("atlas_region.mat");
SST_bold_real = Func_bold_mid_rest_sst{3};

for s=1:length(simulate_bold)
SST_bold_sim = readNPY([simulate_bold(s).folder,'\',simulate_bold(s).name,'\bold_after_assim.npy']);
SST_bold_sim_rescale = zeros(size(SST_bold_sim));
for i=1:length(voxel_label)
    SST_bold_sim_rescale(:,i) = rescale_array(SST_bold_sim(:,i),SST_bold_real(:,voxel_label(i)));
end
mask_image = niftiread("MNI152_T1_3mm_gmwmi_shen268_label.nii");
mask_info = niftiinfo("MNI152_T1_3mm_gmwmi_shen268_label.nii");
SST_image = niftiread('Preprocessed_sub-000182136619_task-sst_space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii');
SST_info = niftiinfo('Preprocessed_sub-000182136619_task-sst_space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii');
SST_sim_image = zeros([61,73,61,349],"single");
SST_sim_info = SST_info;
SST_sim_info.ImageSize = [61,73,61,349];
for i=1:length(voxel_label)
    k = find(mask_image == voxel_label(i));
    [x,y,z] = ind2sub(size(mask_image),k);
    SST_sim_image(x,y,z,:) = SST_bold_sim_rescale(:,i);
end
niftiwrite(SST_sim_image,[simulate_bold(s).folder,'\',simulate_bold(s).name,'\SST_sim.nii'],SST_sim_info);
end

%% generate simulated nii
clear;clc
simulate_file=dir('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\new_model\mani_gaba\mani_task_SST_gaba\*gaba*');

for s=1:length(simulate_file)
Fun_indi_file=load_nii('Preprocessed_sub-000182136619_task-sst_space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii');
Fun_indi_vol = Fun_indi_file.img;
Fun_indi_vol2=Fun_indi_vol;
A=Fun_indi_vol(:,:,:,1); 
func_ind=reshape(A~=0,1,[]);
simufile=load_nii([simulate_file(s).folder,'\',simulate_file(s).name,'\SST_sim.nii']);
simu_vol = simufile.img;
B=simu_vol(:,:,:,2);
simu_ind = reshape(B~=0,1,[]);
% find(simu_ind==1); % 同化体素有多少个voxel
overlay_ind=func_ind.*simu_ind;
find(overlay_ind==1);
overlay_ind=logical(overlay_ind);
% isequal(overlay_ind,simu_ind);
for n=2:size(Fun_indi_vol,4) % 模拟数据少一个时间点
    A=Fun_indi_vol(:,:,:,n);
    B=simu_vol(:,:,:,n-1);
    A(overlay_ind)=B(overlay_ind); % 替换模拟的voxel BOLD
    Fun_indi_vol2(:,:,:,n)=A;
end
Fun_indi_file.img=Fun_indi_vol2;
save_nii(Fun_indi_file,[simulate_file(s).folder,'\',simulate_file(s).name,'\Simulated_sst.nii']);
end

%% mid 
clear;clc
simulate_file=dir('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\new_model\mani_gaba\mani_task_MID_gaba\*gaba*');
for s=1:length(simulate_file)
Fun_indi_file=load_nii('Preprocessed_sub-000182136619_task-mid_space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii');
Fun_indi_vol = Fun_indi_file.img;
Fun_indi_vol2=Fun_indi_vol;
A=Fun_indi_vol(:,:,:,1); 
func_ind=reshape(A~=0,1,[]);
simufile=load_nii([simulate_file(s).folder,'\',simulate_file(s).name,'\MID_sim.nii']);
simu_vol = simufile.img;
B=simu_vol(:,:,:,2);
simu_ind = reshape(B~=0,1,[]);
% find(simu_ind==1); % 同化体素有多少个voxel
overlay_ind=func_ind.*simu_ind;
find(overlay_ind==1);
overlay_ind=logical(overlay_ind);
% isequal(overlay_ind,simu_ind);
for n=2:size(Fun_indi_vol,4) % 模拟数据少一个时间点
    A=Fun_indi_vol(:,:,:,n);
    B=simu_vol(:,:,:,n-1);
    A(overlay_ind)=B(overlay_ind); % 替换模拟的voxel BOLD
    Fun_indi_vol2(:,:,:,n)=A;
end
Fun_indi_file.img=Fun_indi_vol2;
save_nii(Fun_indi_file,[simulate_file(s).folder,'\',simulate_file(s).name,'\Simulated_mid.nii']);
end
