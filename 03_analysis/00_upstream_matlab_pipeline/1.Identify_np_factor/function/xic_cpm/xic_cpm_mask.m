
function  [mask_cpm] = xic_CPM_mask(all_mats,CPM_Result)

if size(all_mats,3)>100
all_mats = reshape(all_mats,[],size(all_mats,3));
all_mats= all_mats';
end


    all_mats_nan_mask = all_mats(1,:);
    all_mats(:,isnan(all_mats_nan_mask))=[];

    all_mats_nan = all_mats(:,1);
    all_mats(isnan(all_mats_nan),:)=[];


    
    % ----------------------
  
    size2 = sqrt(length(all_mats_nan_mask));
    mask = find((isnan(all_mats_nan_mask))==0);
    
    mask_all = zeros(length(all_mats_nan_mask),size(CPM_Result.mask_pos,2));

    mask_pos = mask_all;
    mask_pos(mask',:) = CPM_Result.mask_pos;
    
    mask_pos_pro = sum(mask_pos,2)/size(all_mats,1);
    mask_pos_pro(mask_pos_pro<0.95) = 0;
    mask_pos_pro = round(reshape(mask_pos_pro,size2,size2));


%     mask_neg = mask_all;
%     mask_neg(mask',:) = CPM_Result.mask_neg;
%     mask_neg_pro = sum(mask_neg,2)/size(all_mats,1);
%     mask_neg_pro(mask_neg_pro<0.95) = 0;
%     mask_neg_pro = round(reshape(mask_neg_pro,size2,size2));

    mask_both = mask_all;
    mask_both(mask',:) = CPM_Result.mask_both;
    mask_both_pro = sum(mask_both,2)/size(all_mats,1);
    mask_both_pro(mask_both_pro<0.95) = 0;
    mask_both_pro = round(reshape(mask_both_pro,size2,size2));
    
%     neg_degree = sum((mask_neg_pro));
    pos_degree = sum((mask_pos_pro));
    both_degree = sum((mask_both_pro));
    
%     mask_cpm.neg_matrix = mask_neg_pro;
%     mask_cpm.neg_degree = neg_degree;
%     
    mask_cpm.pos_matrix = mask_pos_pro;
    mask_cpm.pos_degree = pos_degree;
    
    mask_cpm.both_matrix = mask_both_pro;
    mask_cpm.both_degree = both_degree;  
end