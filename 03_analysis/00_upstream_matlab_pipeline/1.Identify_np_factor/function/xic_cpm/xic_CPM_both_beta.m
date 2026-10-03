
function [CPM_Result,CPM_mask] = xic_CPM_both_beta(all_mats,all_behav,thresh)


if size(all_mats,3)>100
all_mats = reshape(all_mats,[],size(all_mats,3));
all_mats= all_mats';
end


all_mats_nan_mask = all_mats(1,:);
all_mats(:,isnan(all_mats_nan_mask))=[];

all_mats_nan = all_mats(:,2);
all_mats(isnan(all_mats_nan),:)=[];
all_behav(isnan(all_mats_nan),:)=[];



size1 = size(all_mats,1);

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
    tic
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
   
%     
%     pos_edges = find(r_mat > 0 & p_mat < thresh);
%     neg_edges = find(r_mat < 0 & p_mat < thresh);
    
    pos_mask(r_mat > 0 & p_mat < thresh) = 1;
    neg_mask(r_mat < 0 & p_mat < thresh) = 1;
       
 
    mask_pos_final(:,leftout) =pos_mask;
    mask_neg_final(:,leftout) =neg_mask;
    mask_both_final(:,leftout) =neg_mask+pos_mask;
    
    % get sum of all edges in TRAIN subs (divide by 2 to control for the
    % fact that matrices are symmetric)
    
%     train_sumpos = zeros(no_sub-1,1);
%     train_sumneg = zeros(no_sub-1,1);
%     
%     for ss = 1:size(train_sumpos,1)
%         prect_data = train_mats(ss,:);
%         train_sumpos(ss) = sum((prect_data((pos_mask==1))))/2;
%         train_sumneg(ss) = sum((prect_data((neg_mask==1))))/2;
%     end

% beta

    mat_sum_pos = train_mats(:,pos_mask==1); pos_weight = repmat(r_mat(pos_mask==1)',size(train_mats,1),1);
    mat_sum_neg = train_mats(:,neg_mask==1); neg_weight = repmat(r_mat(neg_mask==1)',size(train_mats,1),1); 
     
    train_sumpos = sum(mat_sum_pos.*pos_weight,2)/2;    
    train_sumneg =  sum(mat_sum_neg.*neg_weight,2)/2;
    
    
    % build model on TRAIN subs
    fit_pos = polyfit(train_sumpos, train_behav,1);
    fit_neg = polyfit(train_sumneg, train_behav,1);
    
    fit_both = polyfit(train_sumpos+train_sumneg, train_behav,1);
    fit_both_m = regress(train_behav,[train_sumpos,train_sumneg]);
    % run model on TEST sub

    test_mat = all_mats(leftout,:);

% beta
    test_pos = test_mat(pos_mask==1); pos_weight_test = repmat(r_mat(pos_mask==1)',1,1);
    test_neg = test_mat(neg_mask==1); neg_weight_test = repmat(r_mat(neg_mask==1)',1,1);
    
    test_sumpos = sum(test_pos.*pos_weight_test,2)/2;
    test_sumneg = sum(test_neg.*neg_weight_test,2)/2;
    
    
    behav_pred_pos(leftout) = fit_pos(1)*test_sumpos + fit_pos(2);
    behav_pred_neg(leftout) = fit_neg(1)*test_sumneg + fit_neg(2);
    behav_pred_both(leftout) = fit_both(1)*(test_sumpos-test_sumneg) + fit_both(2);
    behav_pred_both_mul(leftout) = fit_both_m(1)*(test_sumpos) + fit_both_m(2)*(test_sumneg);
    toc
end

catch
    
end

try
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


mask_pos = mask_pos_final;


CPM_Result.R_neg = R_neg;
CPM_Result.P_neg = P_neg;
CPM_Result.neg_predict = behav_pred_neg;
CPM_Result.neg_test = test2;
CPM_Result.mask_neg = mask_neg_final;

CPM_Result.R_both = R_both;
CPM_Result.P_both = P_both;
CPM_Result.both_predict = behav_pred_both;
CPM_Result.both_test = test3;

mask_both = mask_both_final;

end
% 
% figure(1); plot(test,behav_pred_pos,'r.'); lsline;title([num2str(P_pos),'|',num2str(R_pos)])
% figure(2); plot(test2,behav_pred_neg,'b.'); lsline;title([num2str(P_neg),'|',num2str(R_neg)])
% figure(3); plot(test3,behav_pred_both,'m.'); lsline;title([num2str(P_both),'|',num2str(R_both)])

[CPM_mask] = xic_CPM_mask(mask_pos,mask_both,all_mats_nan_mask,size1);


end


function  [mask_cpm] = xic_CPM_mask(mask_pos,mask_both,all_mats_nan_mask,size1)



    
    % ----------------------
  
    size2 = sqrt(length(all_mats_nan_mask));
    mask = find((isnan(all_mats_nan_mask))==0);
    
    mask_all = zeros(length(all_mats_nan_mask),size(mask_pos,2));

    mask_pos_se = mask_all;
    mask_pos_se(mask',:) = mask_pos;
    
    mask_pos_pro = sum(mask_pos_se,2)/size1;
    mask_pos_pro(mask_pos_pro<0.95) = 0;
    mask_pos_pro = round(reshape(mask_pos_pro,size2,size2));


    mask_neg = mask_all;
    mask_neg(mask',:) = CPM_Result.mask_neg;
    mask_neg_pro = sum(mask_neg,2)/size(all_mats,1);
    mask_neg_pro(mask_neg_pro<0.95) = 0;
    mask_neg_pro = round(reshape(mask_neg_pro,size2,size2));

    mask_both_se = mask_all;
    mask_both_se(mask',:) = mask_both;
    mask_both_pro = sum(mask_both_se,2)/size1;
    mask_both_pro(mask_both_pro<0.95) = 0;
    mask_both_pro = round(reshape(mask_both_pro,size2,size2));
    
    neg_degree = sum((mask_neg_pro));
    pos_degree = sum((mask_pos_pro));
    both_degree = sum((mask_both_pro));
    
    mask_cpm.neg_matrix = mask_neg_pro;
    mask_cpm.neg_degree = neg_degree;
%     
    mask_cpm.pos_matrix = mask_pos_pro;
    mask_cpm.pos_degree = pos_degree;
    
    mask_cpm.both_matrix = mask_both_pro;
    mask_cpm.both_degree = both_degree;  
end
