
function xic_CPM_Auto_match_two(data1,data2,data_sub1,data_sub2, ...
        phenotype,phenotype_name,phenotype_subject,thresh,task_name)

    
 %% data1 
[a,b_data,b_phno] = intersect(data_sub1,phenotype_subject);
 
 data1  = data1(:,:,b_data);
 phenotype1 = phenotype(b_phno);
 
[CPM_Result,]  = xic_CPM_both_ten(data1,phenotype1,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM',task_name{1},'.mat'];
save(out_name,'CPM_Result','CPM_mask');
 
 %% data2 
[a ,b_data, b_phno] = intersect(data_sub2,phenotype_subject);
 
 data2  = data2(:,:,b_data);
 phenotype2 = phenotype(b_phno);
 
[CPM_Result,CPM_mask]  = xic_CPM_both_ten(data2,phenotype2,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM',task_name{2},'.mat'];
save(out_name,'CPM_Result','CPM_mask'); 


    
end
