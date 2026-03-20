
clear;clc
cd('/home1/ISTBI_data/IMAGEN_New_Preprocessed/Conn_second/')
path = '/home1/ISTBI_data/IMAGEN_New_Preprocessed/Prepressed/fmriprep/';
ses = {'ses-followup2','ses-followup3'};
out = {'FU2','FU3'};
template = reshape(y_ReadAll('Reslice_shen_2mm_268_parcellation.nii'),[],1);

files = dir(fullfile(path,'sub*'));
files_all = struct2cell(files)';
files = files(contains(string(files_all(:,5)),'true'),:);

for j=1:2
    for i=1:length(files)
        fprintf('Read subject file %02d %03d  \n',j,i)
        rest_file = dir(fullfile(files(i).folder,files(i).name,ses{j},'func/Preprocessed_*rest*prepro*'));
        rest_ind(i,j) = length(rest_file);  
    end
end

for j=1:2
    ses_files = files(rest_ind(:,j)~=0,:);
    
    clear rest_conn rest_fd rest_name
    parfor i=1:length(ses_files)
        fprintf('Read subject file %02d %03d  \n',j,i)
        rest_file = dir(fullfile(ses_files(i).folder,ses_files(i).name,ses{j},'func/Preprocessed_*rest*prepro*bold.nii.gz'));
        rest_dat  = y_ReadAll(fullfile(rest_file(1).folder,rest_file(1).name));
        rest_conn(:,:,i) = corr(xic_fc(rest_dat,template));
       
        motion_file = dir(fullfile(ses_files(i).folder,ses_files(i).name,ses{j},'func/*est_motion.par'));
        rest_fd(i,1) = xic_fwd(fullfile(motion_file(1).folder,motion_file(1).name));
        
        rest_name(i,1) = str2double(strrep(ses_files(i).name,'sub-',''));
        
    end
    out_name = ['Rest_',out{j},'.mat'];
    save(out_name,'rest_conn','rest_fd','rest_name'); 
end

