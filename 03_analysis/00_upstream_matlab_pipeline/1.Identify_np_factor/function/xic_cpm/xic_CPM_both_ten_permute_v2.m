
function [CPM_Result] = xic_CPM_both_ten_permute_v2(all_mats,all_behav,thresh)



if size(all_behav,2)>1 ;all_behav = all_behav';end

nan_mask = all_mats(:,:,1);
nan_mask = reshape(tril(nan_mask,-1),[],1);

size1 = length(nan_mask);

nfold =50;

if size(all_mats,3)>1
all_mats = reshape(all_mats,[],size(all_mats,3))';
all_mats(:,nan_mask==0)=[];

end

size2 = size(all_mats,2);
no_sub = size(all_mats,1);

repeat = 2;

% ---------------------------------------
   tic
for k = 1:repeat
 
    tic
    Indices = crossvalind('Kfold',no_sub,nfold);
     
parfor leftout = 1:nfold
    
   
%     fprintf('\n Leaving out subject # %6.3f',leftout);
    disp(['Ten folder subject Times #',num2str(leftout),' Repeat time # ',num2str(k)])
   
    train_mats = all_mats;
    train_mats(Indices==leftout,:) = [];
    
    train_behav = all_behav;
    train_behav(Indices==leftout,:) = [];
    
    [r_mat,p_mat] = corr(train_mats,train_behav);
    r_mat(isnan(r_mat))= 0;
    p_mat(isnan(p_mat))= 0;
    
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
    
    
    fit_pos = polyfit(train_sumpos, train_behav,1);
    fit_neg = polyfit(train_sumneg, train_behav,1);
    
    fit_both = polyfit(train_sumpos-train_sumneg, train_behav,1);
  
    test_mat = all_mats(Indices==leftout,:);
    test_sumpos = sum(test_mat(:,pos_mask==1),2)/2;
    test_sumneg = sum(test_mat(:,neg_mask==1),2)/2;
    
    behav_pred_pos{k,leftout} = fit_pos(1)*test_sumpos + fit_pos(2);
    behav_pred_neg{k,leftout} = fit_neg(1)*test_sumneg + fit_neg(2);
    behav_pred_both{k,leftout} = fit_both(1)*(test_sumpos-test_sumneg)  + fit_both(2); 
      
    
    mask_pos_all{k,leftout} = find(pos_mask==1)'; 
    mask_neg_all{k,leftout} = find(neg_mask==1)'; 
    mask_all_all{k,leftout} = find((pos_mask+neg_mask)==1)';
    
    indictnumber{k,leftout} = find(Indices==leftout);
    
end

   toc
 
end
toc

% predict
[CPM_Result.pos_r,CPM_Result.pos_p,CPM_Result.pos_predit,CPM_Result.pos_qs]     = corr_input(behav_pred_pos,indictnumber,all_behav);
[CPM_Result.neg_r,CPM_Result.neg_p,CPM_Result.neg_predit,CPM_Result.neg_qs]     = corr_input(behav_pred_neg,indictnumber,all_behav);
[CPM_Result.both_r,CPM_Result.both_p,CPM_Result.both_predit,CPM_Result.both_qs] = corr_input(behav_pred_both,indictnumber,all_behav);

CPM_Result.test = all_behav;

CPM_Result.pos_r_mean  = mean(CPM_Result.pos_r);
CPM_Result.neg_r_mean  = mean(CPM_Result.neg_r);
CPM_Result.both_r_mean = mean(CPM_Result.both_r);

% mask
if sum(vertcat(mask_pos_all{:}))>1;CPM_Result.pos_mask = mask_input(mask_pos_all,size2,size1,nan_mask);
end

if sum(vertcat(mask_neg_all{:}))>1;CPM_Result.neg_mask = mask_input(mask_neg_all,size2,size1,nan_mask);
end

if sum(vertcat(mask_all_all{:}))>1;CPM_Result.all_mask = mask_input(mask_all_all,size2,size1,nan_mask);
end


    mask_pos = [cell2mat(mask_pos_all(1,:)),cell2mat(mask_pos_all(2,:))];
    mask_pos_unique = unique(mask_pos);
    [pos_conut] = histc(mask_pos,mask_pos_unique);
    mask_pos_t = mask_pos_unique(pos_conut>95);
    mask_pos_fc = sum(all_mats(:,mask_pos_t),2);

    mask_neg = [cell2mat(mask_neg_all(1,:)),cell2mat(mask_neg_all(2,:))];
    mask_neg_unique = unique(mask_neg);
    [neg_conut] = histc(mask_neg,mask_neg_unique);
    mask_neg_t = mask_pos_unique(neg_conut>95);
    mask_neg_fc = sum(all_mats(:,mask_neg_t),2);
    
CPM_Result.FC_pos_R = corr(mask_pos_fc,CPM_Result.test);
CPM_Result.FC_neg_R = corr(mask_neg_fc,CPM_Result.test);
CPM_Result.FC_both_R = corr(mask_neg_fc+mask_pos_fc,CPM_Result.test);

toc
end

