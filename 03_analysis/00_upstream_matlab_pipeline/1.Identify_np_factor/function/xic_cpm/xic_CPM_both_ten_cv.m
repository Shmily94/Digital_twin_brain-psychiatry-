
function [CPM_Result] = xic_CPM_both_ten_cv(all_mats,all_behav,thresh,phenotype_subject)



nan_mask = all_mats(:,:,1);
nan_mask = reshape(tril(nan_mask,-1),[],1);

size1 = length(nan_mask);

no_sub = size(all_mats,3);


nfold =10;

all_mats = reshape(all_mats,[],size(all_mats,3))';
all_mats(:,nan_mask==0)=[];

size2 = size(all_mats,2);

repeat =1000;

% ---------------------------------------
   tic
   
parfor k = 1:length(all_behav)
 
    tic
    
%     [train_behav,test_behav,train_mats,test_mat] = xic_cpm_site_cv(all_mats,all_behav,phenotype_subject)


%     fprintf('\n Leaving out subject # %6.3f',k);
    disp(['Ten folder subject Times #',' Repeat time # ',num2str(k)])
    % leave out subject from matrices and behavior
    
    train_mats = all_mats;
    train_mats(k,:) = [];
    
    train_behav = all_behav;
    train_behav(k,:) = [];
    
    test_mat = all_mats(k,:);
   
    % correlate all edges with behavior

    [r_mat,p_mat] = corr(train_mats,train_behav);
    r_mat(isnan(r_mat))= 0;
    p_mat(isnan(p_mat))= 0;
    
    % set threshold and define masks
    
    pos_mask = zeros(size(all_mats,2),1);
    neg_mask = zeros(size(all_mats,2),1);
   
    
    
    pos_mask((r_mat > 0 & p_mat < thresh)) = 1;
    
    if sum((r_mat < 0 & p_mat < thresh))>0
    neg_mask((r_mat < 0 & p_mat < thresh)) = 1;    
    else
    neg_mask(1)=1;    
    end
    
    train_sumpos = sum((train_mats(:,pos_mask==1)),2)/2;
    train_sumneg = sum((train_mats(:,neg_mask==1)),2)/2;
    
    
    % build model on TRAIN subs
    fit_pos = polyfit(train_sumpos, train_behav,1);
    fit_neg = polyfit(train_sumneg, train_behav,1);
    
    fit_both = polyfit(train_sumpos-train_sumneg, train_behav,1);
    
    % run model on TEST sub

    
    test_sumpos = sum(test_mat(:,pos_mask==1),2)/2;
    test_sumneg = sum(test_mat(:,neg_mask==1),2)/2;
    
    behav_pred_pos(k,1) = fit_pos(1)*test_sumpos + fit_pos(2);
    behav_pred_neg(k,1) = fit_neg(1)*test_sumneg + fit_neg(2);
    behav_pred_both(k,1) = fit_both(1)*(test_sumpos-test_sumneg)  + fit_both(2); 
    
   
    

   toc
 
end

k=1;
    [r_pos(k), p_pos(k)] = corr(behav_pred_pos,all_behav);
    [r_neg(k) ,p_neg(k)] = corr(behav_pred_neg,all_behav);
    [r_both(k),p_both(k)] = corr(behav_pred_both,all_behav);
   

CPM_Result.r_pos = r_pos;  
CPM_Result.p_pos= p_pos;
CPM_Result.r_neg = r_neg;
CPM_Result.p_neg = p_neg;

CPM_Result.r_both = r_both;
CPM_Result.p_both = p_both;

toc


end


