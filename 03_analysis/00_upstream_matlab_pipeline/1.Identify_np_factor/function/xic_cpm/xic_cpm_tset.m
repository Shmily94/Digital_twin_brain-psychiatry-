

function xic_cpm_tset(data_subs,phenotype_subjects,data,phenotypes,phenotype_names,threshs,task_names)

[a, b_data, b_phno] = intersect(data_subs,phenotype_subjects);
       
 data3_ph = data(:,:,b_data);
 phenotype3 = phenotypes(b_phno);
 
[CPM_Result] = xic_CPM_both_ten(data3_ph,phenotype3,threshs);
CPM_Result.subject = a;

out_name = [phenotype_names,'_CPM',task_names,'.mat'];
save(out_name,'CPM_Result');
    
end