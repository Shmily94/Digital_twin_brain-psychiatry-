
clear;clc

load('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM\XIC_shen\FU2_Models\A2_1_1_Network_P_factor.mat');

%% within internalizing neg-neg
idx1=TableS6.TableS6_across.SST_stop_sucess_id{5,1};
idx2=TableS6.TableS6_across.SST_stop_failure_id{5,1};
idx3=TableS6.TableS6_across.MID_feedhit_id{5,1};
idx4=TableS6.TableS6_across.MID_anticip_id{5,1};

load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\FU2_MID_data_all.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\FU2_SST_data_all.mat');

mask_id_all = tril(reshape(1:268*268,268,268),-1);

for i=1:length(idx4) % idx1,idx2,idx3,idx4

[row, col] = ind2sub(size(mask_id_all), idx4(i,1));
%FC1(i,:)=sst_stop_suces(row,col,:);
%FC2(i,:)=sst_stop_failure(row,col,:);
%FC3(i,:)=mid_feed_hit(row,col,:);
FC4(i,:)=mid_antici_hit(row,col,:);

end

[C,ia,ib]=intersect(mid_subject,sst_subject);
C_sst_stop_suces=FC1(:,ib);
C_sst_stop_failure=FC2(:,ib);
C_mid_feed_hit=FC3(:,ia);
C_mid_antici_hit=FC4(:,ia);

FC_in_nn=sum([C_sst_stop_suces',C_sst_stop_failure',C_mid_feed_hit',C_mid_antici_hit'],2);
FC_in_nn_all.C_sst_stop_suces=C_sst_stop_suces;
FC_in_nn_all.C_sst_stop_failure=C_sst_stop_failure;
FC_in_nn_all.C_mid_feed_hit=C_mid_feed_hit;
FC_in_nn_all.C_mid_antici_hit=C_mid_antici_hit;

%% within internalizing pos-pos
clear FC1 FC2 FC3 FC4
idx1=TableS6.TableS6_across.SST_stop_sucess_id{4,1};
idx2=TableS6.TableS6_across.SST_stop_failure_id{4,1};
idx3=TableS6.TableS6_across.MID_feedhit_id{4,1};
idx4=TableS6.TableS6_across.MID_anticip_id{4,1};

for i=1:length(idx4) % idx1,idx2,idx3,idx4

[row, col] = ind2sub(size(mask_id_all), idx4(i,1));
%FC1(i,:)=sst_stop_suces(row,col,:);
%FC2(i,:)=sst_stop_failure(row,col,:);
%FC3(i,:)=mid_feed_hit(row,col,:);
FC4(i,:)=mid_antici_hit(row,col,:);

end

%[C,ia,ib]=intersect(mid_subject,sst_subject);

C_sst_stop_suces=FC1(:,ib);
C_sst_stop_failure=FC2(:,ib);
C_mid_feed_hit=FC3(:,ia);
C_mid_antici_hit=FC4(:,ia);

FC_in_pp=sum([C_sst_stop_suces',C_sst_stop_failure',C_mid_feed_hit',C_mid_antici_hit'],2);
FC_in_pp_all.C_sst_stop_suces=C_sst_stop_suces;
FC_in_pp_all.C_sst_stop_failure=C_sst_stop_failure;
FC_in_pp_all.C_mid_feed_hit=C_mid_feed_hit;
FC_in_pp_all.C_mid_antici_hit=C_mid_antici_hit;

save CPM_fu2_key_fcs FC_in_nn_all FC_in_nn FC_in_pp_all FC_in_pp C
