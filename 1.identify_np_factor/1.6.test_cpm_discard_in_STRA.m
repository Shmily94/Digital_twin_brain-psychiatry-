%% run model on STRATIFY samples
clear;clc
%% clinical sample
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\FC_results\Shen_results\CONN_FC\STRATIFY_MID_SST_FC.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\control_id.mat');
[STRA_SST_subject2,ia]=setdiff(SST_subject,idx_discard); 
[STRA_MID_subject2,ib]=setdiff(MID_subjtec,idx_discard); 
STRA_SST_subject2(1:2,:)=[];
ia(1:2,:)=[];

Dis_data={MID_antici_hit(:,:,ib) MID_feedhit(:,:,ib) MID_feedmiss(:,:,ib) SST_stop_suces(:,:,ia) SST_stop_failure(:,:,ia) SST_go_wrong(:,:,ia)};
Dis_subject={MID_subjtec(ib) MID_subjtec(ib) MID_subjtec(ib) SST_subject(ia) SST_subject(ia) SST_subject(ia)};
model_name = {'_antici_hit.mat','_feed_hit.mat','_feed_miss.mat','_SST_stopsuc.mat','_SST_stopfai.mat','_SST_gowrong.mat'};
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\Behavior_related_results\beha_data\STRA_self_dawba.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Self_FU2_inter_exter.mat','FU2_self');

for i=1:6 % task condition
   for j=1:6 % beha symp

   models=dir(fullfile('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\',[FU2_self.FU2_psy_name{j},'_CPM','*',model_name{i}]));
   load(models.name);
   test_mat=Dis_data{i};
   [C,ia,ib]=intersect(Dis_subject{i},STRA_self.psy_match_sub);
   test_mat2=test_mat(:,:,ia);
   test_beha2=STRA_self.STRA_psy_match(ib,j);
   [r_pos,p_pos,r_neg,p_neg,r_all,p_all]=test_fcs_beha(test_mat2,test_beha2,CPM_Result);
   test_results{i,j}=[r_all,p_all;r_pos,p_pos;r_neg,p_neg];
   p_all_all(i,j)=p_all;
   r_all_all(i,j)=r_all;
   end
end
r_all_all(p_all_all>0.05)=0;
save STRA_Dis_validation_perfom test_results r_all_all p_all_all

%% HC sample
clear;clc
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\HC_brain_beha_cova.mat');
HC_data={MID_antici_hit MID_feed_hit MID_feed_miss SST_stop_sucess SST_stop_failure SST_go_wrong};
HC_subject={MID_subject MID_subject MID_subject SST_subject SST_subject SST_subject};
model_name = {'_antici_hit.mat','_feed_hit.mat','_feed_miss.mat','_SST_stopsuc.mat','_SST_stopfai.mat','_SST_gowrong.mat'};
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Self_FU2_inter_exter.mat','FU2_self');

for i=1:6 % task condition
   for j=1:6 % beha symp

   models=dir(fullfile('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\',[FU2_self.FU2_psy_name{j},'_CPM','*',model_name{i}]));
   load(models.name);
   test_mat=HC_data{i};
   [C,ia,ib]=intersect(HC_subject{i},beha.subject);
   test_mat2=test_mat(:,:,ia);
   test_beha2=beha.data(ib,j);
   [r_pos,p_pos,r_neg,p_neg,r_all,p_all]=test_fcs_beha(test_mat2,test_beha2,CPM_Result);
   test_results{i,j}=[r_all,p_all;r_pos,p_pos;r_neg,p_neg];
   p_all_all(i,j)=p_all;
   r_all_all(i,j)=r_all;
   end
end
r_all_all(p_all_all>0.05)=0;
save STRA_HC_validation_perfom test_results r_all_all p_all_all
