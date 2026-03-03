clear;clc
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2');
%% cal fcs for STRATIFY
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\FC_results\Shen_results\CONN_FC\Striatify_Match_MID_CONN.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\FC_results\Shen_results\CONN_FC\Striatify_Match_SST_CONN.mat');

MID_antici_hit=cat(3,Striatify_MID_antici_hit1,Striatify_MID_antici_hit);
MID_feedhit=cat(3,Striatify_MID_feedhit1,Striatify_MID_feedhit);
MID_feedmiss=cat(3,Striatify_MID_feedmiss1,Striatify_MID_feedmiss);
SST_stop_suces=cat(3,Striatify_SST_stop_suces1,Striatify_SST_stop_suces);
SST_stop_failure=cat(3,Striatify_SST_stop_failure1,Striatify_SST_stop_failure);
SST_go_wrong=cat(3,Striatify_SST_go_wrong1,Striatify_SST_go_wrong);
MID_subjtec=[Striatify_MID_subject1;Striatify_MID_subject];
SST_subject=[Striatify_SST_subject1;Striatify_SST_subject];
[C,ia,ib]=intersect(MID_subjtec,SST_subject);
MID_antici_hit=MID_antici_hit(:,:,ia);
MID_feedhit=MID_feedhit(:,:,ia);
MID_feedmiss=MID_feedmiss(:,:,ia);
SST_stop_suces=SST_stop_suces(:,:,ib);
SST_stop_failure=SST_stop_failure(:,:,ib);
SST_go_wrong=SST_go_wrong(:,:,ib);

save STRATIFY_MID_SST_same_id_FC C MID_antici_hit MID_feedhit MID_feedmiss SST_stop_suces SST_stop_failure SST_go_wrong

%pos fc
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\A2_2_1_2_make_mask_across_single_v2.mat','oppo_pp_dimen_ind');
for n=1:length(C)

FC1_pos=SST_stop_suces(:,:,n);
FCS1_pos(n,1)=sum(FC1_pos(oppo_pp_dimen_ind{1}));

FC2_pos=SST_stop_failure(:,:,n);
FCS2_pos(n,1)=sum(FC2_pos(oppo_pp_dimen_ind{2}));

FC3_pos=MID_feedhit(:,:,n);
FCS3_pos(n,1)=sum(FC3_pos(oppo_pp_dimen_ind{3}));

FC4_pos=MID_antici_hit(:,:,n);
FCS4_pos(n,1)=sum(FC4_pos(oppo_pp_dimen_ind{4}));

end
NP_factor=FCS1_pos+FCS2_pos+FCS3_pos+FCS4_pos;

%neg fc
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\A2_2_1_2_make_mask_across_single_v2.mat','oppo_nn_dimen_ind');

for n=1:length(C)

FC1_neg=SST_stop_suces(:,:,n);
FCS1_neg(n,1)=sum(FC1_neg(oppo_nn_dimen_ind{1}));

FC2_neg=SST_stop_failure(:,:,n);
FCS2_neg(n,1)=sum(FC2_neg(oppo_nn_dimen_ind{2}));

FC3_neg=MID_feedhit(:,:,n);
FCS3_neg(n,1)=sum(FC3_neg(oppo_nn_dimen_ind{3}));

FC4_neg=MID_antici_hit(:,:,n);
FCS4_neg(n,1)=sum(FC4_neg(oppo_nn_dimen_ind{4}));

end
NP_factor_neg=FCS1_neg+FCS2_neg+FCS3_neg+FCS4_neg;
save STRATIFY_NP_factor NP_factor NP_factor_neg C

%% cal fcs for STRATIFY control
clear;clc
load("STRATIFY_NP_factor.mat");
load('STRATIFY_control_id.mat');
[STRA_dis_id,ia]=setdiff(C,STRA_control_id);
NP_factor_stra_dis=[NP_factor(ia,1),NP_factor_neg(ia,1)]; % diseased NP
[STRA_control_id2,ia,ib]=intersect(C,STRA_control_id);
NP_factor_stra_control=[NP_factor(ia,1),NP_factor_neg(ia,1)]; %Stratify control NP
save STRA_NP_dis_control NP_factor_stra_dis STRA_dis_id NP_factor_stra_control STRA_control_id2

%% cal fcs for FU2
clear;clc
load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\FU2_SST_CONN_Name_match.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\FU2_Match_MID_CONN.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro\idx_discard.mat');
[C,ia,ib]=intersect(FU2_MID_subname,SST_subject);
FU2_MID_antici_hit=FU2_MID_antici_hit(:,:,ia);
FU2_MID_feed_hit=FU2_MID_feed_hit(:,:,ia);
FU2_MID_feed_miss=FU2_MID_feed_miss(:,:,ia);
FU2_SST_stop_sucess=FU2_SST_stop_sucess(:,:,ib);
FU2_SST_stop_failure=FU2_SST_stop_failure(:,:,ib);
FU2_SST_go_wrong=FU2_SST_go_wrong(:,:,ib);

[FU2_control_id2,ia,ib]=intersect(C,idx_discard);%从FU2抽出的Control的id
FU2_MID_antici_hit2=FU2_MID_antici_hit(:,:,ia);
FU2_MID_feed_hit2=FU2_MID_feed_hit(:,:,ia);
FU2_MID_feed_miss2=FU2_MID_feed_miss(:,:,ia);
FU2_SST_stop_sucess2=FU2_SST_stop_sucess(:,:,ia);
FU2_SST_stop_failure2=FU2_SST_stop_failure(:,:,ia);
FU2_SST_go_wrong2=FU2_SST_go_wrong(:,:,ia);

% [FU2_control_id2,ia]=setdiff(C,idx_discard);%从FU2排除掉Control的id
% FU2_MID_antici_hit2=FU2_MID_antici_hit(:,:,ia);
% FU2_MID_feed_hit2=FU2_MID_feed_hit(:,:,ia);
% FU2_MID_feed_miss2=FU2_MID_feed_miss(:,:,ia);
% FU2_SST_stop_sucess2=FU2_SST_stop_sucess(:,:,ia);
% FU2_SST_stop_failure2=FU2_SST_stop_failure(:,:,ia);
% FU2_SST_go_wrong2=FU2_SST_go_wrong(:,:,ia);

%pos fc
load('A2_2_1_2_make_mask_across_single_v2.mat','oppo_pp_dimen_ind');
for n=1:length(FU2_control_id2)
FC1_pos=FU2_SST_stop_sucess2(:,:,n);
FCS1_pos(n,1)=sum(FC1_pos(oppo_pp_dimen_ind{1}));
FC2_pos=FU2_SST_stop_failure2(:,:,n);
FCS2_pos(n,1)=sum(FC2_pos(oppo_pp_dimen_ind{2}));
FC3_pos=FU2_MID_feed_hit2(:,:,n);
FCS3_pos(n,1)=sum(FC3_pos(oppo_pp_dimen_ind{3}));
FC4_pos=FU2_MID_antici_hit2(:,:,n);
FCS4_pos(n,1)=sum(FC4_pos(oppo_pp_dimen_ind{4}));
end
NP_factor=FCS1_pos+FCS2_pos+FCS3_pos+FCS4_pos;

%neg fc
load('A2_2_1_2_make_mask_across_single_v2.mat','oppo_nn_dimen_ind');
for n=1:length(FU2_control_id2)
FC1_neg=FU2_SST_stop_sucess2(:,:,n);
FCS1_neg(n,1)=sum(FC1_neg(oppo_nn_dimen_ind{1}));
FC2_neg=FU2_SST_stop_failure2(:,:,n);
FCS2_neg(n,1)=sum(FC2_neg(oppo_nn_dimen_ind{2}));
FC3_neg=FU2_MID_feed_hit2(:,:,n);
FCS3_neg(n,1)=sum(FC3_neg(oppo_nn_dimen_ind{3}));
FC4_neg=FU2_MID_antici_hit2(:,:,n);
FCS4_neg(n,1)=sum(FC4_neg(oppo_nn_dimen_ind{4}));
end
NP_factor_neg=FCS1_neg+FCS2_neg+FCS3_neg+FCS4_neg;
save FU2_control_NP_factor NP_factor NP_factor_neg FU2_control_id2
%% cal fcs for FU3
clear;clc
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\CPM_results\Shen_results\CPM_results\FU3_SST_data_all.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\CPM_results\Shen_results\CPM_results\FU3_MID_data_all.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\FU3_control_id.mat');
[C,ia,ib]=intersect(mid_subject,sst_subject);
FU3_MID_antici_hit=mid_antici_hit(:,:,ia);
FU3_MID_feed_hit=mid_feed_hit(:,:,ia);
FU3_MID_feed_miss=mid_feed_miss(:,:,ia);
FU3_SST_stop_sucess=sst_stop_suces(:,:,ib);
FU3_SST_stop_failure=sst_stop_failure(:,:,ib);
FU3_SST_go_wrong=sst_go_wrong(:,:,ib);

[FU3_control_id2,ia,ib]=intersect(C,FU3_control_id);%从FU3抽出的Control的id
FU3_MID_antici_hit2=FU3_MID_antici_hit(:,:,ia);
FU3_MID_feed_hit2=FU3_MID_feed_hit(:,:,ia);
FU3_MID_feed_miss2=FU3_MID_feed_miss(:,:,ia);
FU3_SST_stop_sucess2=FU3_SST_stop_sucess(:,:,ia);
FU3_SST_stop_failure2=FU3_SST_stop_failure(:,:,ia);
FU3_SST_go_wrong2=FU3_SST_go_wrong(:,:,ia);

%pos fc
load('A2_2_1_2_make_mask_across_single_v2.mat','oppo_pp_dimen_ind');
for n=1:length(FU3_control_id2)
FC1_pos=FU3_SST_stop_sucess2(:,:,n);
FCS1_pos(n,1)=sum(FC1_pos(oppo_pp_dimen_ind{1}));
FC2_pos=FU3_SST_stop_failure2(:,:,n);
FCS2_pos(n,1)=sum(FC2_pos(oppo_pp_dimen_ind{2}));
FC3_pos=FU3_MID_feed_hit2(:,:,n);
FCS3_pos(n,1)=sum(FC3_pos(oppo_pp_dimen_ind{3}));
FC4_pos=FU3_MID_antici_hit2(:,:,n);
FCS4_pos(n,1)=sum(FC4_pos(oppo_pp_dimen_ind{4}));
end
NP_factor=FCS1_pos+FCS2_pos+FCS3_pos+FCS4_pos;

%neg fc
load('A2_2_1_2_make_mask_across_single_v2.mat','oppo_nn_dimen_ind');
for n=1:length(FU3_control_id2)
FC1_neg=FU3_SST_stop_sucess2(:,:,n);
FCS1_neg(n,1)=sum(FC1_neg(oppo_nn_dimen_ind{1}));
FC2_neg=FU3_SST_stop_failure2(:,:,n);
FCS2_neg(n,1)=sum(FC2_neg(oppo_nn_dimen_ind{2}));
FC3_neg=FU3_MID_feed_hit2(:,:,n);
FCS3_neg(n,1)=sum(FC3_neg(oppo_nn_dimen_ind{3}));
FC4_neg=FU3_MID_antici_hit2(:,:,n);
FCS4_neg(n,1)=sum(FC4_neg(oppo_nn_dimen_ind{4}));
end
NP_factor_neg=FCS1_neg+FCS2_neg+FCS3_neg+FCS4_neg;
save FU3_control_NP_factor NP_factor NP_factor_neg FU3_control_id2

%% compare hc and diseased
clear;clc
load('STRA_NP_dis_control.mat');
load('FU2_control_NP_factor.mat');
NP_factor_fu2_control=[NP_factor,NP_factor_neg];
load('FU3_control_NP_factor.mat');
NP_factor_fu3_control=[NP_factor,NP_factor_neg];
NP_HC=[NP_factor_stra_control;NP_factor_fu2_control;NP_factor_fu3_control];
NP_HC_id=[STRA_control_id2;FU2_control_id2;FU3_control_id2];
load('STRA_NP_dis_control.mat');
NP_dis=NP_factor_stra_dis;
NP_dis_id=STRA_dis_id;
save NP_HC_dis NP_HC NP_HC_id NP_dis NP_dis_id
