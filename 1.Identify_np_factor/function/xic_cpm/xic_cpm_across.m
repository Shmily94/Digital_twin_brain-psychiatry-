

function [predict_all,test_all,subject,R_all_max] = xic_cpm_across(names)

files = dir([names,'*']);  
    
load(files(1).name);
all = CPM_Result.subject;

for i = 1:length(files)
    load(files(i).name)
    
all = intersect(CPM_Result.subject,all);

end


for i = 1:length(files)
  disp(i)
    
 load(files(i).name)
   
[all b]= intersect(CPM_Result.subject,all);

[predict_pos(:,i)] = mean(CPM_Result.pos_predit(b),2);
[predict_neg(:,i)] = mean(CPM_Result.neg_predit(b),2);
[predict_both(:,i)] = mean(CPM_Result.both_predit(b),2);
[predict_test] = mean(CPM_Result.test(b),2);

[predict_all] = cat(3,predict_pos,predict_neg,predict_both);

 R_pos(i)= mean(CPM_Result.pos_r);
 R_neg(i)= mean(CPM_Result.neg_r);
 R_both(i)= mean(CPM_Result.both_r);
 
 P_pos(i)= mean(CPM_Result.pos_p);
 P_neg(i)= mean(CPM_Result.neg_p);
 P_both(i)= mean(CPM_Result.both_p);
end


R_all = [R_pos;R_neg;R_both];

for j = 1:size(R_all,2)
    [a number(j)] = max(R_all(:,j));
    R_all_max(j) = a;
end


eft_all = [predict_all(:,1,number(1)),predict_all(:,2,number(2))];

mid_all = [predict_all(:,3,number(3)),predict_all(:,4,number(4)),predict_all(:,5,number(5))];

sst_all = [predict_all(:,6,number(6)),predict_all(:,7,number(7)),predict_all(:,8,number(8))];

test_all = predict_test;

predict_all = [eft_all,mid_all,sst_all];

subject = all;
