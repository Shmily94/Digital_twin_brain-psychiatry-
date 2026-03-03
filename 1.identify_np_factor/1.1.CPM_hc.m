clear;clc
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\HC_withsex\')
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\STRA_control.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\FU2_control.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\FU3_control.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\HC_cova.mat');

MID_antici_hit=cat(3,STRA_MID_antici_hit,FU2_MID_antici_hit,FU3_MID_antici_hit);
MID_feed_hit=cat(3,STRA_MID_feedhit,FU2_MID_feed_hit,FU3_MID_feed_hit);
MID_feed_miss=cat(3,STRA_MID_feedmiss,FU2_MID_feed_miss,FU3_MID_feed_miss);
SST_stop_sucess=cat(3,STRA_SST_stop_suces,FU2_SST_stop_sucess,FU3_SST_stop_sucess);
SST_stop_failure=cat(3,STRA_SST_stop_failure,FU2_SST_stop_failure,FU3_SST_stop_failure);
SST_go_wrong=cat(3,STRA_SST_go_wrong,FU2_SST_go_wrong,FU3_SST_go_wrong);
MID_subject=[MID_subject;FU2_MID_subject2;FU3_MID_subject2];
SST_subject=[SST_subject;FU2_SST_subject2;FU3_SST_subject2];
beha.data=[STRA_beha_data;FU2_beha_data;FU3_beha_data];
beha.subject=[STRA_beha_subject2;FU2_beha_subject2;FU3_beha_subject2];
save HC_brain_beha_cova MID_subject MID_antici_hit MID_feed_hit MID_feed_miss SST_subject SST_stop_sucess SST_stop_failure...
    SST_go_wrong beha cova_data cova_subject psy_name

load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\HC_brain_beha_cova.mat');
cova_data_all =repmat({cova_data},9,1);
cova_subject_all =repmat({cova_subject},9,1);
thresh = 0.01;
for i=1:6
       
    phenotype_name = psy_name{i};
    phenotype_HC = zscore(beha.data(:,i)); 
    phenotype_HC = zscore(boxcox(phenotype_HC+3)); % 为了可以做boxcox，所以需要大于0，因此+3
    phenotype_subject = beha.subject;

% regress phenotype
     
   cova_subject_i = cova_subject_all{i};
   cova_data_i = cova_data_all{i};

    [all,ph,cova] = intersect(phenotype_subject,cova_subject_i);
    phenotype_HC = phenotype_HC(ph);
    cova_data_se = cova_data_i(cova,:);
    
    phenotype_HC = zscore(xic_cpm_regress(phenotype_HC,cova_data_se(:,1:4)));
    phenotype_subject = phenotype_subject(ph);
    
    
%  SST

    task_name = {'_SST_gowrong','_SST_stopfai','_SST_stopsuc'}; 
    xic_cpm_tset3(SST_subject,phenotype_subject,SST_go_wrong,...
        phenotype_HC,phenotype_name,thresh,task_name{1})

    xic_cpm_tset3(SST_subject,phenotype_subject,SST_stop_failure,...
        phenotype_HC,phenotype_name,thresh,task_name{2})

    xic_cpm_tset3(SST_subject,phenotype_subject,SST_stop_sucess,...
        phenotype_HC,phenotype_name,thresh,task_name{3})


% MID

     task_name = {'_MID_antici_hit','_MID_feed_hit','_MID_feed_miss'}; 

    xic_cpm_tset3(MID_subject,phenotype_subject,MID_antici_hit,...
        phenotype_HC,phenotype_name,thresh,task_name{1})

    xic_cpm_tset3(MID_subject,phenotype_subject,MID_feed_hit,...
        phenotype_HC,phenotype_name,thresh,task_name{2})

    xic_cpm_tset3(MID_subject,phenotype_subject,MID_feed_miss,...
        phenotype_HC,phenotype_name,thresh,task_name{3})
     
end

