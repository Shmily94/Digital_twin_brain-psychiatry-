%% ============================================================
%  EFT self-other validation for Digital Twin Brain simulations
%  Author: Yunman Xia
%  Date: 2025-10
% =============================================================

clear; clc;

%% ====== Settings ======
nSubj = 4;                 % number of subjects
conds = [1,2,3];           % 1=angry, 2=neutral, 3=happy
nConds = numel(conds);

% subjects' data file naming rule
% Each subject should have:
%   empirical_BOLD_subjX.mat   (variable: empirical_BOLD)
%   simulated_BOLD_subjX.mat   (variable: simulated_BOLD)
%   condition_subjX.mat        (variable: condition)
% Make sure all files are in the same folder as this script.

%% ====== Load data ======
% for s = 1:nSubj
%     fprintf('Loading subject %d ...\n', s);
%     load(['empirical_BOLD_subj' num2str(s) '.mat']);  % empirical_BOLD
%     load(['simulated_BOLD_subj' num2str(s) '.mat']);  % simulated_BOLD
%     load(['condition_subj' num2str(s) '.mat']);       % condition
% 
%     data(s).emp = empirical_BOLD;
%     data(s).sim = simulated_BOLD;
%     data(s).cond = task_vector;
% end

% step 1: 找到共有的值
shared_ab = intersect(voxel_label_all{1}, voxel_label_all{2});
shared_abc = intersect(shared_ab, voxel_label_all{3});
shared_all = intersect(shared_abc, voxel_label_all{4});

disp('Shared values in all four vectors:');
disp(shared_all);

% step 1: 找到共有的值
% 对共有值逐个找索引
for i = 1:length(shared_all)
    val = shared_all(i);
    idx_a(i) = find(voxel_label_all{1} == val);
    idx_b(i) = find(voxel_label_all{2} == val);
    idx_c(i) = find(voxel_label_all{3} == val);
    idx_d(i) = find(voxel_label_all{4} == val);

    %fprintf('Value %d: a(%d), b(%d), c(%d), d(%d)\n', ...
       % val, idx_a, idx_b, idx_c, idx_d);
end
idx=[idx_a;idx_b;idx_c;idx_d]';
for s = 1:nSubj        
        data_shared(s).emp = data(s).emp(:,idx(:,s)); % 1x12000
        data_shared(s).sim = data(s).sim(:,idx(:,s));
        data_shared(s).cond = data(s).cond;
end


%% ====== Compute  BOLD per condition ======
for s = 1:nSubj
    for c = conds
        idx = (data_shared(s).cond == c);
        data_shared(s).emp_condition{c} = data_shared(s).emp(idx,:); % 1x12000
        c(s).sim_condition{c} = data_shared(s).sim(idx,:);
    end
end

%% ====== Compute self simulated vs other empirical correlations of same condition using all bold signals======
r_mat = nan(nSubj, nSubj, nConds); % [self x other x condition]

for c = conds
    for i = 1:nSubj
        for j = 1:nSubj
            A=data_shared(i).sim_condition{c};
            B=data_shared(j).emp_condition{c};
            % 获取两个矩阵的时间点数
nTime_A = size(A,1);
nTime_B = size(B,1);

% 取最小时间点
nTime = min(nTime_A, nTime_B);

% 截取前 nTime 时间点
A_trim = A(1:nTime,:);
B_trim = B(1:nTime,:);

r_mat(i,j,c) = corr2(A_trim, B_trim);
        end
    end
end
%% compute self simulate and empirical vs other empirical correlations of half time series
r_mat_half = nan(nSubj, nSubj, nConds); % [self x other x condition]

for c = conds
    for i = 1:nSubj
        for j = 1:nSubj
            A=data_shared(i).sim_condition{c};
            B=data_shared(j).emp_condition{c};
            % 获取两个矩阵的时间点数
%nTime_A = size(A,1);
%nTime_B = size(B,1);

% 取最小时间点
%nTime = min(nTime_A, nTime_B);
nTime=16;
% 截取前 nTime 时间点
%A_trim = A(1:nTime,:);
%B_trim = B(1:nTime,:);
A_trim = A(1:nTime,:);
B_trim = B(end-15:end,:);

r_mat_half(i,j,c) = corr2(A_trim, B_trim);
        end
    end
end

%% compute self empirical and empirical vs other empirical correlations of half time series
r_mat_half = nan(nSubj, nSubj, nConds); % [self x other x condition]

for c = conds
    for i = 1:nSubj
        for j = 1:nSubj
            A=data_shared(i).emp_condition{c};
            B=data_shared(j).emp_condition{c};
            % 获取两个矩阵的时间点数
%nTime_A = size(A,1);
%nTime_B = size(B,1);

% 取最小时间点
%nTime = min(nTime_A, nTime_B);
nTime=16;
% 截取前 nTime 时间点
%A_trim = A(1:nTime,:);
%B_trim = B(1:nTime,:);
A_trim = A(1:nTime,:);
B_trim = B(end-15:end,:);

r_mat_half(i,j,c) = corr2(A_trim, B_trim);
        end
    end
end
%% compute self vs other correlations of half time series in assimilated voxels

for i = 1:length(assimilated_idx)
    val = assimilated_idx(i);
    assimilated_idx_atlas_region{i} = find(atlas_region_c == val);

end

assimilated_idx_all = vertcat(assimilated_idx_atlas_region{:}');
r_mat_half_assimi = nan(nSubj, nSubj, nConds); % [self x other x condition]

for c = conds
    for i = 1:nSubj
        for j = 1:nSubj
            A=data_shared(i).sim_condition{c};
            B=data_shared(j).emp_condition{c};
            % 获取两个矩阵的时间点数
nTime_A = size(A,1);
nTime_B = size(B,1);

% 取最小时间点
nTime = min(nTime_A, nTime_B);
%nTime=16;
% 截取前 nTime 时间点
A_trim = A(1:nTime,assimilated_idx_all);
B_trim = B(1:nTime,assimilated_idx_all);
%A_trim = A(1:nTime,assimilated_idx_all);
%B_trim = B(end-15:end,assimilated_idx_all);

r_mat_half_assimi(i,j,c) = corr2(A_trim, B_trim);
        end
    end
end
%% ====== Display results ======
for c = 1:nConds
    fprintf('\nCondition %d (1=angry, 2=neutral, 3=happy):\n', c);
    disp(round(r_mat(:,:,c),3))
end

%% ====== Compute self vs other difference ======
self_corr = nan(nSubj, nConds);
other_corr = nan(nSubj, nConds);

for c = 1:nConds
    for s = 1:nSubj
        self_corr(s,c) = r_mat(s,s,c);
        temp = r_mat(s,:,c);
        temp(s) = []; % remove self
        other_corr(s,c) = mean(temp);
    end
end

diff_corr = self_corr - other_corr;

disp('Mean self vs other correlation difference by condition:')
disp(mean(diff_corr,1));

%% ====== Statistical test ======
for c = 1:nConds
    [~,p(c)] = ttest(self_corr(:,c), other_corr(:,c));
end

results_table = table((1:3)', mean(self_corr)', mean(other_corr)', p', ...
    'VariableNames', {'Condition','Self_r','Other_r','p_value'});
disp(results_table);

%% ====== Plot results ======
figure;
bar([mean(self_corr); mean(other_corr)]');
set(gca, 'XTickLabel', {'Angry','Neutral','Happy'});
legend({'Self','Other'}, 'Location','best');
ylabel('Correlation (r)');
title('EFT model validation: self vs other prediction');
grid on;

%% extract activation 
maskfile=('MNI152_T1_3mm_gmwmi_shen268_label.nii');
mask=load_nii(maskfile);
img=mask.img;

for i=1:2472
idx(1,i)=find(img==assimilated_idx_all(i)); %find assimilated voxels location

end

sub=dir('sub*');

for n=1:4   
for s=1:4
   
load(fullfile(sub(n).folder,sub(n).name,'empirical_eft_con_map.mat')); % sub1
load(fullfile(sub(s).folder,sub(s).name,'simulate_eft_con_map.mat')); % sub2

clear empiri_assim simulate_assim

for j=5:6 % 1:2 angry, 5:6 neutral, 9:10 happy
    simulate_data=simulate_activ{j}; % sub1 first half simulated data
    simulate_assim(:,j)=simulate_data(idx);
    empiri_data=empirical_activ{j+2}; % sub2 second half real data 
    empiri_assim(:,j-4)=empiri_data(idx);  
    
end

valid = all(~isnan(simulate_assim), 2) & all(~isnan(empiri_assim), 2);
[r,p]=corr(mean(simulate_assim(valid,:), 2),mean(empiri_assim(valid,:), 2) );
r_activ_simulate_empirical(n,s) = r;
p_activ_simulate_empirical(n,s) = p;

end
end


save eft_angry_r_assimi_voxel_activ_simulate_empirical_trial_4subs r_activ_simulate_empirical p_activ_simulate_empirical 


for n=1:4   
for s=1:4
   
empirical_activ_sub1=load(fullfile(sub(n).folder,sub(n).name,'empirical_eft_con_map.mat')); % sub1
empirical_activ_sub2=load(fullfile(sub(s).folder,sub(s).name,'empirical_eft_con_map.mat')); % sub2

clear empiri_assim_1 empiri_assim_2

for j=9:10 % 1:2 angry, 5:6 neutral, 9:10 happy
    empiri_data_1=empirical_activ_sub1.empirical_activ{j}; % sub1 first half real data 
    empiri_assim_1(:,j-8)=empiri_data_1(idx); 
    empiri_data_2=empirical_activ_sub2.empirical_activ{j+2}; % sub2 second half real data 
    empiri_assim_2(:,j-8)=empiri_data_2(idx);  
    
end

valid = all(~isnan(empiri_assim_1), 2) & all(~isnan(empiri_assim_2), 2);
[r,p]=corr(mean(empiri_assim_1(valid,:), 2),mean(empiri_assim_2(valid,:), 2) );
r_activ_empirical_empirical(n,s) = r;
p_activ_empirical_empirical(n,s) = p;

end
end

save eft_happy_r_assimi_voxel_activ_empirical_empirical_trial_4subs r_activ_empirical_empirical p_activ_empirical_empirical 


%% calculate each trial simulated and empirical correlations bootstrap
clear all; clc;

Nsub = 4;
Ntrial = 12;

for n = 1:Nsub
    % load subject n empirical
    load(fullfile(sub(n).folder, sub(n).name, 'empirical_eft_con_map.mat'));

    % extract empirical voxel × trial matrix
    Emp = zeros(length(idx), Ntrial);
    for t = 1:Ntrial
        tmp = empirical_activ{t};
        Emp(:, t) = tmp(idx);
    end

    for k = 1:Ntrial

        % ---- Simulated trial k of subject n ----
        load(fullfile(sub(n).folder, sub(n).name, 'simulate_eft_con_map.mat'));
        tmp = simulate_activ{k};
        Sim_k = tmp(idx);

        % remove NaN for this trial pair
        valid = ~isnan(Sim_k);
        Sim_k=Sim_k';

        %% -------- Within-subject correlations --------
        within_corr = zeros(1, Ntrial);
        for t = 1:Ntrial
            emp_t = Emp(:, t);
            valid2 = valid & ~isnan(emp_t');
           
            within_corr(t) = corr(Sim_k(valid2), emp_t(valid2));
        end

        %% -------- Between-subject correlations --------
        between_corr = [];

        for s = 1:Nsub
            if s == n, continue; end

            load(fullfile(sub(s).folder, sub(s).name, 'empirical_eft_con_map.mat'));

            for t = 1:Ntrial
                tmp2 = empirical_activ{t};
                emp_other = tmp2(idx);
                emp_other=emp_other';

                valid2 = valid & ~isnan(emp_other');
                between_corr(end+1) = corr(Sim_k(valid2), emp_other(valid2));
            end
        end

        % save distributions
        ALL_within{n, k} = within_corr;
        ALL_between{n, k} = between_corr;

        % statistical test
        [pval, h] = ranksum(within_corr, between_corr); % non-parametric

        results(n, k).within = within_corr;
        results(n, k).between = between_corr;
        results(n, k).p = pval;
        results(n, k).sig = h;
    end
end

save corr_simulate_self_and_other_empirical_activ_4subs_12_trials_bootstrap results

figure;
hold on;

all_within = [];
all_between = [];
group = [];

for n = 1:Nsub
    for k = 1:Ntrial
        all_within = [all_within, results(n,k).within];
        all_between = [all_between, results(n,k).between];

        group = [group, ones(1,length(results(n,k).within))*n]; % 分组用
    end
end

% Boxplot
boxplot([all_within, all_between], [ones(1,length(all_within)), 2*ones(1,length(all_between))], ...
    'Labels', {'Within','Between'});
ylabel('Correlation');
title('Trial-level simulated vs empirical correlations');

figure;
for n = 1:Nsub
    subplot(2,2,n);
    within_mean = cellfun(@mean, results(n,:));
    between_mean = cellfun(@mean, results(n,:));

    plot(1:Ntrial, within_mean, '-o', 'LineWidth', 2, 'DisplayName','Within');
    hold on;
    plot(1:Ntrial, between_mean, '-s', 'LineWidth', 2, 'DisplayName','Between');
    xlabel('Trial');
    ylabel('Correlation');
    title(sprintf('Subject %d', n));
    legend;
end

all_corr = [all_within, all_between];
group_label = [repmat({'1'},1,length(all_within)), repmat({'2'},1,length(all_between))];

violinplot(all_corr, char(group_label));
ylabel('Correlation');
title('Within vs Between-subject correlations');

%% predict
%% 假设你的数据结构
% Nsub = 4; % 被试数
% Ntrial = 16; % 每个被试 trial 数
% empirical_activ{n}{t} = voxel vector of subject n, trial t
% simulate_activ{n}{t} = voxel vector of subject n, trial t
Nsub = 4;
Ntrial=12;
for n = 1:Nsub
    % load subject n empirical
    load(fullfile(sub(n).folder, sub(n).name, 'empirical_eft_con_map.mat'));

    % extract empirical voxel × trial matrix
    %Emp = zeros(length(idx), Ntrial);
    for t = 1:Ntrial
        tmp = empirical_activ{t};
        Emp{n}{t} = tmp(idx);
    end
end
save simulate_empirical_eft_activation_4subs Empirical_activ Simulate_activ

%% fingerpredict corr
Nsub = 4;   
Ntrain_trial = [1 2 5 6 9 10]; % first 2 trials used for training
Ntest_trial = [1 2 5 6 9 10];  % last 2 trials of simulated data for testing

% 构建 subject template（training：empirical first 2 trials）
templates = cell(1, Nsub);
for n = 1:Nsub
    train_data = [];
    for t = Ntrain_trial
        train_data = [train_data, Empirical_activ{n}{t}(:)]; % 列向量
    end
    templates{n} = mean(train_data, 2); % 平均得到模板
end

% 测试：用 simulated first 2 trials
correct = 0;
total = 0;

for n = 1:Nsub
    for t = Ntest_trial
        test_trial =Simulate_activ{n}{t}(:); % 列向量
        corr_scores = zeros(1, Nsub);
        for s = 1:Nsub
            valid_idx = ~isnan(test_trial) & ~isnan(templates{s});  % 只保留非 NaN
            corr_scores(s) = corr(test_trial(valid_idx), templates{s}(valid_idx));
        end
        corr_scores_all(n,:)=corr_scores;
        [~, pred_sub] = max(corr_scores); % 预测 subject
        if pred_sub == n
            correct = correct + 1;
        end
        total = total + 1;
    end
end

accuracy = correct / total;
fprintf('Identification accuracy: %.1f%%\n', accuracy*100);

% corr_matrix(trial, subject_template)
corr_matrix = zeros(Nsub*6, Nsub);
row_idx = 1;
for n = 1:Nsub
    for t = Ntest_trial
        test_trial = Simulate_activ{n}{t}(:);
        for s = 1:Nsub
            template = templates{s};
            valid_idx = ~isnan(test_trial) & ~isnan(template);  % 只保留非 NaN
            
            corr_matrix(row_idx, s) = corr(test_trial(valid_idx), template(valid_idx));
        end
        row_idx = row_idx + 1;
    end
end

figure;
imagesc(corr_matrix);
colorbar;
xlabel('Subject Template');
ylabel('Test Trial');
title('Correlation of Simulated Trials with Subject Templates');