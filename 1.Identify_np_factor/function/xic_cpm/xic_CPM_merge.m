

function [CPM_Result] = xic_CPM_merge(all_mats_set1,all_mats_set2,all_mats_set3,all_behav_set,thresh_set)



all_mats1  = all_mats_set1;
all_mats2  = all_mats_set2;
all_mats3  = all_mats_set3;

all_behav = all_behav_set;
% all_mats(out,:)=[];
% all_behav(out,:)=[];
% threshold for feature selection
thresh = thresh_set;

% try

% ---------------------------------------

no_sub = size(all_mats_set1,1);
no_node = size(all_mats_set1,2);

behav_pred_pos = zeros(no_sub,1);
behav_pred_neg = zeros(no_sub,1);
% 
% mask_pos_final = zeros(size(all_mats_set1,2),length(no_sub));
% mask_neg_final = zeros(size(all_mats,2),length(no_sub));
    
    
parfor leftout = 1:no_sub
    fprintf('\n Leaving out subject # %6.3f',leftout);
    
    
    % part 1
    % leave out subject from matrices and behavior
    
    train_mats1 = all_mats1;
    train_mats1(leftout,:) = [];    
    
    train_mats2 = all_mats2;
    train_mats2(leftout,:) = [];  
    
    train_mats3 = all_mats3;
    train_mats3(leftout,:) = [];
    
    train_behav = all_behav;
    train_behav(leftout) = [];
    

    [train_sumpos1,pos_mask1,train_sumneg1,neg_mask1,train_all1,mask_all1] = CPM_train(train_mats1,train_behav,thresh);
    [train_sumpos2,pos_mask2,train_sumneg2,neg_mask2,train_all2,mask_all2] = CPM_train(train_mats2,train_behav,thresh);
    [train_sumpos3,pos_mask3,train_sumneg3,neg_mask3,train_all3,mask_all3] = CPM_train(train_mats3,train_behav,thresh);
    
    all_pos_train=train_sumpos1+train_sumpos2+train_sumpos3;
    all_neg_train=train_sumneg1+train_sumneg2+train_sumneg3;
    all_overall_train=train_all1+train_all2+train_all3;
    
    % build model on TRAIN subs
    fit_pos = polyfit(all_pos_train, train_behav,1);
    fit_neg = polyfit(all_neg_train, train_behav,1);
    fit_all = polyfit(all_overall_train, train_behav,1);
    
    % run model on TEST sub

    test_mat1 = all_mats1(leftout,:);
    test_sumpos1 = sum(test_mat1((pos_mask1==1)))/2;
    test_sumneg1 = sum(test_mat1((neg_mask1==1)))/2;
    test_sumall1 = sum(test_mat1((mask_all1==1)))/2;
 
    test_mat2 = all_mats2(leftout,:);
    test_sumpos2 = sum(test_mat2((pos_mask2==1)))/2;
    test_sumneg2 = sum(test_mat2((neg_mask2==1)))/2;
    test_sumall2 = sum(test_mat2((mask_all2==1)))/2;
    
    test_mat3 = all_mats3(leftout,:);
    test_sumpos3 = sum(test_mat3((pos_mask3==1)))/2;
    test_sumneg3 = sum(test_mat3((neg_mask3==1)))/2;
    test_sumall3 = sum(test_mat3((mask_all3==1)))/2;
    
    test_sumneg =  test_sumpos1+ test_sumpos2+test_sumpos3;
    test_sumpos =  test_sumneg1+ test_sumneg2+test_sumneg3;
    test_sumall =  test_sumall1+ test_sumall2+test_sumall3;
    
    
    
    behav_pred_pos(leftout) = fit_pos(1)*test_sumpos + fit_pos(2);
    behav_pred_neg(leftout) = fit_neg(1)*test_sumneg + fit_neg(2);
    behav_pred_all(leftout) = fit_all(1)*test_sumall + fit_all(2);
       
    
end   
test = all_behav;
test((isnan(behav_pred_pos)))=[];
behav_pred_pos(isnan(behav_pred_pos))=[];

test2 = all_behav;
test2((isnan(behav_pred_neg)))=[];
behav_pred_neg(isnan(behav_pred_neg))=[];

test3 = all_behav;
test3((isnan(behav_pred_all)))=[];
behav_pred_all(isnan(behav_pred_all))=[];

% compare predicted and observed scores
  
[R_pos, P_pos] = corr(behav_pred_pos,test);
[R_neg, P_neg] = corr(behav_pred_neg,test2);
[R_both, P_both] = corr(behav_pred_all,test3);

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
CPM_Result.both_predict = behav_pred_all;
CPM_Result.both_test = test3;
CPM_Result.mask_neg = mask_both_final;

figure(1); plot(test,behav_pred_pos,'r.'); lsline;title([num2str(P_pos),'|',num2str(R_pos)])
figure(2); plot(test2,behav_pred_neg,'b.'); lsline;title([num2str(P_neg),'|',num2str(R_neg)])
figure(3); plot(test3,behav_pred_all,'m.'); lsline;title([num2str(P_both),'|',num2str(R_both)]) 


end






