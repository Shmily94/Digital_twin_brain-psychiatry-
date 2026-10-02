% 结构连接 “dti_net_full” —— n*n
% 灰质体积 “grey_matter_size” —— n*1
% 静息态BOLD “rest_state_bold” —— t*n
% 任务态BOLD “XX_task_bold” XX为该任务的缩写如 “MID_task_bold” —— t*n
% 体素所属脑区 “atlas_region” —— n*1
% 所有脑区编号 “uni_region” —— N*1
% 脑区是否属于皮层 “is_cortex” —— N*1
% 体素在原mask中的编号 “voxel_label” （原mask标记的是灰白质交接的体素，但未必所有体素都会被纳入模型）—— n*1
clear;

%% 数据读取

project_dir = fileparts(mfilename('fullpath'));
if isempty(project_dir)
    project_dir = pwd;
end

target_subjects = { ...
    'sub-000044576096', ...
    'sub-000063218063', ...
    'sub-000111086310', ...
    'sub-000112517217', ...
    'sub-000168370463'};

subpath = dir(fullfile(project_dir, 'sub-*'));
subpath = subpath([subpath.isdir]);
[~, subject_order] = ismember(target_subjects, {subpath.name});
missing_subjects = target_subjects(subject_order == 0);
if ~isempty(missing_subjects)
    warning('Missing subject folder(s): %s', strjoin(missing_subjects, ', '));
end
subpath = subpath(subject_order(subject_order > 0));

for sub = 1:length(subpath)
    
    sub_dir = fullfile(subpath(sub).folder, subpath(sub).name);
    datapath = dir(fullfile(sub_dir, '*.mat'));
    fnames = {datapath.name};
    ffolders = {datapath.folder};
    
    % ---- 1. 按文件名模式匹配各类数据 ----
    
    % SC / DTI —— 含 "connectome"
    sc_idx = find(contains(lower(fnames), 'connectome'), 1);
    if isempty(sc_idx)
        warning('被试 %s: 未找到 connectome 文件，跳过。', subpath(sub).name);
        continue;
    end
    
    % GMV —— 使用更新后的 "<subject>_gmv_new.mat"
    expected_new_gmv = [subpath(sub).name, '_gmv_new.mat'];
    gmv_idx = find(strcmpi(fnames, expected_new_gmv), 1);
    if isempty(gmv_idx)
        warning('被试 %s: 未找到新 GMV 文件 %s，跳过。', subpath(sub).name, expected_new_gmv);
        continue;
    end
    
    % fMRI —— 含 "bold" / "func" / "fmri"
    fmri_idx = find(contains(lower(fnames), 'bold') | ...
                    contains(lower(fnames), 'func') | ...
                    contains(lower(fnames), 'fmri'), 1);
    if isempty(fmri_idx)
        warning('被试 %s: 未找到 fMRI 文件，跳过。', subpath(sub).name);
        continue;
    end
    
    % ---- 2. 加载 SC（v7.3 格式，用 load 返回 struct 避免变量名依赖） ----
    fprintf('[%s] 加载 SC: %s\n', subpath(sub).name, fnames{sc_idx});
    tic;
    sc_data = load(fullfile(ffolders{sc_idx}, fnames{sc_idx}));
    sc_fields = fieldnames(sc_data);
    dti_net_full = sc_data.(sc_fields{1});   % 动态取第一个（也是唯一一个）变量
    clear sc_data;
    toc;
    
    % ---- 3. 加载 GMV（兼容 gmv_indi / gmv 两种变量名） ----
    fprintf('[%s] 加载 GMV: %s\n', subpath(sub).name, fnames{gmv_idx});
    tic;
    gmv_data = load(fullfile(ffolders{gmv_idx}, fnames{gmv_idx}));
    if isfield(gmv_data, 'gmv_indi')
        grey_matter_size = gmv_data.gmv_indi';
    elseif isfield(gmv_data, 'gmv')
        grey_matter_size = gmv_data.gmv';
    else
        gmv_fields = fieldnames(gmv_data);
        grey_matter_size = gmv_data.(gmv_fields{1})';
        warning('被试 %s: GMV 变量名未知 (%s)，自动取第一个字段。', ...
            subpath(sub).name, gmv_fields{1});
    end
    clear gmv_data;
    toc;
    
    % ---- 4. 加载 fMRI（兼容 Func_bold / Func_bold_mid_rest_sst 等变量名） ----
    fprintf('[%s] 加载 fMRI: %s\n', subpath(sub).name, fnames{fmri_idx});
    tic;
    fmri_data = load(fullfile(ffolders{fmri_idx}, fnames{fmri_idx}));
    fmri_fields = fieldnames(fmri_data);
    bold_cell = fmri_data.(fmri_fields{1});   % cell 数组
    clear fmri_data;
    toc;
    
    % ---- 5. 按时间维度自动匹配 MID / rest / SST ----
    %     预期时间点数: MID ≈ 190,  Rest ≈ 165,  SST ≈ 350
    %     可能有第 4 个多余数组（~200 时间点），将被跳过
    n_cells = length(bold_cell);
    tp = zeros(1, n_cells);
    for c = 1:n_cells
        tp(c) = size(bold_cell{c}, 1);   % 时间维度（行数）
    end
    fprintf('[%s] fMRI cell 时间点数: %s\n', subpath(sub).name, mat2str(tp));
    
    if n_cells < 3
        error('被试 %s: fMRI cell 数量不足（%d < 3），无法提取 MID/rest/SST。', ...
            subpath(sub).name, n_cells);
    end
    
    % 贪心匹配：对每种条件，从未匹配的 cell 中找到时间点数最接近的
    exp_tp = [190, 165, 350];           % [MID, Rest, SST]
    cond_labels = {'MID', 'Rest', 'SST'};
    used = false(1, n_cells);
    assign_idx = zeros(1, 3);
    
    for k = 1:3
        diffs = abs(tp - exp_tp(k));
        diffs(used) = Inf;
        [min_diff, best] = min(diffs);
        used(best) = true;
        assign_idx(k) = best;
        fprintf('[%s]   %s <- cell{%d}  (tp=%d, diff=%d)\n', ...
            subpath(sub).name, cond_labels{k}, best, tp(best), min_diff);
    end
    
    MID_task_bold   = bold_cell{assign_idx(1)};
    rest_state_bold = bold_cell{assign_idx(2)};
    SST_task_bold   = bold_cell{assign_idx(3)};
    
    % 检查是否有未匹配的多余 cell
    unused = find(~used);
    if ~isempty(unused)
        for u = unused
            warning('被试 %s: cell{%d} (tp=%d) 未被匹配，已跳过。', ...
                subpath(sub).name, u, tp(u));
        end
    end

%% mask与atlas
atlas_table = readtable(fullfile(project_dir, "shen_268.csv"));
voxel_location = niftiread(fullfile(project_dir, "MNI152_T1_3mm_gmwmi_shen268_label.nii"));
atlas_image = niftiread(fullfile(project_dir, "shen_3mm_268_parcellation.nii"));

assert(max(voxel_location,[],'all') == length(grey_matter_size),'mask file have different voxel numbers with data')

% 得到体素的脑区分布
atlas_region = zeros([length(unique(voxel_location))-1, 1]);
for i=1:length(atlas_region)
    atlas_region(i) = atlas_image(voxel_location(:) == i);
end
sum(atlas_region == 0)

%% 去除小脑和脑干，并区分皮层和皮层下

leave_out = {'Cerebellum', 'BrainStem'};
Sub_regions = {'n/a', 'Caudate', 'Putamen', 'Thalamus', 'Amygdala', 'Hippocampus'};

atlas_table = atlas_table(~ismember(atlas_table.BA, leave_out),:);
uni_region = atlas_table.ROI;
is_cortex = ~ismember(atlas_table.BA,Sub_regions);

voxel_label = 1:length(atlas_region);
voxel_label = voxel_label(ismember(atlas_region,uni_region))';

rest_state_bold = rest_state_bold(:,ismember(atlas_region,uni_region));
MID_task_bold = MID_task_bold(:,ismember(atlas_region,uni_region));
SST_task_bold = SST_task_bold(:,ismember(atlas_region,uni_region));
grey_matter_size = grey_matter_size(ismember(atlas_region,uni_region));
dti_net_full = dti_net_full(ismember(atlas_region,uni_region),ismember(atlas_region,uni_region));

atlas_region = atlas_region(ismember(atlas_region,uni_region));

%% dti对称化以及bold计算z-score

dti_net_full = dti_net_full + dti_net_full';
dti_net_full(eye(size(dti_net_full)) == 1) = 0;

rest_state = rest_state_bold;
for i=1:size(rest_state,2)
    rest_state_bold(:,i) = zscore(rest_state(:,i));
end
task_state = MID_task_bold;
for i=1:size(task_state,2)
    MID_task_bold(:,i) = zscore(task_state(:,i));
end
task_state = SST_task_bold;
for i=1:size(task_state,2)
    SST_task_bold(:,i) = zscore(task_state(:,i));
end

subplot(2,1,1)
plot(rest_state_bold(:,1:10))

%% bold滤波
fs = 1/2.2;
fpass = [0.01,0.1];
rest_state_bold = bandpass(rest_state_bold,fpass,fs);
MID_task_bold = bandpass(MID_task_bold,fpass,fs);
SST_task_bold = bandpass(SST_task_bold,fpass,fs);

subplot(2,1,2)
plot(rest_state_bold(:,1:10))

out_file = fullfile(sub_dir, [subpath(sub).name, '_voxel_data.mat']);
save(out_file, "dti_net_full","atlas_region","uni_region","is_cortex", ...
    "voxel_label","grey_matter_size","MID_task_bold","rest_state_bold","SST_task_bold");
fprintf('[%s] 已保存: %s\n', subpath(sub).name, out_file);
end
