
function [CPM_Result] = xic_CPM_both_ten2(all_mats,all_behav,thresh)
% [CPM_Result] = xic_CPM_both_ten2(data3_ph,phenotype3,threshs);

if size(all_behav,2)>1
   all_behav = all_behav'; 
    
end

nan_mask = all_mats(:,:,1);
nan_mask = reshape(tril(nan_mask,-1),[],1);

size1 = length(nan_mask);



% nfold =50;

if size(all_mats,3)>1
all_mats = reshape(all_mats,[],size(all_mats,3))';
all_mats(:,nan_mask==0)=[];
end

size2 = size(all_mats,2);
no_sub = size(all_mats,1);

repeat = 1000;

% ---------------------------------------
   tic
for k = 1:repeat
 
    tic
    % Indices = crossvalind('Kfold',no_sub,nfold);
training_ratio = 0.65;
validation_ratio = 1 - training_ratio;
num_training_samples = round(training_ratio*no_sub);
num_validation_samples = no_sub - num_training_samples;
indices = randperm(no_sub);
training_indices = indices(1:num_training_samples);
validation_indices = indices(num_training_samples + 1:end);
     
% parfor leftout = 1:nfold
    
   leftout=1;
%     fprintf('\n Leaving out subject # %6.3f',leftout);
    disp(['Ten folder subject Times #',num2str(leftout),' Repeat time # ',num2str(k)])
    % leave out subject from matrices and behavior
    
    % train_mats = all_mats;
    % train_mats(Indices==leftout,:) = [];
    train_mats = all_mats(training_indices,:);
    
    % train_behav = all_behav;
    % train_behav(Indices==leftout,:) = [];
    train_behav=all_behav(training_indices,:);
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

    % test_mat = all_mats(Indices==leftout,:);
    test_mat = all_mats(validation_indices,:);
    test_sumpos = sum(test_mat(:,pos_mask==1),2)/2;
    test_sumneg = sum(test_mat(:,neg_mask==1),2)/2;  
    
    behav_pred_pos{k,leftout} = fit_pos(1)*test_sumpos + fit_pos(2);
    behav_pred_neg{k,leftout} = fit_neg(1)*test_sumneg + fit_neg(2);
    behav_pred_both{k,leftout} = fit_both(1)*(test_sumpos-test_sumneg)  + fit_both(2); 
    
  
%     % rcca
%     
%     [fit_coef, fit_info] = lasso(train_mats(:,pos_mask==1), train_behav, 'Alpha',0.0001, 'CV', 10);
%      idxLambda1SE = fit_info.Index1SE;
%      coef = fit_coef(:,idxLambda1SE);
%      coef0 = fit_info.Intercept(idxLambda1SE);
%      lambda_total(leftout) = fit_info.Lambda(idxLambda1SE);
%      
    
    
    mask_pos_all{k,leftout} = find(pos_mask==1); mask_pos_r{k,leftout}=r_mat(pos_mask==1);
    mask_neg_all{k,leftout} = find(neg_mask==1); mask_neg_r{k,leftout}=r_mat(neg_mask==1);
    mask_all_all{k,leftout} = find((pos_mask+neg_mask)==1);mask_both_r{k,leftout}=r_mat((neg_mask+pos_mask)==1);
    
    indictnumber{k,leftout} = validation_indices;
    
% end

   toc
 
end
toc

CPM_Result.mask_pos_all=mask_pos_all;
CPM_Result.mask_neg_all=mask_neg_all;
CPM_Result.mask_all_all=mask_all_all;

% predict
[CPM_Result.pos_r,CPM_Result.pos_p] = corr_input2(behav_pred_pos,indictnumber,all_behav);
[CPM_Result.neg_r,CPM_Result.neg_p] = corr_input2(behav_pred_neg,indictnumber,all_behav);
[CPM_Result.both_r,CPM_Result.both_p] = corr_input2(behav_pred_both,indictnumber,all_behav);

% CPM_Result.test = all_behav;

CPM_Result.pos_r_mean = mean(CPM_Result.pos_r);
CPM_Result.neg_r_mean = mean(CPM_Result.neg_r);
CPM_Result.both_r_mean = mean(CPM_Result.both_r);

% mask
CPM_Result.mask_pos_all=mask_pos_all;
CPM_Result.mask_neg_all=mask_neg_all;
CPM_Result.mask_all_all=mask_all_all;

if sum(vertcat(mask_pos_all{:}))>1;CPM_Result.pos_mask = mask_input(mask_pos_all,size2,size1,nan_mask);
end

if sum(vertcat(mask_neg_all{:}))>1;CPM_Result.neg_mask = mask_input(mask_neg_all,size2,size1,nan_mask);
end

if sum(vertcat(mask_all_all{:}))>1;CPM_Result.all_mask = mask_input(mask_all_all,size2,size1,nan_mask);
end

% r
if isnan(sum(vertcat(mask_pos_r{:})))~=1;CPM_Result.pos_weight_r = weight_input(mask_pos_r,mask_pos_all,size2,size1,nan_mask);
end

if isnan(sum(vertcat(mask_neg_r{:})))~=1;CPM_Result.neg_weight_r = weight_input(mask_neg_r,mask_neg_all,size2,size1,nan_mask);
end

if isnan(sum(vertcat(mask_both_r{:})))~=1;CPM_Result.all_weight_r = weight_input(mask_both_r,mask_all_all,size2,size1,nan_mask);
end


toc
end


