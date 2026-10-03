

clear;clc
% conn_batchexample_singlesubject_nopreprocessing
% This example prompts the user to select one anatomical volume and one first-level SPM.mat file 
% and performs all connectivity analyses using all the default atlas ROIs
%
addpath(genpath('/home1/xic_fdu/share/spm12'));
addpath(genpath('/home1/xic_fdu/share/conn16a'));
addpath(genpath('/home1/xic_fdu/xic_analysis/xic_conn'));

data_path = '/share/inspurStorage/home1/ISTBI_data/IMAGEN_New_Preprocessed/First_Level/MID/ses-followup2';
output = '/share/inspurStorage/home1/ISTBI_data/IMAGEN_New_Preprocessed/Conn_second/MID/FU2';
mkdir(output)

files = dir(fullfile(data_path,'sub*'));
outfiles=  dir(fullfile(output,'/conn*'));
%%

t1_file = '/home1/xic_fdu/share/spm12/canonical/avg152T1.nii';
tr = 2.2;
roi_file = '/home1/ISTBI_data/IMAGEN_New_Preprocessed/Conn_second/Reslice_shen_2mm_268_parcellation.nii';
roi_name = 'shen_2mm_268';

%% batch preprocessing for single-subject single-session data 

parfor i=1:length(files)
	fprintf('subject %4d \n',i)
	out_path = fullfile(output,['conn_',files(i).name]);
	sub_file(i,1) = length(dir(out_path));

end

files= files(sub_file<10,:);


parfor i=1:length(files)
    try
 
    spm_path = fullfile(files(i).folder,files(i).name,'SPM.mat');
    out_path = fullfile(output,['conn_',files(i).name]);
    out_name = fullfile(output,['conn_',files(i).name,'.mat']);
    
    %if length(dir(out_path))< 3
    %delete(out_path);
    xic_conn_batch(spm_path,t1_file,tr,out_name,roi_name,roi_file)
    %% move file
    disp(['Process Subject_conn__',num2str(i,'%04d')]);
    
    movefile(fullfile(out_path,'/results/firstlevel/ANALYSIS_01/resultsROI_Condition*'),out_path);
    movefile(fullfile(out_path,'/results/firstlevel/ANALYSIS_01/_list_conditions*'),out_path);
    
    rmdir(fullfile(out_path,'/data'),'s');
    rmdir(fullfile(out_path,'/results/'),'s');   
    delete(out_name)
    %else
    %disp(['Donot Need to Process Subject_conn__',num2str(i,'%04d')]);
    
    %end
    
    catch
        
    end
end

%% CONN Setup



