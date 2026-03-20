%% calculate task-speicifc fc
clear;clc
data_path = 'simulated_nii\first_Level\SST';
output = 'simulated_nii\Conn\SST\';
mkdir(output)   
files = dir(fullfile(data_path,'*gaba*'));
t1_file = 'D:\SciTools\spm12\spm12\canonical\avg152T1.nii';
tr = 2.2;
% roi_file = '\Mask\shen268_3mm_parcellation.nii';
% roi_file = '\sub_demo\shen268_mask_3mm_13040.nii'; % actual used voxel in the DTB model

roi_name = 'shen_3mm_217';

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

%% extract np factor
clear;clc
path = '\Conn\MID';
files = dir(fullfile(path,'*gaba*'));
[mid_antici_hit,mid_feed_hit,mid_feed_miss,mid_subject] = xic_mid_data2(files);
save mid_data_mani_gaba mid_antici_hit mid_feed_hit mid_feed_miss mid_subject

path = '\Conn\SST';
files = dir(fullfile(path,'*gaba*'));
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
save simulate_FC simulate_FC