
% task ROI figure
mask_input='D:\postdoc\Work\Computer-Brain-Project\Code\Mask\Reslice_shen_2mm_268_parcellation.nii';
maskfile=load_nii(mask_input);
mask_vol = maskfile.img;
for i=1:268
      mask_vol(mask_vol==i) = SST_roi(i);  
end 
maskfile.img=mask_vol;
save_nii(maskfile,'ROI_SST_DTB.nii');
save ROI_MID_SST MID_roi SST_roi idx_SST idx_MID

% validation task DTB biological
bold_assim_MID = readNPY('bold_random_gui.npy');
bold_real_processed_MID = readNPY('MID_task_bold.npy');
bold_assim_MID = bold_assim_MID(5:end,:);
bold_real_processed_MID = bold_real_processed_MID(5:end-1,:);
% bold_assim_MID=bold_assim_MID_smoothed;
for n=1:size(bold_assim_MID,2)
[r,p]=corrcoef(bold_assim_MID(:,n),bold_real_processed_MID(:,n));
r_all(n,1)=r(1,2);
end
histogram(r_all);
title(['mean value = ',num2str(mean(r_all))]);
fig = figure(1);
saveas(fig,'MID_cc_smoothed','png');
r_diff=r_all_smoothed-r_all_random;
histogram(r_diff);
title(['mean value = ',num2str(mean(r_diff))]);
fig = figure(1);
saveas(fig,'MID_cc_diff','png');
save MID_cc_smoothed_random_diff_assi_no_assi r_MID_smoothed ...,
r_MID_random r_MID_diff r_assi_MID r_no_assi_MID

% post cc histogram
bold_assim_MID = readNPY('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\group_averaged\top_bot_10_FU2\Results\Simulated_1B\top\bold_after_assim_MID.npy');
bold_real_processed_MID = readNPY('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\group_averaged\top_bot_10_FU2\Results\top\supplementary_info\MID_task_bold.npy');
bold_assim_MID = bold_assim_MID(5:end,:);
bold_real_processed_MID = bold_real_processed_MID(5:end-1,:);
for n=1:size(bold_assim_MID,2)
[r,p]=corrcoef(bold_assim_MID(:,n),bold_real_processed_MID(:,n));
r_all(n,1)=r(1,2);
end
histogram(r_all);
title(['mean value = ',num2str(mean(r_all))]);
% fig = figure(1);
% saveas(fig,'MID_cc_1B','png');
bold_assim_SST= readNPY('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\group_averaged\top_bot_10_FU2\Results\Simulated_1B\top\bold_after_assim_SST.npy');
bold_real_processed_SST = readNPY('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\group_averaged\top_bot_10_FU2\Results\top\supplementary_info\SST_task_bold.npy');
bold_assim_SST = bold_assim_SST(10:end,:);
bold_real_processed_SST = bold_real_processed_SST(9:end-2,:);
for n=1:size(bold_assim_SST,2)
[r,p]=corrcoef(bold_assim_SST(:,n),bold_real_processed_SST(:,n));
r_all(n,1)=r(1,2);
end
histogram(r_all);
title(['mean value = ',num2str(mean(r_all))]);
fig = figure(1);
saveas(fig,'SST_cc_1B','png');
save SST_cc_smoothed_assi_no_assi r_SST_smoothed r_assi_SST r_no_assi_SST

% plot brain figure
load('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\group_averaged\top_bot_10_FU2\Results\top\supplementary_info\atlas_region.mat');
mask_image = niftiread("MNI152_T1_3mm_gmwmi_shen268_label.nii");
mask_info = niftiinfo("MNI152_T1_3mm_gmwmi_shen268_label.nii");
for i=1:length(voxel_label)
    k = find(mask_image == voxel_label(i));
    [x,y,z] = ind2sub(size(mask_image),k);
    mask_image(x,y,z) = r_SST(i,1);
end
mask_image(mask_image>=1)=0;
niftiwrite(mask_image,"SST_cc_1B.nii",mask_info);

% 区分同化体素和同化外体素的cc
idx_assi_MID_all=0;
for i=1:length(idx_MID)
idx_assi_MID=find(atlas_region==idx_SST(i));
idx_assi_MID_all=[idx_assi_MID_all idx_assi_MID];
end
idx_assi_MID_all(1,1)=[];
idx_assi_MID_all=idx_assi_MID_all';
r_assi_MID=r_diff(idx_assi_MID_all);
logical_idx=true(size(r_all_smoothed));
logical_idx(idx_assi_MID_all)=false;
r_no_assi_MID=r_diff(logical_idx);
histogram(r_no_assi_MID);
title(['mean value = ',num2str(mean(r_no_assi_MID))]);
fig = figure(1);
saveas(fig,'MID_cc_no_assi_diff','png');

idx_assi_SST_all=0;
for i=1:length(idx_SST)
idx_assi_SST=find(atlas_region==idx_SST(i));
idx_assi_SST_all=[idx_assi_SST_all idx_assi_SST];
end
idx_assi_SST_all(1,1)=[];
idx_assi_SST_all=idx_assi_SST_all';
r_assi_SST=r_SST_smoothed(idx_assi_SST_all);
logical_idx=true(size(r_SST_smoothed));
logical_idx(idx_assi_SST_all)=false;
r_no_assi_SST=r_SST_smoothed(logical_idx);
histogram(r_assi_SST);
title(['mean value = ',num2str(mean(r_assi_SST))]);
fig = figure(1);
saveas(fig,'SST_cc_assi_diff','png');