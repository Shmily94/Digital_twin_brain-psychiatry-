
function xic_CPM_Auto_tenvali_three(data1,data2,data3,data_sub1,data_sub2,data_sub3, ...
        phenotype,phenotype_name,phenotype_subject,thresh,task_name)

        
    
 %% data1 
xic_cpm_tset(data_sub1,phenotype_subject,data1,phenotype,phenotype_name,thresh,task_name{1})
 
 %% data2 

 xic_cpm_tset(data_sub2,phenotype_subject,data2,phenotype,phenotype_name,thresh,task_name{2})
 %% data3 
 
 xic_cpm_tset(data_sub3,phenotype_subject,data3,phenotype,phenotype_name,thresh,task_name{3})

end

function xic_cpm_tset(data_subs,phenotype_subjects,data,phenotypes,phenotype_names,threshs,task_names)

[a, b_data, b_phno] = intersect(data_subs,phenotype_subjects);
       
 data3_ph = data(:,:,b_data);
 phenotype3 = phenotypes(b_phno);
 
[CPM_Result] = xic_CPM_both_ten(data3_ph,phenotype3,threshs);
CPM_Result.subject = a;

out_name = [phenotype_names,'_CPM',task_names,'.mat'];
save(out_name,'CPM_Result');
    
end

