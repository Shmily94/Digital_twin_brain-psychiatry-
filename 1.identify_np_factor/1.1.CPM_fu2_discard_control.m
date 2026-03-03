%% FU2

clear;clc
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\')
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Self_FU2_inter_exter.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro\idx_discard.mat');
thresh = 0.01;
load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\FU2_SST_CONN_Name_match.mat')
load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\FU2_Match_MID_CONN.mat')
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Cova_subject_jia.mat')

[FU2_SST_subject2,ia]=setdiff(SST_subject,idx_discard); 
[FU2_MID_subject2,ib]=setdiff(FU2_MID_subname,idx_discard); 

cova_data_all =repmat({cova_data},9,1);
cova_subject_all =repmat({cova_subject},9,1);

for i=1:6
    
    phenotype_name = FU2_self.FU2_psy_name{i};
    phenotype_fu2 = zscore(FU2_self.FU2_psy_match(:,i)); 
    phenotype_fu2 = zscore(boxcox(phenotype_fu2+2));
    phenotype_subject = FU2_self.FU2_psy_match_sub;

% regress phenotype
     
   cova_subject_i = cova_subject_all{i};
   cova_data_i = cova_data_all{i};

    [all,ph,cova] = intersect(phenotype_subject,cova_subject_i);
    phenotype_fu2 = phenotype_fu2(ph);
    cova_data_se = cova_data_i(cova,:);
    
    phenotype_fu2 = zscore(xic_cpm_regress(phenotype_fu2,cova_data_se(:,1:8)));
    phenotype_subject = phenotype_subject(ph);
    
    
%  SST

    task_name = {'_SST_gowrong','_SST_stopfai','_SST_stopsuc'}; 
    xic_cpm_tset(FU2_SST_subject2,phenotype_subject,FU2_SST_go_wrong(:,:,ia),...
        phenotype_fu2,phenotype_name,thresh,task_name{1})

    xic_cpm_tset(FU2_SST_subject2,phenotype_subject,FU2_SST_stop_failure(:,:,ia),...
        phenotype_fu2,phenotype_name,thresh,task_name{2})

    xic_cpm_tset(FU2_SST_subject2,phenotype_subject,FU2_SST_stop_sucess(:,:,ia),...
        phenotype_fu2,phenotype_name,thresh,task_name{3})


% MID

     task_name = {'_MID_antici_hit','_MID_feed_hit','_MID_feed_miss'}; 

    xic_cpm_tset(FU2_MID_subject2,phenotype_subject,FU2_MID_antici_hit(:,:,ib),...
        phenotype_fu2,phenotype_name,thresh,task_name{1})

    xic_cpm_tset(FU2_MID_subject2,phenotype_subject,FU2_MID_feed_hit(:,:,ib),...
        phenotype_fu2,phenotype_name,thresh,task_name{2})

    xic_cpm_tset(FU2_MID_subject2,phenotype_subject,FU2_MID_feed_miss(:,:,ib),...
        phenotype_fu2,phenotype_name,thresh,task_name{3})
     
end

