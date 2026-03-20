

function [r,p,result] = cpm_pfactor_corr(subj,subjects,matrix,phenos,p_matrix_pos,p_matrix_neg)



% internal mean

subject_all = subjects{1};

for i=1:4
    
   [subject_all a b] = intersect(subject_all,subjects{i}); 
end


for i=1:4
    
   [subject_all a b] = intersect(subject_all,subjects{i}); 
   pheno_single = phenos{i};
   phenos_all(:,i) = pheno_single(b);
   
end

inter_mean = mean(phenos_all,2);


% mean matrix
p_matrix_pos = reshape(p_matrix_pos,[],1);
p_matrix_neg = reshape(p_matrix_neg,[],1);

pos_net = sum(matrix(:,p_matrix_pos>0),2);
neg_net = sum(matrix(:,p_matrix_neg>0),2);

[all a b] = intersect(subject_all,subj);

[r p] = corr(inter_mean(a),pos_net(b)-neg_net(b));


result.brain = pos_net(b)-neg_net(b);
result.beha = inter_mean(a);
result.sub = all;

end