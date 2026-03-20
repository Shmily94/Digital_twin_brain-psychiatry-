function [train_sumpos,pos_mask,train_sumneg,neg_mask,train_all,mask_all] = CPM_train(train_mats,train_behav,thresh)

    [r_mat,p_mat] = corr(train_mats,train_behav);
    r_mat(isnan(r_mat))= 0;
    p_mat(isnan(p_mat))= 0;
    
    % set threshold and define masks
    
    pos_mask = zeros(size(all_mats,2),1);
    neg_mask = zeros(size(all_mats,2),1);
 
    pos_mask((r_mat > 0 & p_mat < thresh)) = 1;
    neg_mask((r_mat < 0 & p_mat < thresh)) = 1;
    mask_all = pos_mask+neg_mask;
    % get sum of all edges in TRAIN subs (divide by 2 to control for the
    % fact that matrices are symmetric)
    
    train_sumpos = zeros(no_sub-1,1);
    train_sumneg = zeros(no_sub-1,1);
    
    for ss = 1:size(train_sumpos)
        prect_data = train_mats(ss,:);
        train_sumpos(ss) = sum(prect_data((pos_mask==1)))/2;
        train_sumneg(ss) = sum(prect_data((neg_mask==1)))/2;
    end

    train_all = train_sumpos-train_sumneg;
end