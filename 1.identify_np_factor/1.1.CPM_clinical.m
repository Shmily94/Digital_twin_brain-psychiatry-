clear;clc
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\')
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\Behavior_related_results\beha_data\STRA_self_dawba.mat');
thresh = 0.01;
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\FC_results\Shen_results\CONN_FC\STRATIFY_MID_SST_FC.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\Cova_subject_stra.mat');
load('control_id.mat');
cova_data_all =repmat({cova_data},9,1);
cova_subject_all =repmat({cova_subject},9,1);
% 去掉control的被试，只留下疾病
[STRA_SST_subject2,ia]=setdiff(SST_subject,idx_discard); 
[STRA_MID_subject2,ib]=setdiff(MID_subjtec,idx_discard); 
STRA_SST_subject2(1:2,:)=[];
ia(1:2,:)=[];
for i=1:6
       
    phenotype_name = STRA_self.psy_name{i};
    phenotype_STRA = zscore(STRA_self.STRA_psy_match(:,i)); 
    phenotype_STRA = zscore(boxcox(phenotype_STRA+3)); % 为了可以做boxcox，所以需要大于0，因此+3
    phenotype_subject = STRA_self.psy_match_sub;

% regress phenotype
     
   cova_subject_i = cova_subject_all{i};
   cova_data_i = cova_data_all{i};

    [all,ph,cova] = intersect(phenotype_subject,cova_subject_i);
    phenotype_STRA = phenotype_STRA(ph);
    cova_data_se = cova_data_i(cova,:);
    
    phenotype_STRA = zscore(xic_cpm_regress(phenotype_STRA,cova_data_se(:,1:4)));
    phenotype_subject = phenotype_subject(ph);
    
    
%  SST

    task_name = {'_SST_gowrong','_SST_stopfai','_SST_stopsuc'}; 
    xic_cpm_tset3(STRA_SST_subject2,phenotype_subject,SST_go_wrong(:,:,ia),...
        phenotype_STRA,phenotype_name,thresh,task_name{1})

    xic_cpm_tset3(STRA_SST_subject2,phenotype_subject,SST_stop_failure(:,:,ia),...
        phenotype_STRA,phenotype_name,thresh,task_name{2})

    xic_cpm_tset3(STRA_SST_subject2,phenotype_subject,SST_stop_suces(:,:,ia),...
        phenotype_STRA,phenotype_name,thresh,task_name{3})


% MID

     task_name = {'_MID_antici_hit','_MID_feed_hit','_MID_feed_miss'}; 

    xic_cpm_tset3(STRA_MID_subject2,phenotype_subject,MID_antici_hit(:,:,ib),...
        phenotype_STRA,phenotype_name,thresh,task_name{1})

    xic_cpm_tset3(STRA_MID_subject2,phenotype_subject,MID_feedhit(:,:,ib),...
        phenotype_STRA,phenotype_name,thresh,task_name{2})

    xic_cpm_tset3(STRA_MID_subject2,phenotype_subject,MID_feedmiss(:,:,ib),...
        phenotype_STRA,phenotype_name,thresh,task_name{3})
     
end

