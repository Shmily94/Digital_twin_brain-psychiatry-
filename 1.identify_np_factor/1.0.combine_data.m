%% combine control brain,cova,beha_symptoms
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\HC');
clear;clc
% Stratify control
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\Behavior_related_results\beha_data\STRA_self_dawba.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\FC_results\Shen_results\CONN_FC\STRATIFY_MID_SST_FC.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\Cova_subject_stra.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\control_id.mat');

% control的FC，cov,beha
[STRA_SST_subject2,ia]=intersect(SST_subject,idx_discard); 
[STRA_MID_subject2,ib]=intersect(MID_subjtec,idx_discard); 
STRA_SST_stop_suces=SST_stop_suces(:,:,ia);
STRA_SST_stop_failure=SST_stop_failure(:,:,ia);
STRA_SST_go_wrong=SST_go_wrong(:,:,ia);
STRA_MID_antici_hit=MID_antici_hit(:,:,ib);
STRA_MID_feedhit=MID_feedhit(:,:,ib);
STRA_MID_feedmiss=MID_feedmiss(:,:,ib);

[STRA_beha_subject2,ic]=intersect(STRA_self.psy_match_sub,idx_discard); 
STRA_beha_data=STRA_self.STRA_psy_match(ic,:);

[STRA_cova_subject2,id]=intersect(cova_subject,idx_discard); 
STRA_cova_data2=cova_data(id,:);
save STRA_control STRA_SST_subject2 STRA_SST_stop_suces STRA_SST_stop_failure STRA_SST_go_wrong...
    STRA_MID_subject2 STRA_MID_antici_hit STRA_MID_feedhit STRA_MID_feedmiss STRA_beha_subject2 STRA_beha_data...
    STRA_cova_subject2 STRA_cova_data2

%FU2 control
clear;clc
load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\FU2_SST_CONN_Name_match.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\FU2_Match_MID_CONN.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Self_FU2_inter_exter.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro\FU2_control_NP_factor.mat','FU2_control_id2');
[FU2_MID_subject2,ia]=intersect(FU2_MID_subname,FU2_control_id2);
[FU2_SST_subject2,ib]=intersect(SST_subject,FU2_control_id2);
FU2_MID_antici_hit=FU2_MID_antici_hit(:,:,ia);
FU2_MID_feed_hit=FU2_MID_feed_hit(:,:,ia);
FU2_MID_feed_miss=FU2_MID_feed_miss(:,:,ia);
FU2_SST_stop_sucess=FU2_SST_stop_sucess(:,:,ib);
FU2_SST_stop_failure=FU2_SST_stop_failure(:,:,ib);
FU2_SST_go_wrong=FU2_SST_go_wrong(:,:,ib);
[FU2_beha_subject2,ic]=intersect(FU2_self.FU2_psy_match_sub,FU2_control_id2); 
FU2_beha_data=FU2_self.FU2_psy_match(ic,:);
save FU2_control FU2_MID_subject2 FU2_MID_antici_hit FU2_MID_feed_hit FU2_MID_feed_miss FU2_SST_subject2 FU2_SST_stop_sucess...
    FU2_SST_stop_failure FU2_SST_go_wrong FU2_beha_subject2 FU2_beha_data

%FU3 control
clear;clc
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\CPM_results\Shen_results\CPM_results\FU3_SST_data_all.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\CPM_results\Shen_results\CPM_results\FU3_MID_data_all.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\CPM_results\Shen_results\CPM_Models\FU3_psy_match.mat');
% load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\CPM_results\Shen_results\CPM_Models\FU3_psy_name.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\FU3_External_Internal.mat','sub_fu3');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro\FU3_control_NP_factor.mat','FU3_control_id2');
[FU3_MID_subject2,ia]=intersect(mid_subject,FU3_control_id2);
[FU3_SST_subject2,ib]=intersect(sst_subject,FU3_control_id2);
FU3_MID_antici_hit=mid_antici_hit(:,:,ia);
FU3_MID_feed_hit=mid_feed_hit(:,:,ia);
FU3_MID_feed_miss=mid_feed_miss(:,:,ia);
FU3_SST_stop_sucess=sst_stop_suces(:,:,ib);
FU3_SST_stop_failure=sst_stop_failure(:,:,ib);
FU3_SST_go_wrong=sst_go_wrong(:,:,ib);
[FU3_beha_subject2,ic]=intersect(sub_fu3,FU3_control_id2); 
FU3_beha_data=FU3_psy_match(ic,:);
save FU3_control FU3_MID_subject2 FU3_MID_antici_hit FU3_MID_feed_hit FU3_MID_feed_miss FU3_SST_subject2 FU3_SST_stop_sucess...
    FU3_SST_stop_failure FU3_SST_go_wrong FU3_beha_subject2 FU3_beha_data
