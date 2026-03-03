
%% baseline
% clear;clc
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_Models')
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\BL_1Psycho_data.mat');

thresh = 0.01;
load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\BL_MID_CONN.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\BL_SST_CONN.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Code\IAMGEN_Develop_diagnostic_0814\Cova_subject_jia.mat');

cova_data_all =repmat({cova_data},9,1);
cova_subject_all =repmat({cova_subject},9,1);
for i=1:9
    
    phenotype_name = ['BL_0815_',BL_psycho_name{i}];
    phenotype_bl = mean(BL_psycho_data{i},2);    
    phenotype_subject = BL_psycho_subject{i};
      

    
% regress phenotype
     
   cova_subject_i = cova_subject_all{i};
   cova_data_i = cova_data_all{i};

    [all,ph, cova] = intersect(phenotype_subject,cova_subject_i);
    phenotype_bl = phenotype_bl(ph);
    cova_data_se = cova_data_i(cova,:);
    
    phenotype_bl = zscore(xic_cpm_regress(phenotype_bl,cova_data_se(:,1:8)));
    phenotype_subject = phenotype_subject(ph);
  
   [a, b_data, b_phno] = intersect(cell2mat(sublist),phenotype_subject);
       
   data3_ph = activ_AAL(b_data,:);
   phenotype3 = phenotypes(b_phno);
 
task_name = {'_SST_gowrong','_SST_stopfai','_SST_stopsuc'}; 
       
    xic_cpm_tset(go_wrong_subject,phenotype_subject,go_wrong,...
        phenotype_bl,phenotype_name,thresh,task_name{1})
    
    xic_cpm_tset(stop_failure_subject,phenotype_subject,stop_failure,...
        phenotype_bl,phenotype_name,thresh,task_name{2})
    
    xic_cpm_tset(stop_suces_subject,phenotype_subject,stop_suces,...
        phenotype_bl,phenotype_name,thresh,task_name{3})
    
    
 % MID
   
     task_name = {'_MID_antici_hit','_MID_feed_hit','_MID_feed_miss'}; 
    
    xic_cpm_tset(sub_mid_subject,phenotype_subject,sub_antici_hit_reward,...
        phenotype_bl,phenotype_name,thresh,task_name{1})
    
    xic_cpm_tset(sub_mid_subject,phenotype_subject,sub_feed_hit_reward,...
        phenotype_bl,phenotype_name,thresh,task_name{2})
    
    xic_cpm_tset(sub_mid_subject,phenotype_subject,sub_feed_miss_reward,...
        phenotype_bl,phenotype_name,thresh,task_name{3})
    
       
    % EFT
    %  task_name = {'_EFT_angry','_EFT_neutral'}; 
    % 
    %  xic_cpm_tset(BL_EFT_angry_subject,phenotype_subject,BL_EFT_angry,...
    %     phenotype_bl,phenotype_name,thresh,task_name{1})
    % 
    % xic_cpm_tset(BL_EFT_neutral_subject,phenotype_subject,BL_EFT_neutral,...
    %     phenotype_bl,phenotype_name,thresh,task_name{2})
    % 
  
end


%% FU2

clear;clc
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_Models_FU2\')

load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Self_FU2_inter_exter.mat');
thresh = 0.01;
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\FU2_SST_CONN.mat')
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\FU2_MID_CONN.mat')
load('D:\postdoc\Work\Computer-Brain-Project\Code\IAMGEN_Develop_diagnostic_0814\Cova_subject_jia.mat')
   
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

    [all,ph, cova] = intersect(phenotype_subject,cova_subject_i);
    phenotype_fu2 = phenotype_fu2(ph);
    cova_data_se = cova_data_i(cova,:);
    
    phenotype_fu2 = zscore(xic_cpm_regress(phenotype_fu2,cova_data_se(:,1:8)));
    phenotype_subject = phenotype_subject(ph);
    
    
%  SST

    task_name = {'_SST_gowrong','_SST_stopfai','_SST_stopsuc'}; 
    xic_cpm_tset(go_wrong_subject,phenotype_subject,go_wrong,...
        phenotype_fu2,phenotype_name,thresh,task_name{1})
    
    xic_cpm_tset(stop_failure_subject,phenotype_subject,stop_failure,...
        phenotype_fu2,phenotype_name,thresh,task_name{2})
    
    xic_cpm_tset(stop_suces_subject,phenotype_subject,stop_suces,...
        phenotype_fu2,phenotype_name,thresh,task_name{3})

    
% MID
   
     task_name = {'_MID_antici_hit','_MID_feed_hit','_MID_feed_miss'}; 
    
    xic_cpm_tset(sub_mid_subject,phenotype_subject,sub_antici_hit_reward,...
        phenotype_fu2,phenotype_name,thresh,task_name{1})
    
    xic_cpm_tset(sub_mid_subject,phenotype_subject,sub_feed_hit_reward,...
        phenotype_fu2,phenotype_name,thresh,task_name{2})
    
    xic_cpm_tset(sub_mid_subject,phenotype_subject,sub_feed_miss_reward,...
        phenotype_fu2,phenotype_name,thresh,task_name{3})
     
end


%% FU3

clear;clc
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\S1\CPM_Models')

load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\FU3_External_Internal.mat');
load('FU3_psy_match.mat');
load('FU3_psy_name.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\S1\FU3_SST_CONN.mat')
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\S1\FU3_MID_CONN.mat')
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Cova_subject_jia.mat')

thresh = 0.01;
cova_data_all =repmat({cova_data},9,1);
cova_subject_all =repmat({cova_subject},9,1);
FU3_psy_match(isnan(FU3_psy_match))=0;
%FU3_psy_match=cat(2,sub_adhd_s,sub_cd_s,sub_eat_s,sub_dep_s,sub_anxiety_s,sub_sp_s);

for i=2:6

    phenotype_name = FU3_psy_name{i};
    phenotype_fu3 = FU3_psy_match(:,i);     
    phenotype_subject = sub_fu3;

% regress phenotype
     
   cova_subject_i = cova_subject_all{i};
   cova_data_i = cova_data_all{i};

    [all,ph, cova] = intersect(phenotype_subject,cova_subject_i);
    phenotype_fu3 = phenotype_fu3(ph);
    cova_data_se = cova_data_i(cova,:);
    
    phenotype_fu3 = zscore(xic_cpm_regress(phenotype_fu3,cova_data_se(:,1:8)));
    phenotype_subject = phenotype_subject(ph);
    
    
%  SST

    task_name = {'_SST_gowrong','_SST_stopfai','_SST_stopsuc'}; 
    xic_cpm_tset(go_wrong_subject,phenotype_subject,go_wrong,...
        phenotype_fu3,phenotype_name,thresh,task_name{1})
    
    xic_cpm_tset(stop_failure_subject,phenotype_subject,stop_failure,...
        phenotype_fu3,phenotype_name,thresh,task_name{2})
    
    xic_cpm_tset(stop_suces_subject,phenotype_subject,stop_suces,...
        phenotype_fu3,phenotype_name,thresh,task_name{3})

    
% MID
   
     task_name = {'_MID_antici_hit','_MID_feed_hit','_MID_feed_miss'}; 
    
    xic_cpm_tset(sub_mid_subject,phenotype_subject,sub_antici_hit_reward,...
        phenotype_fu3,phenotype_name,thresh,task_name{1})
    
    xic_cpm_tset(sub_mid_subject,phenotype_subject,sub_feed_hit_reward,...
        phenotype_fu3,phenotype_name,thresh,task_name{2})
    
    xic_cpm_tset(sub_mid_subject,phenotype_subject,sub_feed_miss_reward,...
        phenotype_fu3,phenotype_name,thresh,task_name{3})
     
end