

function [train_behav,test_behav,train_data,test_data] = xic_cpm_site_cv(all_mats,all_behav,phenotype_subject)




cova = load('/home1/xic_fdu/project/IAMGEN/Match_control_subject_All things scale/Cova_subject_jia.mat');

cova_data = cova.cova_data;
cova_subject = cova.cova_subject;


[all,a,b] = intersect(phenotype_subject,cova_subject);


all_behav = all_behav(a);
cova_data = cova_data(b,:);

cova_site = cova_data(:,2:8);

site = repmat([1:7],size(cova_site,1),1);

site_all = sum(site.*cova_site,2)+1;


nfold = 10;

train_sub ={0};
test_sub = {0};

for i=1:8
    
    subject = find(site_all == i);
    
    index = crossvalind('Kfold',length(subject),nfold);
    
    test_sub{i} = subject(index==1);
    train_sub{i} = subject(index~=1);  
    
    site_score(i) = mean(all_behav(site_all==i));
    
    subplot(4,2,i)
    histogram( all_behav(site_all==i),20)
end

 subject_test = vertcat(test_sub{:});
 subject_train = vertcat(train_sub{:});
 
 test_site = cova_data(subject_test,:);
 train_site = cova_data(subject_train,:);
 
 test_data = all_mats(subject_test,:);
 train_data = all_mats(subject_train,:);
 
 test_behav_o = all_behav(subject_test);
 train_behav_o = all_behav(subject_train);
 
 [a b test_behav d] = regress(test_behav_o,test_site(:,1:8));
 [a b train_behav d]= regress(train_behav_o,train_site(:,1:8));
 
end
 
 




