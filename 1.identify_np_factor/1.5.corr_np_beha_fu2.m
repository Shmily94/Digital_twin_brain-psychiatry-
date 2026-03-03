%fu2 healthy brain and behavior associations
clear;clc
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Self_FU2_inter_exter.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2\Case_control\FU2_discard_NP_factor.mat');
for i=1:6
    phenotype_fu2 = FU2_self.FU2_psy_match(:,i);
    phenotype_name = FU2_self.FU2_psy_name{i};
    phenotype_subject = FU2_self.FU2_psy_match_sub;
    brain_subject = FU2_control_id2;
    [all,ph,cova] = intersect(phenotype_subject,brain_subject);
    phenotype_fu2_2 = phenotype_fu2(ph);
    phenotype_fu2_all(:,i)=phenotype_fu2_2;
    brain_data = [NP_factor(cova,1),NP_factor_neg(cova,1)];
end
load('D:\postdoc\Work\Computer-Brain-Project\Code\CPM\IAMGEN_Develop_diagnostic_0814\Cova_subject_jia.mat')
[C_brain_beha,ia,ib] = intersect(all,cova_subject);
C_cova_data=cova_data(ib,:);
C_beha=phenotype_fu2_all(ia,:);
C_brain=brain_data(ia,:);
df = 1048;
for i=1:2
    X=C_brain(:,i);
    for j=1:6
        Y=C_beha(:,j);
        Y_resi = xic_cpm_regress(Y,C_cova_data);
        [bb,dev,stats] = glmfit(X,Y_resi);
        results{i}.stats = stats;
        glm_np_beha_t(i,j) = stats.t(2,1);
        t=stats.t(2,1);
        glm_np_beha_r(i,j) = sqrt(t^2 / (t^2 + df));
        glm_np_beha_p(i,j) = stats.p(2,1);
    end
end
save corr_np_beha_fu2 glm_np_beha_r glm_np_beha_t glm_np_beha_p C_brain C_cova_data C_beha C_brain_beha