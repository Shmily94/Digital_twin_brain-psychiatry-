
function xic_CPM_ROI_Task(phenotype,phenotype_name,phenotype_subject,mask_input)

%% sst



% ------------ INPUTS -------------------

%% data1 
[a,b_data,b_phno] = intersect(data_sub1,phenotype_subject);
 
 data1  = data1(:,:,b_data);
 phenotype1 = phenotype(b_phno);
 

clear mask_template_all
% sst sucess ; sst failure ; go wrong
mask_template_all{1} = fullfile(mask_input(9).folder,mask_input(9).name);
mask_template_all{2} = fullfile(mask_input(7).folder,mask_input(7).name);
mask_template_all{3} = fullfile(mask_input(8).folder,mask_input(8).name);


CPM_Result = xic_CPM_roi_task_square(all_mats_all,all_behav_all,mask_template_all);

out_name = [phenotype_name,'_CPM_SST.mat'];
save(out_name,'CPM_Result');


end
