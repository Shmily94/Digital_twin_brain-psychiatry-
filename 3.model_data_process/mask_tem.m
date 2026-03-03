
%% create conn template for DTB model
clear;clc
load('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000159066706\atlas_region.mat');
maskfile=('D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\group_averaged\top_bot_10_FU2\Results\MNI152_T1_3mm_gmwmi_shen268_label.nii');
mask_hdr = spm_vol(maskfile);
mask_vol = spm_read_vols(mask_hdr);
mask_ind = reshape(mask_vol>0,1,[]);
label_ind=zeros(1,length(mask_ind)); 
label=mask_vol(mask_ind);

[C,ia]=setdiff(label,voxel_label); %找到模型中没有的voxel，置零
for i=1:length(C)
mask_vol(mask_vol==C(i))=0;
end
%找到对应的Shen268 ROI id
mask_ind2 = reshape(mask_vol>0,1,[]);
label_ind2=zeros(1,length(mask_ind2)); 
label2=mask_vol(mask_ind2);
for j = 1:length(label2)
    label3(j) = atlas_region(find(voxel_label==label2(j)));
end

label_ind2(mask_ind2)=label3;
[dim1,dim2,dim3]=size(mask_vol);
label_vol=reshape(label_ind2,dim1,dim2,dim3);
mask_hdr.fname='D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000159066706\shen268_mask_3mm_13003.nii';
mask_hdr.dt=[16,0]; 
spm_write_vol(mask_hdr,label_vol);


%% task-fc without cerebullum
for i=1:length(location_pp2)
    for j=1:2
    idx1=find(uni_region==location_pp2(i,j)); %atlas regions
    if idx1~=0
    location2(i,j)=idx1;
    else
        location2(i,j)=0;
    end
    end
end
% transfer 268 idx to 217 idx
original_edges=location;
new_nodes=uni_region;
new_edges = [];
for i = 1:size(original_edges, 1)
    from = original_edges(i, 1);
    to   = original_edges(i, 2);

    % 在新列表中查找原始编号对应的新索引
    idx_from = find(new_nodes == from);
    idx_to   = find(new_nodes == to);

    % 如果两个节点都在新网络中
    if ~isempty(idx_from) && ~isempty(idx_to)
        new_edges(end+1, :) = [idx_from, idx_to];
    end
end

% 输出 new_edges：是基于新的217节点的索引
disp(new_edges)
save positive_np_without_cerebellum_location2 location2

%% EXTRACT FC MATRIX
clear;clc
path = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000113174215\voxel_int_ext\New_assimilated\Conn\MID';
files = dir(fullfile(path,'conn_2507*'));
[mid_antici_hit,mid_feed_hit,mid_feed_miss,mid_subject] = xic_mid_data2(files);
save mid_data_mani_gaba mid_antici_hit mid_feed_hit mid_feed_miss mid_subject

path = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000113174215\voxel_int_ext\New_assimilated\Conn\SST';
files = dir(fullfile(path,'conn_2503*'));
[sst_go_wrong, sst_stop_suces, sst_stop_failure, sst_subject] = xic_sst_data2(files);
save sst_data_mani_gaba sst_go_wrong sst_stop_suces sst_stop_failure sst_subject

load('np_without_cerebellum_location2.mat');
for j=1:size(sst_stop_suces,3)

for i=1:3
simulate_FC(i,j)=sst_stop_suces(location2(i,1),location2(i,2),j);
end

for i=4:6
simulate_FC(i,j)=sst_stop_failure(location2(i,1),location2(i,2),j);
end

for i=7:11
simulate_FC(i,j)=mid_feed_hit(location2(i,1),location2(i,2),j);
end

for i=12:length(location2)
simulate_FC(i,j)=mid_antici_hit(location2(i,1),location2(i,2),j);
end

end
save simulate_FC_high simulate_FC
