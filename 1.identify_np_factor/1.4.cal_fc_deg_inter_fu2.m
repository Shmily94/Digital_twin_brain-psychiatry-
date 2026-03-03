
%% calculate fc degree in internalizing for fu2 and fu3
clear;clc;close all
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\');
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
nums_pos_all = zeros(4,4);
nums_neg_all = zeros(4,4);
nums_pos=zeros(4,4);
nums_neg=zeros(4,4);
for k= 1:4
    k
    models = dir(fullfile('D:\postdoc\Work\Computer-Brain-Project\Results\Baseline\CPM_results\XIC_shen_results\FU2_Models\',['*',model_name{model(k)}]));
    % models = dir(fullfile('D:\postdoc\Work\Computer-Brain-Project\Results\Followup3\CPM_results\Shen_results\CPM_Models\',['*',model_name{model(k)}]));
    neg_neg = neg_neg_all_dimension{model(k)};
    neg_pos = neg_pos_all_dimension{model(k)};
    pos_pos = pos_pos_all_dimension{model(k)};
    pos_neg = pos_neg_all_dimension{model(k)};
    
    oppo_all = zeros(268,268); 
    oppo_all_pn = zeros(268,268);oppo_all_np = zeros(268,268);
    oppo_all_nn = zeros(268,268);oppo_all_pp = zeros(268,268);
    
    inter_all_nn = zeros(268,268);inter_all_pp = zeros(268,268);
    
    %% get the cross-disorder fc: external-postive FC, Internal Negative FC, Translation Pos-Neg FC

    for i = 3:6
         net1 = load(fullfile(models(1).folder,models(number(i)).name));
         R_value1 = mean(net1.CPM_Result.both_r_mean); 
         Rvalue1(i-2,k) = R_value1;
        for j=3:6
             net2 = load(fullfile(models(1).folder,models(number(j)).name));
             R_value2 = mean(net2.CPM_Result.both_r_mean);
             Rvalue2(j-2,k) = R_value2;
            if  R_value1 > 0.02 && R_value2 > 0.02
            
             if i~=j 
                pos_pos_net = tril(pos_pos{i,j});
                neg_neg_net = tril(neg_neg{i,j});
                inter_all_pp =  inter_all_pp +  pos_pos_net;
                inter_all_nn =  inter_all_nn +  neg_neg_net;
                nums_pos(i-2,j-2) = sum(sum(pos_pos_net));
                nums_neg(i-2,j-2) = sum(sum(neg_neg_net));
                
             end
            end
        end
    end
    
     nums_pos_all = nums_pos_all+nums_pos;
     nums_neg_all = nums_neg_all+nums_neg;
     inter_pp_dimen{k} = inter_all_pp; 
     inter_pp_dimen_ind{k} = find(inter_all_pp>0);
     inter_nn_dimen{k} = inter_all_nn; 
     inter_nn_dimen_ind{k} = find(inter_all_nn>0);

    % Coss_matrix_single = array2table(nums);
    % Coss_matrix_single.Properties.VariableNames = dis_names(3:6);
    % Coss_matrix_single = [cell2table(dis_names(3:6)'),Coss_matrix_single];
    % Coss_matrix_single.Properties.VariableNames(1) = name(model(k));
    % Coss_matrix_all{k,1} = Coss_matrix_single;
    
end

% 
% Coss_matrix = array2table(nums_all);
% Coss_matrix.Properties.VariableNames = dis_names(3:6);
% Coss_matrix = [cell2table(dis_names(1:2)'),Coss_matrix];
% 
% Cross_FC = table;
% Cross_FC.Exter_name = dis_names(1:2)';
% Cross_FC.Exter_sum = sum(nums_all,2);
% Cross_FC.Inter_name = dis_names(3:6)';
% Cross_FC.Inter_sum = sum(nums_all)';
% 
% 
% 
% imagesc(nums_all)
% xticks(1:4); xticklabels(dis_names(3:6))
% yticks(1:2); yticklabels(dis_names(1:2))
% 

ind_pos_fc_all = [];
ind_neg_fc_all = [];
for i=1:4

    ind_pos_fc = inter_pp_dimen{i}(inter_pp_dimen_ind{i});
    ind_pos_fc_all = [ind_pos_fc_all;ind_pos_fc];
    ind_pos_fc_condi{i} = ind_pos_fc;

    ind_neg_fc = inter_nn_dimen{i}(inter_nn_dimen_ind{i});
    ind_neg_fc_all = [ind_neg_fc_all;ind_neg_fc];
    ind_neg_fc_condi{i} = ind_neg_fc;
end
% fc num of 4 task conditions

[h p c t] = ttest2([ind_pos_fc_condi{1};ind_pos_fc_condi{2}],[ind_pos_fc_condi{3};ind_pos_fc_condi{4}] )
ind_pos_FC = [ind_pos_fc_condi{1};ind_pos_fc_condi{2}; ind_pos_fc_condi{3};ind_pos_fc_condi{4}] ;
ind_pos_FC_ind = [inter_pp_dimen_ind{1};inter_pp_dimen_ind{2};inter_pp_dimen_ind{3};inter_pp_dimen_ind{4}];
% ind_pos_FC_num = histc(ind_pos_FC, unique(ind_pos_FC));
ind_neg_FC = [ind_neg_fc_condi{1};ind_neg_fc_condi{2}; ind_neg_fc_condi{3};ind_neg_fc_condi{4}] ;
ind_neg_FC_ind = [inter_nn_dimen_ind{1};inter_nn_dimen_ind{2};inter_nn_dimen_ind{3};inter_nn_dimen_ind{4}];
 

share_pp{1} = inter_pp_dimen{1} + inter_pp_dimen{2}  + inter_pp_dimen{3} +inter_pp_dimen{4};
net_num = sum(sum(share_pp{1}>0));
share_pp{1} =  share_pp{1}+(share_pp{1})';
share_pp_degree1  = sum(share_pp{1},2);

share_nn{1} = inter_nn_dimen{1} + inter_nn_dimen{2}  + inter_nn_dimen{3} +inter_nn_dimen{4};
share_nn{1} =  share_nn{1}+(share_nn{1})';
share_nn_degree1  = sum(share_nn{1},2);

save inter_pp_nn_degree.mat inter_pp_dimen_ind inter_nn_dimen_ind ind_pos_FC ind_neg_FC ind_pos_FC_ind ind_neg_FC_ind inter_pp_dimen inter_nn_dimen share_pp share_pp_degree1 share_nn share_nn_degree1


