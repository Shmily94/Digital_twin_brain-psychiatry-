function xic_cpm_tset2(data_subs,phenotype_subjects,data,phenotypes,phenotype_names,threshs,task_names)

[a, b_data, b_phno] = intersect(data_subs,phenotype_subjects);
 data3_ph = data(:,:,b_data);
 phenotype3 = phenotypes(b_phno);

parfor r=1:100
% resampling
training_ratio = 0.65;
validation_ratio = 1 - training_ratio;
num_training_samples = round(training_ratio * size(data3_ph,3));
num_validation_samples = size(data3_ph,3) - num_training_samples;
indices = randperm(size(data3_ph,3));
training_indices = indices(1:num_training_samples);
validation_indices = indices(num_training_samples + 1:end);

[CPM_Result] = xic_CPM_both_ten(data3_ph(:,:,training_indices),phenotype3(training_indices,:),threshs);
CPM_Result.subject = a;
% out_name = [phenotype_names,'_CPM',num2str(k),task_names,'.mat'];
% save(out_name,'CPM_Result');
CPM_Result_perm{r}=CPM_Result;

% run model on test sub
% load([phenotype_names,'_CPM',num2str(k),task_names,'.mat']);
test_mat=data3_ph(:,:,validation_indices);
test_beha=phenotype3(validation_indices,:);
[r_pos,p_pos,r_neg,p_neg,r_all,p_all]=test_fcs_beha(test_mat,test_beha,CPM_Result);
test_results{r}=[r_all,p_all;r_pos,p_pos;r_neg,p_neg];

end    
out_name = [phenotype_names,'_CPM',task_names,'.mat'];
save(out_name,'CPM_Result_perm');
save([phenotype_names,'test_results_perm',task_names,'.mat'],'test_results');

end 
