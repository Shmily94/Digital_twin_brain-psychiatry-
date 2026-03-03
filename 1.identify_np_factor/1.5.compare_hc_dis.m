%% compare beha between control and stratify
clear;clc
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\HC_brain_beha_cova.mat');
[C,ia,ib]=intersect(beha.subject,cova_subject);
hc_data=[beha.data(ia,:),cova_data(ib,:)];

load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\Behavior_related_results\beha_data\STRA_self_dawba.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\cova_subject_stra.mat');
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\Diseased\*');
STRA_MID_subject2=CPM_Result.subject;
STRA_SST_subject2=CPM_Result.subject;
beha_data=STRA_self.STRA_psy_match;
beha_id=STRA_self.psy_match_sub;
cova_data=cova_data;
cova_id=cova_subject;
[C_diseased,ia,ib]=intersect (STRA_SST_subject2,cova_subject); % STRA_SST_subject2 or STRA_MID_subject2
cova_data2=cova_data(ib,:);
[C_diseased2,ia,ib]=intersect(C_diseased,STRA_self.psy_match_sub);
beha_data=STRA_self.STRA_psy_match(ib,:);
cova_data3=cova_data2(ia,:);
dis_data=[beha_data,cova_data3];
dis_data(:,7)=2; % second group

Y=[hc_data(:,1:6);dis_data(:,1:6)];
X=[hc_data(:,7:end);dis_data(:,7:end)];
Y_resi = xic_cpm_regress(Y,X(:,2:end));
for i = 1:6
    
    [bb,dev,stats] = glmfit(X,Y_resi(:,i)); % group,site,and sex 
    results{i}.stats = stats;
    group_compare_hc_dis_beha(i,1) = stats.t(2,1);
    group_compare_hc_dis_beha(i,2) = stats.p(2,1);
end
save beha_compare_SST C hc_data C_diseased2 dis_data group_compare_hc_dis_beha results

%% compare NP between control and stratify
clear;clc
cd('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro2');
load('diseased_label.mat');
load('STRA_NP_dis_control.mat');
load('FU2_control_NP_factor.mat');
NP_factor_fu2_control=[NP_factor,NP_factor_neg];
load('FU3_control_NP_factor_new.mat'); % 因为没有头动数据，所以又删掉一些人
NP_HC=[NP_factor_stra_control;NP_factor_fu2_control;NP_fu3_new];
NP_HC_id=[STRA_control_id2;FU2_control_id2;ID_fu3_new];
load('STRA_NP_dis_control_new.mat');% 因为没有头动数据，所以又删掉1个人
% [C,ia,ib]=intersect(STRA_dis_id_new,STRA_dis_id);
% NP_dis=NP_factor_stra_dis(ib,:);
% NP_dis_id=C;
% whole diseasd
Y=[NP_HC;NP_dis];
load('D:\postdoc\Work\Computer-Brain-Project\Results\Followup2\CPM_Models_discard_contro\compare_NP_stra\beha_compare_NP_whole_dis.mat');
X=cova;
Y_resi = xic_cpm_regress(Y,X(:,2:end));
for i = 1:2
    
    [bb,dev,stats] = glmfit(X,Y_resi(:,i)); % group,site,sex and hd 
    results{i}.stats = stats;
    glm_np_beha(i,1) = stats.t(2,1);
    glm_np_beha(i,2) = stats.p(2,1);

end
save compare_NP_whole_diseased  X Y_resi glm_np_beha results

% specific_disorder
X=cova(diseased_label.MDD==1,:);
Y_resi = xic_cpm_regress(Y(diseased_label.MDD==1,:),X(:,2:end));
for i = 1:2
    
    [bb,dev,stats] = glmfit(X,Y_resi(:,i)); % group,site,sex and hd 
    results{i}.stats = stats;
    glm_np_beha(i,1) = stats.t(2,1);
    glm_np_beha(i,2) = stats.p(2,1);

end

save compare_NP_eat  X Y_resi glm_np_beha results


%corr NP with beha in the STRATIFY
load('D:\postdoc\Work\Computer-Brain-Project\Results\Stratify\CPM_Models\beha_compare_MID.mat');
beha_id=[C;C_diseased2];
beha_data=[hc_data;dis_data];
[C,ia,ib]=intersect(NP_id,beha_id);
NP_C=NP(ia,:);
beha_data_C=beha_data(ib,:);
cova_C=beha_data_C(:,8:end);
% hd=NP(ia,3);
cova_C=[cova_C,hd];

for j=1:2
X=NP_C(:,j);
for i=1:6
Y=beha_data_C(:,i);
% Y_resi = xic_cpm_regress(Y,[X,cova_C]);

    [bb,dev,stats] = glmfit([X,cova_C],Y); % NP,site, sex,hd
    results{i,j}.stats = stats;
    glm_np_beha_t(i,j) = stats.t(2,1);
    glm_np_beha_p(i,j) = stats.p(2,1);

end
end
save glm_NP_beha_STRA NP_C C cova_C beha_data_C glm_np_beha_t glm_np_beha_p results

beha_data_C2(:,1)=beha_data_C(:,1)+beha_data_C(:,2);
beha_data_C2(:,2)=beha_data_C(:,3)+beha_data_C(:,4)+beha_data_C(:,5)+beha_data_C(:,6);

for j=1:2
X=NP_C(:,j);
for i=1:2
Y=beha_data_C2(:,i);
% Y_resi = xic_cpm_regress(Y,[X,cova_C]);

    [bb,dev,stats] = glmfit([X,cova_C],Y); % NP,site, sex,hd
    results2{i,j}.stats = stats;
    glm_np_beha_t2(i,j) = stats.t(2,1);
    glm_np_beha_p2(i,j) = stats.p(2,1);

end
end
save glm_NP_beha_STRA2 NP_C C cova_C beha_data_C2 glm_np_beha_t2 glm_np_beha_p2 results2

