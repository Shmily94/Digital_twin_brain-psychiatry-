
%% calculate across fc degree for fu2 and fu3
clear;clc;close all
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2');
model_name = {'_SST_stopsuc.mat','_SST_stopfai.mat' ...
        'SST_gowrong.mat','feed_miss.mat','feed_hit.mat' ...
        'antici_hit.mat'};
model  = [1 2 5 6];

name = {'SST_stopsuccess','SST_stopfailure','SST_gowrong',...
       'MID_feedmiss','MID_feedhit','MID_anticihit'};
number=[1 3 2 4 5 6];
dis_names  = {'adhd','cd','anxiety','dep','eat','speph'};
load('A2_1_1_Network_P_factor_0927.mat')
mask_all = reshape(1:268*268,268,268);
nums_pp_all = zeros(2,4);
nums_nn_all = zeros(2,4);

for k= 1:4
    k
    models = dir(fullfile('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\',['*',model_name{model(k)}]));
    neg_neg = neg_neg_all_dimension{model(k)};
    neg_pos = neg_pos_all_dimension{model(k)};
    pos_pos = pos_pos_all_dimension{model(k)};
    pos_neg = pos_neg_all_dimension{model(k)};
    
    oppo_all = zeros(268,268); 
    oppo_all_pn = zeros(268,268);
    oppo_all_np = zeros(268,268);
    oppo_all_nn = zeros(268,268);
    oppo_all_pp = zeros(268,268);
    nums_pp=zeros(2,4);
    nums_nn=zeros(2,4);
    
    %% get the cross-disorder fc: external-postive FC, Internal Negative FC, Translation Pos-Neg FC

    for i = 1:2
         net1 = load(fullfile(models(1).folder,models(number(i)).name));
         R_value1 = mean(net1.CPM_Result.both_r_mean); 
         Rvalue1(i,k) = R_value1;
        for j=3:6
             net2 = load(fullfile(models(1).folder,models(number(j)).name));
             R_value2 = mean(net2.CPM_Result.both_r_mean);
             Rvalue2(j-2,k) = R_value2;
            if  R_value1 > 0.02 && R_value2 > 0.02
            if i~=j 
                pos_pos_net = tril(pos_pos{i,j});
                neg_neg_net = tril(neg_neg{i,j});
                oppo_all_pp =  oppo_all_pp +  pos_pos_net;
                oppo_all_nn =  oppo_all_nn +  neg_neg_net;
                nums_pp(i,j-2) = sum(sum(pos_pos_net));
                nums_nn(i,j-2) = sum(sum(neg_neg_net));
            end
            end
        end
    end
    
     nums_pp_all = nums_pp_all+nums_pp;
     nums_nn_all = nums_nn_all+nums_nn;

     oppo_pp_dimen{k} = oppo_all_pp; 
     oppo_pp_dimen_ind{k} = find(oppo_all_pp>0);
     oppo_nn_dimen{k} = oppo_all_nn; 
     oppo_nn_dimen_ind{k} = find(oppo_all_nn>0);

    Coss_matrix_single = array2table(nums_pp);
    Coss_matrix_single.Properties.VariableNames = dis_names(3:6);
    Coss_matrix_single = [cell2table(dis_names(1:2)'),Coss_matrix_single];
    Coss_matrix_single.Properties.VariableNames(1) = name(model(k));
    Coss_matrix_all{k,1} = Coss_matrix_single;
end


Coss_matrix = array2table(nums_pp_all);
Coss_matrix.Properties.VariableNames = dis_names(3:6);
Coss_matrix = [cell2table(dis_names(1:2)'),Coss_matrix];

Cross_FC = table;
Cross_FC.Exter_name = dis_names(1:2)';
Cross_FC.Exter_sum = sum(nums_pp_all,2);
Cross_FC.Inter_name = dis_names(3:6)';
Cross_FC.Inter_sum = sum(nums_pp_all)';
 
% imagesc(nums_all)
% xticks(1:4); xticklabels(dis_names(3:6))
% yticks(1:2); yticklabels(dis_names(1:2))
%
ind_fc_all = [];
for i=1:4
    
    ind_nn_fc = oppo_nn_dimen{i}(oppo_nn_dimen_ind{i});
    ind_pp_fc = oppo_pp_dimen{i}(oppo_pp_dimen_ind{i});
    %ind_pp_fc_all = [ind_fc_all;ind_pp_fc];
    %ind_nn_fc_all = [ind_fc_all;ind_nn_fc];
    ind_fc_pp_condi{i} = ind_pp_fc;
    ind_fc_nn_condi{i} = ind_nn_fc;
end
%[h p c t] = ttest2([ind_fc_condi{1};ind_fc_condi{2}],[ind_fc_condi{3};ind_fc_condi{4}] )
ind_pp_FC = [ind_fc_pp_condi{1};ind_fc_pp_condi{2}; ind_fc_pp_condi{3};ind_fc_pp_condi{4}] ;
ind_nn_FC = [ind_fc_nn_condi{1};ind_fc_nn_condi{2}; ind_fc_nn_condi{3};ind_fc_nn_condi{4}] ;

ind_nn_FC_ind = [oppo_nn_dimen_ind{1};oppo_nn_dimen_ind{2};oppo_nn_dimen_ind{3};oppo_nn_dimen_ind{4}];%每个task condition下的FC的idx
ind_pp_FC_ind = [oppo_pp_dimen_ind{1};oppo_pp_dimen_ind{2};oppo_pp_dimen_ind{3};oppo_pp_dimen_ind{4}];
%ind_FC_num = histc(ind_FC, unique(ind_FC));
%pie(ind_FC_num)
share_pp = oppo_pp_dimen{1} + oppo_pp_dimen{2}  + oppo_pp_dimen{3} +oppo_pp_dimen{4};
share_nn = oppo_nn_dimen{1} + oppo_nn_dimen{2}  + oppo_nn_dimen{3} +oppo_nn_dimen{4};
net_num = sum(sum(share_pp>0))
net_num = sum(sum(share_nn>0))

share_pp = share_pp + share_pp';
share_nn = share_nn + share_nn';
share_pp_degree1  = sum(share_pp,2); 
share_nn_degree1  = sum(share_nn,2); % 每个脑区的FC数量

save A2_2_1_2_make_mask_across_single_v2.mat Coss_matrix_all oppo_pp_dimen oppo_pp_dimen_ind ...
oppo_nn_dimen oppo_nn_dimen_ind ind_pp_FC ind_pp_FC_ind ind_nn_FC ind_nn_FC_ind share_pp share_pp_degree1 share_nn share_nn_degree1

xic_shen_template(share_pp_degree1,'pp_degree_corss.nii','D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\');
xic_shen_template(share_nn_degree1,'nn_degree_corss.nii','D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\');
