
%% create individualized template including voxels used in DTB model
clear;clc

load('sub-demo\atlas_region.mat');
maskfile=('MNI152_T1_3mm_gmwmi_shen268_label.nii');
mask_hdr = spm_vol(maskfile);
mask_vol = spm_read_vols(mask_hdr);
mask_ind = reshape(mask_vol>0,1,[]);
label_ind=zeros(1,length(mask_ind)); 
label=mask_vol(mask_ind);

[C,ia]=setdiff(label,voxel_label); 
for i=1:length(C)
mask_vol(mask_vol==C(i))=0;
end

mask_ind2 = reshape(mask_vol>0,1,[]);
label_ind2=zeros(1,length(mask_ind2)); 
label2=mask_vol(mask_ind2);
for j = 1:length(label2)
    label3(j) = atlas_region(find(voxel_label==label2(j)));
end

label_ind2(mask_ind2)=label3;
[dim1,dim2,dim3]=size(mask_vol);
label_vol=reshape(label_ind2,dim1,dim2,dim3);
mask_hdr.fname='\sub-demo\shen268_mask_3mm_13003.nii';
mask_hdr.dt=[16,0]; 
spm_write_vol(mask_hdr,label_vol);

