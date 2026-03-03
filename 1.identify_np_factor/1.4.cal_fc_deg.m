
clear;clc

%% calculate the degree of each regions based on NP factors

%load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM\AAL_node.mat');

roi_degree=zeros(268,1);

idx=TableS6.TableS6_across.SST_stop_sucess_id{5,1};
idx=TableS6.TableS6_across.SST_stop_failure_id{5,1};
idx=TableS6.TableS6_across.SST_go_wrong_id{5,1};
idx=TableS6.TableS6_across.MID_feedmiss_id{5,1};
%idx=TableS6.TableS6_across.MID_feedhit_id{4,1};
idx=TableS6.TableS6_across.MID_anticip_id{5,1};

for i=1:length(idx)
idx_single=idx(i);
[m,n]=find(mask_id_all==idx_single);
roi_degree(m,1)=roi_degree(m,1)+1;
roi_degree(n,1)=roi_degree(n,1)+1;
% ROI1=char(AAL_noble.ROI_label(m));
% ROI2=char(AAL_noble.ROI_label(n));
% FC_pp_MID_feedhit{i}=[ROI1,'-',ROI2];
end
save roi_degree.mat roi_degree FC_pp_stop_sucess FC_pp_stop_failure FC_pp_MID_feedhit

% visual
maskfile=('D:\postdoc\Work\Computer-Brain-Project\Code\Mask\shen_3mm_268_parcellation.nii');
mask_hdr = spm_vol(maskfile);
mask_vol = spm_read_vols(mask_hdr);
mask_ind = reshape(mask_vol>0,1,[]);
label_ind=zeros(1,length(mask_ind)); 
label=mask_vol(mask_ind);
%normalized_roi_detgree=zscore(roi_degree);
roi_degree(roi_degree<3)=0;
for i = 1:length(roi_degree)
    label2(label==i) = roi_degree(i);
end
label_ind(mask_ind)=label2;
[dim1,dim2,dim3]=size(mask_vol);
label_vol=reshape(label_ind,dim1,dim2,dim3);
mask_hdr.fname='D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Shen\roi_degree_neg_neg.nii';
mask_hdr.dt=[16,0]; 
spm_write_vol(mask_hdr,label_vol);