
function [CPM_Result] = xic_CPM_both_ten_noizy(all_mats,all_behav,thresh)



nan_mask = all_mats(:,:,1);
nan_mask = reshape(tril(nan_mask,-1),[],1);

size1 = length(nan_mask);

no_sub = size(all_mats,3);


nfold =10;

all_mats = reshape(all_mats,[],size(all_mats,3))';
all_mats(:,nan_mask==0)=[];

size2 = size(all_mats,2);

% noizy
std_mats = std(all_mats);
std_mats_rep = repmat(std_mats,size(all_mats,1),1);
std_mats_rep = std_mats_rep/15;

all_mats_random = zscore(rand(size(all_mats))).*std_mats_rep;

all_mats = all_mats+all_mats_random;

% ---------------------------------------
   tic
parfor k = 1:1000
 
    tic
    Indices = crossvalind('Kfold',no_sub,nfold);
     
for leftout = 1:nfold
    
   
%     fprintf('\n Leaving out subject # %6.3f',leftout);
    disp(['Ten folder subject Times #',num2str(leftout),' Repeat time # ',num2str(k)])
    % leave out subject from matrices and behavior
    
    train_mats = all_mats;
    train_mats(Indices==leftout,:) = [];
    
    train_behav = all_behav;
    train_behav(Indices==leftout,:) = [];
    
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

    test_mat = all_mats(Indices==leftout,:);
    test_sumpos = sum(test_mat(:,pos_mask==1),2)/2;
    test_sumneg = sum(test_mat(:,neg_mask==1),2)/2;
    
    behav_pred_pos{k,leftout} = fit_pos(1)*test_sumpos + fit_pos(2);
    behav_pred_neg{k,leftout} = fit_neg(1)*test_sumneg + fit_neg(2);
    behav_pred_both{k,leftout} = fit_both(1)*(test_sumpos-test_sumneg)  + fit_both(2); 
    
    mask_pos_all{k,leftout} = find(pos_mask==1); mask_pos_r{k,leftout}=r_mat(pos_mask==1);
    mask_neg_all{k,leftout} = find(neg_mask==1); mask_neg_r{k,leftout}=r_mat(neg_mask==1);
    mask_all_all{k,leftout} = find((pos_mask+neg_mask)==1);mask_both_r{k,leftout}=r_mat((neg_mask+pos_mask)==1);
    
    indictnumber{k,leftout} = find(Indices==leftout);
    
end

   toc
 
end
toc

% predict
[CPM_Result.pos_r,CPM_Result.pos_p] = corr_input(behav_pred_pos,indictnumber,all_behav);
[CPM_Result.neg_r,CPM_Result.neg_p] = corr_input(behav_pred_neg,indictnumber,all_behav);
[CPM_Result.both_r,CPM_Result.both_p] = corr_input(behav_pred_both,indictnumber,all_behav);


% mask
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



function [r,p] =   corr_input(behav_pred_pos,indictnumber,all_behav)

parfor j = 1:1000
    subject = behav_pred_pos(j,:); 
    subject_in = vertcat(subject{:});
    
    index_k = indictnumber(j,:);
    index = vertcat(index_k{:});
    
    predict = all_behav(index);
    
    [r(j),p(j)] = corr(subject_in,predict);
   
    % mask
  
end

end


function pos_mask_final = mask_input(mask_pos_all,size2,size1,nan_mask)

  pos_mask = vertcat(mask_pos_all{:});
  pos_mask = tabulate(pos_mask);
  pos_mask(pos_mask(:,2)==0,:)=[];
  
  pos_mask_index = pos_mask(:,1);
  pos_mask_edge = pos_mask(:,2)/(1000*10);
  
  mask  = zeros(1,size2);
  mask(pos_mask_index) = pos_mask_edge;
  
  mask_pos_all = zeros(1,size1);
  mask_pos_all(nan_mask~=0) = mask;
  
  mask_pos_all = reshape(mask_pos_all,sqrt(size1),sqrt(size1));
  
  mask_final = mask_pos_all;
  mask_final_b = rot90(rot90(rot90(flipud(mask_final))));
  
  pos_mask_final = mask_final+mask_final_b;
    
end



function pos_mask_final = weight_input(mask_both_r,mask_all_all,size2,size1,nan_mask)

 mask_all  = zeros(1,size1);
 mask_all_to  = zeros(1,size1);
 
 mask_nan  = zeros(1,size2);
  for j = 1:1000
      disp(j)
      for i=1:10
          
        mask = cell2mat(mask_all_all(j,i));        
        r = cell2mat(mask_both_r(j,i));     
     
        mask_nan(mask) = r;
        mask_all(nan_mask~=0) = mask_nan;
        
        mask_all_to = mask_all+ mask_all_to;
          
      end
  end
  pos_mask = mask_all_to/10000; 
  pos_mask = reshape(pos_mask,sqrt(size1),sqrt(size1));
  
  mask_final_b = rot90(rot90(rot90(flipud(pos_mask))));
  
  pos_mask_final = pos_mask+mask_final_b;
end
