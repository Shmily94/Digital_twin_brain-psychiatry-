 load("/Users/yunman/Desktop/Figures/Figure4/predicted_task_perf_empirical_simulated_fc_matrix.mat");

task_name = {'empirical_MID_antici_hit','empirical_MID_feed_hit','simulated_MID_antici_hit','simulated_MID_feed_hit'}; 
thresh = 0.01;
 
 for i=7:8
 phenotype_name=phenotype_name_all{i};
 task_perf=task_perf_all(:,i);
    xic_cpm_tset(id_task_perf,id_task_perf,empirical_mid_antici_hit_C,...
        task_perf,phenotype_name,thresh,task_name{1})

    xic_cpm_tset(id_task_perf,id_task_perf,empirical_mid_feed_hit_C,...
        task_perf,phenotype_name,thresh,task_name{2})

    xic_cpm_tset(id_task_perf,id_task_perf,simulated_mid_antici_hit_C,...
        task_perf,phenotype_name,thresh,task_name{3})

    xic_cpm_tset(id_task_perf,id_task_perf,simulated_mid_feed_hit_C,...
        task_perf,phenotype_name,thresh,task_name{4})
 end

 %% sort CPM results

 results=dir('*CPM*.mat');

for i=1:length(results)
load(results(i).name);
both_r_mean=CPM_Result.both_r_mean;
predict_perf(i)=both_r_mean;
predict_p_value(i)=mean(CPM_Result.both_p);
end
save predict_perf_simulated_empirical_fc_matrix.mat results predict_perf predict_p_value 


phenotype_name_all{7}='big_win-no_win_rt';
phenotype_name_all{8}='small_win-no_win_rt';
task_perf_all(:,7)=task_perf_all(:,2)-task_perf_all(:,6);
task_perf_all(:,8)=task_perf_all(:,4)-task_perf_all(:,6);