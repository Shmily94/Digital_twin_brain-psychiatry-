
function [CPM_Result]=xic_cpm_permute(data_subs,phenotype_subjects,data,phenotypes,phenotype_names,threshs,task_names)


[a, b_data, b_phno] = intersect(data_subs,phenotype_subjects);
       
 data3_ph = data(:,:,b_data);
 phenotype3 = phenotypes(b_phno);
 
 [CPM_Result] = xic_CPM_both_ten_permute(data3_ph,phenotype3,threshs);
 
 CPM_Result.subject = a;
end


