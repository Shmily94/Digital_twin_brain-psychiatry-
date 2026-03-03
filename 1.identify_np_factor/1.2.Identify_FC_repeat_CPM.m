% examine the cross validation and independent validation results

task_names={'_SST_stopfai','_SST_stopsuc','_MID_antici_hit','_MID_feed_hit'};
phenotype_names=FU2_self.FU2_psy_name;
for i=1:4
    for j=1:6
     load(['FU2_0614_',phenotype_names{j},'_CPM',task_names{i},'.mat']);
     load(['FU2_0614_',phenotype_names{j},'_test_results_perm',task_names{i},'.mat']);

     % 把100次resampling的结果也平均，作为独立样本test的r;
     all_idx_perm=zeros(268,268);
     pos_idx_perm=zeros(268,268);
     neg_idx_perm=zeros(268,268);

     for k=1:100
      both_r_mean_perm(k,1)=CPM_Result_perm{1,k}.both_r_mean;
      both_r_test_results(k,1)=test_results{1,k}(1,1);
      both_r_test_results(k,2)=test_results{1,k}(1,2);
      
      all_idx=CPM_Result_perm{1,k}.all_mask;
      all_idx(all_idx<0.95)=0;
      all_idx(all_idx>0)=1;
      all_idx_perm=all_idx+all_idx_perm;

      pos_idx=CPM_Result_perm{1,k}.pos_mask;
      pos_idx(pos_idx<0.95)=0;
      pos_idx(pos_idx>0)=1;
      pos_idx_perm=pos_idx+pos_idx_perm;

      neg_idx=CPM_Result_perm{1,k}.neg_mask;
      neg_idx(neg_idx<0.95)=0;
      neg_idx(neg_idx>0)=1;
      neg_idx_perm=neg_idx+neg_idx_perm;

     end
      mean_both_r_cpm=mean(both_r_mean_perm);
      N=size(CPM_Result_perm{1,k}.subject,1)-size(CPM_Result_perm{1,k}.test,1); df=N-2;
      r=mean(both_r_test_results(:,1));
      pValue = correlationToPValue(r, df)./2;  % 因为相关值必须为正相关，one-tail paired.
      indep_test_results{i,j}=[r,pValue,mean_both_r_cpm];

      if pValue<0.05 %(0.05./4./6)
       indep_test_mask{i,j}=find(all_idx_perm>80);
       indep_test_pos_mask{i,j}=find(pos_idx_perm>80);
       indep_test_neg_mask{i,j}=find(neg_idx_perm>80);
      end

    end
end
save indep_test_results indep_test_results indep_test_mask indep_test_pos_mask indep_test_neg_mask
