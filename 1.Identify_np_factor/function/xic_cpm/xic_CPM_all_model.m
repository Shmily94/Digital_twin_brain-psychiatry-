
function [CPM_Result] = xic_CPM_all_model(all_mats_toghther,all_behav,thresh)




all_mats  = all_mats_toghther{1};
all_behav = all_behav;
thresh = thresh;


all_mats_nan_mask = all_mats(1,:);
nan_fc = isnan(all_mats_nan_mask);
all_mats_toghther = cellfun(@(x) x(:,nan_fc==0),all_mats_toghther,'UniformOutput', false); 


all_mats_nan = all_mats(:,2);
nan_subject = isnan(all_mats_nan);
all_mats_toghther = cellfun(@(x) x(nan_subject==0,:),all_mats_toghther,'UniformOutput', false); 


all_behav(isnan(all_mats_nan),:)=[];
% cellfun(@(x) x(all_mats_nan~=1,:),beha_cpm,'UniformOutput', false); 

all_mats  = all_mats_toghther{1};


% all_mats_toghther_cpm = [all_mats_toghther,beha_cpm]; 
all_mats_toghther_cpm = [all_mats_toghther]; 
% ---------------------------------------

no_sub = size(all_mats,1);
no_node = size(all_mats,2);

behav_pred_pos = zeros(no_sub,1);
behav_pred_neg = zeros(no_sub,1);
behav_pred_both = zeros(no_sub,1);

mask_pos_final = zeros(size(all_mats,2),no_sub);
mask_neg_final = zeros(size(all_mats,2),no_sub);
mask_both_final = zeros(size(all_mats,2),no_sub);


    
parfor leftout = 1:no_sub
    tic
    fprintf('\n Leaving out subject # %6.3f',leftout);
    
    % leave out subject from matrices and behavior
   
    all_mats_toghther_cpm_train = all_mats_toghther_cpm;
    subject = 1:no_sub;subject(leftout)=[];
    
    all_mats_toghther_cpm_train = cellfun(@(x) x(subject,:),all_mats_toghther_cpm_train,'UniformOutput', false); 
    
    train_behav = all_behav;
    train_behav(leftout) = [];
    
    % correlate all edges with behavior
    [r_mat,p_mat] = cellfun(@(x) corr(x,train_behav),all_mats_toghther_cpm_train,'UniformOutput', false); 
    
    % set threshold and define masks
    

    [pos_edges_mat] = cellfun(@(x,y) x>0&y<thresh,r_mat,p_mat,'UniformOutput', false); 
    [neg_edges_mat] = cellfun(@(x,y) x<0&y<thresh,r_mat,p_mat,'UniformOutput', false); 
    
    [pos_edges_mat_final] = cellfun(@(x,y) x(:,y>0),all_mats_toghther_cpm_train,pos_edges_mat,'UniformOutput', false); 
    [neg_edges_mat_final] = cellfun(@(x,y) x(:,y>0),all_mats_toghther_cpm_train,neg_edges_mat,'UniformOutput', false); 
   
    
    % get sum of all edges in TRAIN subs (divide by 2 to control for the
    % fact that matrices are symmetric)
    
    [pos_edges_mat_sum] = cellfun(@(x) (sum(x,2)),pos_edges_mat_final,'UniformOutput', false); 
    [neg_edges_mat_sum] = cellfun(@(x) (sum(x,2)),neg_edges_mat_final,'UniformOutput', false); 
%     clear pos_edges_mat_final neg_edges_mat_final
    
    pos_edges_mat_sum = sum(cell2mat(pos_edges_mat_sum),2);
    neg_edges_mat_sum = sum(cell2mat(neg_edges_mat_sum),2);
 
    
    % build model on TRAIN subs
    fit_pos = polyfit(pos_edges_mat_sum, train_behav,1);
    fit_neg = polyfit(neg_edges_mat_sum, train_behav,1);
    
    fit_both = polyfit(pos_edges_mat_sum-neg_edges_mat_sum, train_behav,1);
%     clear pos_edges_mat_sum neg_edges_mat_sum
    
    % run model on TEST sub

    test_mat = cellfun(@(x) x(leftout,:),all_mats_toghther_cpm,'UniformOutput', false); 
    test_sumpos = cellfun(@(x,y) x(:,y>0),test_mat,pos_edges_mat,'UniformOutput', false); 
    test_sumneg = cellfun(@(x,y) x(:,y>0),test_mat,neg_edges_mat,'UniformOutput', false);
%     clear test_mat pos_edges_mat neg_edges_mat all_mats_toghther_cpm_train
    
    [test_sumpos_sum] = cellfun(@(x) sum(x,2),test_sumpos,'UniformOutput', false); 
    [test_sumneg_sum] = cellfun(@(x) sum(x,2),test_sumneg,'UniformOutput', false); 
%    clear test_sumpos test_sumneg
    
    pos_test_sumpos_sum = (sum(cell2mat(test_sumpos_sum),2));
    neg_test_sumneg_sum = (sum(cell2mat(test_sumneg_sum),2));
%    clear test_sumpos_sum test_sumneg_sum
       
    behav_pred_pos(leftout) = fit_pos(1)*pos_test_sumpos_sum + fit_pos(2);
    behav_pred_neg(leftout) = fit_neg(1)*neg_test_sumneg_sum + fit_neg(2);
    behav_pred_both(leftout) = fit_both(1)*(pos_test_sumpos_sum-neg_test_sumneg_sum) + fit_both(2);
    toc
end

test = all_behav;
test((isnan(behav_pred_pos)))=[];
behav_pred_pos(isnan(behav_pred_pos))=[];

test2 = all_behav;
test2((isnan(behav_pred_neg)))=[];
behav_pred_neg(isnan(behav_pred_neg))=[];

test3 = all_behav;
test3((isnan(behav_pred_both)))=[];
behav_pred_both(isnan(behav_pred_both))=[];

% compare predicted and observed scores
  
[R_pos, P_pos] = corr(behav_pred_pos,test);
[R_neg, P_neg] = corr(behav_pred_neg,test2);
[R_both, P_both] = corr(behav_pred_both,test3);

CPM_Result.R_pos = R_pos;
CPM_Result.P_pos = P_pos;
CPM_Result.pos_predict = behav_pred_pos;
CPM_Result.pos_test = test;
CPM_Result.mask_pos = mask_pos_final;


CPM_Result.R_neg = R_neg;
CPM_Result.P_neg = P_neg;
CPM_Result.neg_predict = behav_pred_neg;
CPM_Result.neg_test = test2;
CPM_Result.mask_neg = mask_neg_final;

CPM_Result.R_both = R_both;
CPM_Result.P_both = P_both;
CPM_Result.both_predict = behav_pred_both;
CPM_Result.both_test = test3;
CPM_Result.mask_both = mask_both_final;

figure(1); plot(test,behav_pred_pos,'r.'); lsline;title([num2str(P_pos),'|',num2str(R_pos)])
figure(2); plot(test2,behav_pred_neg,'b.'); lsline;title([num2str(P_neg),'|',num2str(R_neg)])
figure(3); plot(test3,behav_pred_both,'m.'); lsline;title([num2str(P_both),'|',num2str(R_both)])
% catch
    
end


% end


