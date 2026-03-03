%% MID conn
clear;clc
data_path = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\new_model\first_Level\SST';
output = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\new_model\Conn\SST\';
mkdir(output)   
files = dir(fullfile(data_path,'2507*'));
% outfiles=  dir(fullfile(output,'\conn*'));
t1_file = 'D:\SciTools\spm12\spm12\canonical\avg152T1.nii';
tr = 2.2;
% roi_file = 'D:\postdoc\Work\Computer-Brain-Project\Code\Mask\Reslice_shen_2mm_268_parcellation.nii';
% roi_file = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000113174215\shen268_mask_3mm_13040.nii';
 roi_file = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000182136619\shen268_mask_3mm_12873.nii';
%roi_file = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000191996808\shen268_mask_3mm_12980.nii';
% roi_file = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000083037309\shen268_mask_3mm_11891.nii';
% roi_file = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000000112288\shen268_mask_3mm_12358.nii';
%roi_file = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000030374303\shen268_mask_3mm_12151.nii';
%roi_file = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000147701848\shen268_mask_3mm_13114.nii';
%roi_file = 'D:\postdoc\Work\Computer-Brain-Project\Results\DTB_model\New_assimilated_results\sub-000159066706\shen268_mask_3mm_13003.nii';

roi_name = 'shen_3mm_268';

for i=1:length(files)
    try
    spm_path = fullfile(files(i).folder,files(i).name,'SPM.mat');
    out_path = fullfile(output,['conn_',files(i).name]);
    out_name = fullfile(output,['conn_',files(i).name,'.mat']);
    xic_conn_batch(spm_path,t1_file,tr,out_name,roi_name,roi_file)
    %% move file
    disp(['Process Subject_conn__',num2str(i,'%04d')]);
    movefile(fullfile(out_path,'\results\firstlevel\ANALYSIS_01\resultsROI_Condition*'),out_path);
    movefile(fullfile(out_path,'\results\firstlevel\ANALYSIS_01\_list_conditions*'),out_path);
    rmdir(fullfile(out_path,'\data'),'s');
    rmdir(fullfile(out_path,'\results\'),'s');   
    delete(out_name)    
    catch
    end
end
