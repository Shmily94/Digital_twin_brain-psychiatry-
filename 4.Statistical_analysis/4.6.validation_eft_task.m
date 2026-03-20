%%compare correlations between simulated and empirical trials (self–self) with those between trials (self–other)

conds = [1,2,3];           % 1=angry, 2=neutral, 3=happy conditions of eft task
nConds = numel(conds);

% Each subject should have:
%   empirical_activation_subjX.mat   (variable: empirical_activation)
%   simulated_activation_subjX.mat   (variable: simulated_activation)
%   condition_subjX.mat        (variable: condition)
% Make sure all files are in the same folder as this script.


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


%% fingerpredict

Nsub = 4;  
%Empirical_activ{n}{t} = voxel vector of subject n, trial t
%Simulate_activ{n}{t} = voxel vector of subject n, trial t
 
Ntrain_trial = [1 2 5 6 9 10]; % first 2 trials used for training
Ntest_trial = [3 4 7 8 11 12];  % last 2 trials of simulated data for testing

% subject template（training：empirical first 2 trials）
templates = cell(1, Nsub);
for n = 1:Nsub
    train_data = [];
    for t = Ntrain_trial
        train_data = [train_data, Empirical_activ{n}{t}(:)]; 
    end
    templates{n} = mean(train_data, 2); % individualized tmeplate
end

%corr simulated last 2 trials with templates
correct = 0;
total = 0;

for n = 1:Nsub
    for t = Ntest_trial
        test_trial =Simulate_activ{n}{t}(:); 
        corr_scores = zeros(1, Nsub);
        for s = 1:Nsub
            valid_idx = ~isnan(test_trial) & ~isnan(templates{s});  
            corr_scores(s) = corr(test_trial(valid_idx), templates{s}(valid_idx));
        end
        corr_scores_all(n,:)=corr_scores;
        [~, pred_sub] = max(corr_scores); 
        if pred_sub == n
            correct = correct + 1;
        end
        total = total + 1;
    end
end

accuracy = correct / total;
fprintf('Identification accuracy: %.1f%%\n', accuracy*100);

xlabel('Subject Template');
ylabel('Test Trial');
title('Correlation of Simulated Trials with Subject Templates');