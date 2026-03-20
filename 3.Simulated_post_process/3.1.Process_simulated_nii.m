%% Bold correlation coefficient
clear;clc
simulate_bold=dir('*gaba*');
for s=1:length(simulate_bold)
bold_assim_MID = readNPY([simulate_bold(s).folder,'\',simulate_bold(s).name,'\bold_after_assim.npy']);
bold_real_processed_MID = readNPY('MID_task_bold.npy');
bold_assim_MID = bold_assim_MID(5:end,:);
bold_real_processed_MID = bold_real_processed_MID(5:end-1,:); % time delay
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
bold_real_processed_SST = readNPY('SST_task_bold.npy');
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

%% rescale simulated data
clear;clc
simulate_bold=dir('*gaba*');
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
MID_image = niftiread('Preprocessed_sub.nii');
MID_info = niftiinfo('Preprocessed_sub.nii');
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

%% generate simulated nii 
clear;clc
simulate_file=dir('*gaba*');
for s=1:length(simulate_file)
Fun_indi_file=load_nii('Preprocessed_sub.nii');
Fun_indi_vol = Fun_indi_file.img;
Fun_indi_vol2=Fun_indi_vol;
A=Fun_indi_vol(:,:,:,1); 
func_ind=reshape(A~=0,1,[]);
simufile=load_nii([simulate_file(s).folder,'\',simulate_file(s).name,'\MID_sim.nii']);
simu_vol = simufile.img;
B=simu_vol(:,:,:,2);
simu_ind = reshape(B~=0,1,[]);
overlay_ind=func_ind.*simu_ind;
find(overlay_ind==1);
overlay_ind=logical(overlay_ind);
% isequal(overlay_ind,simu_ind);
for n=2:size(Fun_indi_vol,4) % first time point 
    A=Fun_indi_vol(:,:,:,n);
    B=simu_vol(:,:,:,n-1);
    A(overlay_ind)=B(overlay_ind); 
    Fun_indi_vol2(:,:,:,n)=A;
end
Fun_indi_file.img=Fun_indi_vol2;
save_nii(Fun_indi_file,[simulate_file(s).folder,'\',simulate_file(s).name,'\Simulated_mid.nii']);
end
