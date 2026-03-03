

clear;clc

%% Match FU2 

load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Self_FU2_inter_exter.mat');
thresh = 0.01;

load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\FU2_SST_CONN_Name_match.mat')
load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\FU2_Match_MID_CONN.mat')

load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Cova_subject_jia.mat')
   
cova_data_all =repmat({cova_data},9,1);
cova_subject_all =repmat({cova_subject},9,1);

for i=1:6
    
    phenotype_name = ['FU2_0614_',FU2_self.FU2_psy_name{i}];
    phenotype_fu2 = zscore(FU2_self.FU2_psy_match(:,i)); 
    phenotype_fu2 = zscore(boxcox(phenotype_fu2+2));
    phenotype_subject = FU2_self.FU2_psy_match_sub;
      
    % regress
    
%     %% regress phenotype
     
   cova_subject_i = cova_subject_all{i};
   cova_data_i = cova_data_all{i};

    [all,ph, cova] = intersect(phenotype_subject,cova_subject_i);
    phenotype_fu2 = phenotype_fu2(ph);
    cova_data_se = cova_data_i(cova,:);
    
    phenotype_fu2 = zscore(xic_cpm_regress(phenotype_fu2,cova_data_se(:,1:8)));
    phenotype_subject = phenotype_subject(ph);
    
    
%  SST

    task_name = {'_SST_gowrong','_SST_stopfai','_SST_stopsuc'}; 
       
     % xic_cpm_tset2(FU2_SST_subject,phenotype_subject,FU2_SST_go_wrong,...
     %    phenotype_fu2,phenotype_name,thresh,task_name{1});
    % xic_cpm_tset(data_subs,phenotype_subjects,data,phenotypes,phenotype_names,threshs,task_names)
    
    xic_cpm_tset2(FU2_SST_subject,phenotype_subject,FU2_SST_stop_failure,...
        phenotype_fu2,phenotype_name,thresh,task_name{2});
    
    xic_cpm_tset2(FU2_SST_subject,phenotype_subject,FU2_SST_stop_sucess,...
        phenotype_fu2,phenotype_name,thresh,task_name{3});
    
    
    % MID
   
     task_name = {'_MID_antici_hit','_MID_feed_hit','_MID_feed_miss'}; 
    
    xic_cpm_tset2(FU2_MID_subject,phenotype_subject,FU2_MID_antici_hit,...
        phenotype_fu2,phenotype_name,thresh,task_name{1});
    
    xic_cpm_tset2(FU2_MID_subject,phenotype_subject,FU2_MID_feed_hit,...
        phenotype_fu2,phenotype_name,thresh,task_name{2});
    
    % xic_cpm_tset2(FU2_MID_subject,phenotype_subject,FU2_MID_feed_miss,...
    %     phenotype_fu2,phenotype_name,thresh,task_name{3});
    
     
end
