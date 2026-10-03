
function xic_CPM_Auto_match_three(data1,data2,data3,data_sub1,data_sub2,data_sub3, ...
        pynotype,phenotype_name,phenotype_subject,thresh,task_name)

        
    
 %% data1 
[a,b_data,b_phno] = intersect(data_sub1,phenotype_subject);
 
 data1  = data1(:,:,b_data);
 pynotype1 = pynotype(b_phno);
 
[CPM_Result,CPM_mask] = xic_CPM_both(data1,pynotype1,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM',task_name{1},'.mat'];
save(out_name,'CPM_Result','CPM_mask');
 
 %% data2 
[a ,b_data, b_phno] = intersect(data_sub2,phenotype_subject);
 
 data2  = data2(:,:,b_data);
 pynotype2 = pynotype(b_phno);
 
[CPM_Result,CPM_mask] = xic_CPM_both(data2,pynotype2,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM',task_name{2},'.mat'];
save(out_name,'CPM_Result','CPM_mask'); 

 %% data3 
[a, b_data, b_phno] = intersect(data_sub3,phenotype_subject);
 
 data3  = data3(:,:,b_data);
 pynotype3 = pynotype(b_phno);
 
[CPM_Result,CPM_mask] = xic_CPM_both(data3,pynotype3,thresh);
CPM_Result.subject = a;

out_name = [phenotype_name,'_CPM',task_name{3},'.mat'];
save(out_name,'CPM_Result','CPM_mask'); c
    
    
end
