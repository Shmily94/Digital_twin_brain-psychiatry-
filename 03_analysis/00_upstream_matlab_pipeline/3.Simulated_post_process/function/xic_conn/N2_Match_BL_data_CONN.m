

clear;clc

cd('/share/inspurStorage/home1/ISTBI_data/IMAGEN_New_Preprocessed/Conn_second')
%% MID
path = '/share/inspurStorage/home1/ISTBI_data/IMAGEN_New_Preprocessed/Conn_second/MID/FU2';
files = dir(fullfile(path,'conn*'));

[mid_antici_hit,mid_feed_hit,mid_feed_miss,mid_subject] = xic_mid_data(files);
save FU2_MID_data.mat mid_antici_hit mid_feed_hit mid_feed_miss mid_subject

%% SST
path = '/share/inspurStorage/home1/ISTBI_data/IMAGEN_New_Preprocessed/Conn_second/SST/FU3';
files = dir(fullfile(path,'conn*'));
[sst_go_wrong, sst_stop_suces, sst_stop_failure, sst_subject] = xic_sst_data(files);
save FU3_SST_data.mat sst_go_wrong sst_stop_suces sst_stop_failure sst_subject
                        
%% EFT
path = '/share/inspurStorage/home1/ISTBI_data/IMAGEN_New_Preprocessed/Conn_second/EFT/FU3';
files = dir(fullfile(path,'conn*')); 
[eft_neutral,eft_angry,eft_subject] = xic_eft_data_BL(files);
save FU3_EFT_data.mat eft_neutral eft_angry eft_subject 
  
