

function [r,p,predit,q_s] =   corr_input(behav_pred_pos,indictnumber,all_behav)


parfor j = 1:size(behav_pred_pos,1)
    subject = behav_pred_pos(j,:); 
    subject_in = vertcat(subject{:});
    
    index_k = indictnumber(j,:);
    index = vertcat(index_k{:});
    
    [a b] = sort(index);
        
    [r(j),p(j)] = corr(subject_in(b),all_behav);
    
    
     mse = sum((subject_in(b) - all_behav).^2) / length(all_behav);
     q_s(j) = 1 - mse / var(all_behav, 1);
    
    [predit(:,j)] = subject_in(b);
 
  
end

end
