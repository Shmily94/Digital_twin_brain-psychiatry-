

function [r,p,result] = cpm_trans_corr(matrix,int_pos_keep,int_neg_keep,int_pos_keep1,int_neg_keep1)


% mean matrix
p_matrix_pos = reshape(int_pos_keep,[],1);
p_matrix_neg = reshape(int_neg_keep,[],1);

p_matrix_pos1 = reshape(int_pos_keep1,[],1);
p_matrix_neg1 = reshape(int_neg_keep1,[],1);



pos_net = sum(matrix(:,p_matrix_pos>0),2);
neg_net = sum(matrix(:,p_matrix_neg>0),2);

pos_net1 = sum(matrix(:,p_matrix_pos1>0),2);
neg_net1 = sum(matrix(:,p_matrix_neg1>0),2);


[r,p] = corr(pos_net-neg_net,pos_net1-neg_net1);

result.brain1 = pos_net-neg_net;
result.brain2 = pos_net1-neg_net1;



end