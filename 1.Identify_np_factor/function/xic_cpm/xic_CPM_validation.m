
function [CPM_Result] = xic_CPM_validation(all_mats_set,all_behav_set,thresh_set)



all_mats  = all_mats_set;
all_behav = all_behav_set;
thresh = thresh_set;


all_mats_nan_mask = all_mats(1,:);
all_mats(:,isnan(all_mats_nan_mask))=[];

all_mats_nan = all_mats(:,2);
all_mats(isnan(all_mats_nan),:)=[];
all_behav(isnan(all_mats_nan),:)=[];

try

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
    fprintf('\n Leaving out subject # %6.3f',leftout);
    
    % leave out subject from matrices and behavior
    
    train_mats = all_mats;
    train_mats(leftout,:) = [];
    
    train_behav = all_behav;
    train_behav(leftout) = [];
    
    % correlate all edges with behavior

    [r_mat,p_mat] = corr(train_mats,train_behav);
    r_mat(isnan(r_mat))= 0;
    p_mat(isnan(p_mat))= 0;
    
    % set threshold and define masks
    
    pos_mask = zeros(size(all_mats,2),1);
    neg_mask = zeros(size(all_mats,2),1);
   
    
    pos_edges = find(r_mat > 0 & p_mat < thresh);
    neg_edges = find(r_mat < 0 & p_mat < thresh);
    
    pos_mask(pos_edges) = 1;
    neg_mask(neg_edges) = 1;
    
    
    mask_pos_final(:,leftout) =pos_mask;
    mask_neg_final(:,leftout) =neg_mask;
    mask_both_final(:,leftout) =neg_mask+pos_mask;
    
    % get sum of all edges in TRAIN subs (divide by 2 to control for the
    % fact that matrices are symmetric)
    
    train_sumpos = zeros(no_sub-1,1);
    train_sumneg = zeros(no_sub-1,1);
    
    for ss = 1:size(train_sumpos,1)
        prect_data = train_mats(ss,:);
        train_sumpos(ss) = sum((prect_data((pos_mask==1))))/2;
        train_sumneg(ss) = sum((prect_data((neg_mask==1))))/2;
    end
    
    
    % build model on TRAIN subs
    fit_pos = polyfit(train_sumpos, train_behav,1);
    fit_neg = polyfit(train_sumneg, train_behav,1);
    
    fit_both = polyfit(train_sumpos-train_sumneg, train_behav,1);
    % run model on TEST sub

    test_mat = all_mats(leftout,:);
    test_sumpos = sum((test_mat((pos_mask==1))))/2;
    test_sumneg = sum((test_mat((neg_mask==1))))/2;
    
    behav_pred_pos(leftout) = fit_pos(1)*test_sumpos + fit_pos(2);
    behav_pred_neg(leftout) = fit_neg(1)*test_sumneg + fit_neg(2);
    behav_pred_both(leftout) = fit_both(1)*(test_sumpos-test_sumneg) + fit_both(2);
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
catch
    
end


% end


