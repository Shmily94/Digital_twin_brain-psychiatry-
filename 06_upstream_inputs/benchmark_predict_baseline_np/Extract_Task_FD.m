clear;clc

subses = {'ses-b0','ses-d2','ses-d10','ses-p2','ses-p10'};
for m = 1:5
    Prep = '/public/home/dtbrain/project/psj/test_YMX/ds005917/derivatives/fmriprep';
    First_level = '/public/home/dtbrain/project/psj/test_YMX/ds005917/first_level/EFT';
    ses = subses{m};
    cd ’/public/home/dtbrain/project/psj/test_YMX/ds005917/derivatives/fmriprep‘
    sub = dir('sub-*');
    sub = sub([sub.isdir]);
    n_sub=length(sub);
% 初始化结果（NaN表示缺失）
    FD_sub_run1  = nan(n_sub, 1);
    FD_sub_run2  = nan(n_sub, 1);
    missing_log  = {};  % 记录缺失信息


    for i = 1:length(sub)
        disp(i)
        motion = dir(fullfile(Prep,sub(i).name,ses,'func','*task-emoeval_*confounds*.tsv'));

        if isempty(motion)
            msg = sprintf('[%s] %s %s: 无confounds文件', ...
                ses, sub(i).name, ses);
            fprintf('⚠ %s\n', msg);
            missing_log{end+1} = msg;
            continue;  % 跳过该被试
        end
        if length(motion) >= 2
       
        sub_motion1 = struct2table(tdfread(fullfile(motion(1).folder,motion(1).name)));
        sub_motion1 = [sub_motion1.rot_x,sub_motion1.rot_y,sub_motion1.rot_z,sub_motion1.trans_x,sub_motion1.trans_y,sub_motion1.trans_z];
        FD_sub_run1(i) = mean(sum([50*abs(sub_motion1(2:end,1:3) - sub_motion1(1:end-1,1:3)),abs(sub_motion1(2:end,4:6) - sub_motion1(1:end-1,4:6))],2));
        sub_motion2 = struct2table(tdfread(fullfile(motion(2).folder,motion(2).name)));
        sub_motion2 = [sub_motion2.rot_x,sub_motion2.rot_y,sub_motion2.rot_z,sub_motion2.trans_x,sub_motion2.trans_y,sub_motion2.trans_z];
        FD_sub_run2(i) = mean(sum([50*abs(sub_motion2(2:end,1:3) - sub_motion2(1:end-1,1:3)),abs(sub_motion2(2:end,4:6) - sub_motion2(1:end-1,4:6))],2));
        
        end
    end
    
    T = table;
    T.SubID = {sub.name}';
    T.mean_FD_run1 = FD_sub_run1;
    T.mean_FD_run2 = FD_sub_run2;
    % T.missing_run1 = isnan(FD_sub_run1);
    % T.missing_run2 = isnan(FD_sub_run2);
    writetable(T,['EFT_',ses,'_mean_FD.txt']);

    if ~isempty(missing_log)
        missing_file = ['EFT_', ses, '_missing_log.txt'];
        fid = fopen(missing_file, 'w');
        for k = 1:length(missing_log)
            fprintf(fid, '%s\n', missing_log{k});
        end
        fclose(fid);
        fprintf('⚠ 缺失记录已保存: %s (%d条)\n', missing_file, length(missing_log));
    else
        fprintf('✓ %s: 所有被试数据完整\n', ses);
    end
    
    fprintf('\n');
end