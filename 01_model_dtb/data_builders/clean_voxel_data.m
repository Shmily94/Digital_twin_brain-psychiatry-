% 清理 IMAGEN 体素数据中的空体素和孤立体素。
%
% 本脚本对齐 normal_generation.py 中 get_valid_voxel_indices 的逻辑：
%   1. 先删除 grey_matter_size <= 0 的空体素；
%   2. 将 DTI 矩阵的自连接，也就是对角线元素，置为 0；
%   3. 在剩余体素构成的 DTI 子网络中，迭代删除行和为 0 的孤立体素；
%   4. 默认只检查行和，不要求列和大于 0，与 normal_generation.py 的默认参数一致。
%
% 运行方式：
%   在 MATLAB 当前目录切换到本文件所在文件夹后运行 clean_voxel_data
%   或在命令行运行 matlab -batch "clean_voxel_data"
%
% 输出说明：
%   原始 data 目录不会被覆盖；清理后的 .mat 文件保存到 data_cleaned 目录。
%   每个输出文件中会额外保存有效体素索引、被删除体素索引和 filter_info。

clear;
clc;

% 获取脚本所在目录，保证从其他工作目录调用时也能找到 data 文件夹。
thisDir = fileparts(mfilename('fullpath'));
if isempty(thisDir)
    thisDir = pwd;
end

% 批处理参数。通常只需要修改 dataDir 或 outputDir。
dataDir = fullfile(thisDir, 'data');
outputDir = fullfile(thisDir, 'data_cleaned');
filePattern = '*_voxel_data.mat';

% 与 normal_generation.py 保持一致：去掉自连接，且不强制要求入连接列和非零。
removeDiagonal = true;
requireCol = false;

% true 表示重复运行时覆盖 data_cleaned 中同名输出文件。
overwriteOutput = true;

summary = clean_voxel_data_batch( ...
    dataDir, outputDir, filePattern, ...
    removeDiagonal, requireCol, overwriteOutput);

disp(struct2table(summary));


function summary = clean_voxel_data_batch(dataDir, outputDir, filePattern, removeDiagonal, requireCol, overwriteOutput)
    % 批量清理指定目录下的体素 .mat 文件，并写出汇总表。

    if ~isfolder(dataDir)
        error("Data directory does not exist: %s", dataDir);
    end

    % 输出目录独立于原始数据目录，避免误覆盖原始 .mat 文件。
    if ~isfolder(outputDir)
        mkdir(outputDir);
    end

    matFiles = dir(fullfile(dataDir, filePattern));
    if isempty(matFiles)
        error("No files found for pattern: %s", fullfile(dataDir, filePattern));
    end

    % 每个文件记录原始体素数、空体素删除数、孤立体素删除数和输出路径。
    summary = repmat(struct( ...
        "file", "", ...
        "n_original", 0, ...
        "n_after_grey_matter", 0, ...
        "n_final", 0, ...
        "n_removed_empty", 0, ...
        "n_removed_isolated", 0, ...
        "iterations", 0, ...
        "output_file", ""), numel(matFiles), 1);

    for k = 1:numel(matFiles)
        inputFile = fullfile(matFiles(k).folder, matFiles(k).name);
        [~, baseName, ext] = fileparts(matFiles(k).name);
        outputFile = fullfile(outputDir, sprintf("%s_cleaned%s", baseName, ext));

        fprintf("\n[%d/%d] Cleaning %s\n", k, numel(matFiles), inputFile);

        one = clean_one_voxel_file( ...
            inputFile, outputFile, removeDiagonal, requireCol, overwriteOutput);

        summary(k).file = string(matFiles(k).name);
        summary(k).n_original = one.n_original;
        summary(k).n_after_grey_matter = one.n_after_grey_matter;
        summary(k).n_final = one.n_final;
        summary(k).n_removed_empty = one.n_removed_empty;
        summary(k).n_removed_isolated = one.n_removed_isolated;
        summary(k).iterations = one.iterations;
        summary(k).output_file = string(outputFile);
    end

    % 汇总文件便于后续快速检查各被试的筛选结果。
    summaryTable = struct2table(summary);
    writetable(summaryTable, fullfile(outputDir, "filter_summary.csv"));
    save(fullfile(outputDir, "filter_summary.mat"), "summary", "summaryTable", "-v7.3");
end


function one = clean_one_voxel_file(inputFile, outputFile, removeDiagonal, requireCol, overwriteOutput)
    % 清理单个被试文件，并保持各体素级变量的体素维度同步筛选。

    if exist(outputFile, "file") && ~overwriteOutput
        error("Output file exists and overwriteOutput=false: %s", outputFile);
    end

    data = load(inputFile);

    required = ["dti_net_full", "grey_matter_size"];
    for i = 1:numel(required)
        name = char(required(i));
        if ~isfield(data, name)
            error("Missing required variable '%s' in %s", name, inputFile);
        end
    end

    % DTI 矩阵体积较大，先从 data 结构中取出，后续输出时再放回 out。
    dti = data.dti_net_full;
    data = rmfield(data, 'dti_net_full');

    if ndims(dti) ~= 2 || size(dti, 1) ~= size(dti, 2)
        error("dti_net_full must be square. Got size [%s]", num2str(size(dti)));
    end

    nVox = size(dti, 1);
    blockSize = double(data.grey_matter_size(:));
    if numel(blockSize) ~= nVox
        error( ...
            "grey_matter_size length does not match dti size. length=%d, dti=%d x %d", ...
            numel(blockSize), size(dti, 1), size(dti, 2));
    end

    % normal_generation.py 先把对角线置零，再检查 NaN/Inf/负值。
    dti = prepare_dti_for_filtering(dti, removeDiagonal);

    [validIdx, filterInfo] = get_valid_voxel_indices_matlab( ...
        dti, blockSize, removeDiagonal, requireCol);

    % DTI 是体素 x 体素矩阵，因此行列都使用同一组有效体素索引筛选。
    out = data;
    out.dti_net_full = dti(validIdx, validIdx);
    nClean = size(out.dti_net_full, 1);
    if removeDiagonal
        out.dti_net_full(1:nClean + 1:end) = 0;
    end

    % 这些变量是一维体素属性，按体素维度直接筛选。
    vectorFields = ["grey_matter_size", "atlas_region", "voxel_label"];
    for i = 1:numel(vectorFields)
        name = char(vectorFields(i));
        if isfield(out, name)
            out.(name) = filter_voxel_vector(out.(name), validIdx, nVox, name);
        end
    end

    % BOLD 数据可能是 时间 x 体素，也可能是 体素 x 时间；
    % filter_voxel_matrix 会自动识别长度等于 nVox 的那一维。
    boldFields = ["rest_state_bold", "MID_task_bold", "SST_task_bold", "EFT_task_bold"];
    for i = 1:numel(boldFields)
        name = char(boldFields(i));
        if isfield(out, name)
            out.(name) = filter_voxel_matrix(out.(name), validIdx, nVox, name);
        end
    end

    allIdx = (1:nVox).';
    removedIdx = setdiff(allIdx, validIdx, "stable");

    filterInfo.input_file = string(inputFile);
    filterInfo.output_file = string(outputFile);
    filterInfo.source_logic = "normal_generation.py:get_valid_voxel_indices";
    filterInfo.created_at = string(datetime("now", "Format", "yyyy-MM-dd HH:mm:ss"));

    % 同时保存 MATLAB 的 1-based 索引和 Python/NumPy 的 0-based 索引，
    % 方便与 normal_generation.py 的 nonzero_all 对照。
    out.valid_voxel_indices_matlab = validIdx(:);
    out.valid_voxel_indices_zero_based = validIdx(:) - 1;
    out.removed_voxel_indices_matlab = removedIdx(:);
    out.removed_voxel_indices_zero_based = removedIdx(:) - 1;
    out.removed_empty_voxel_indices_matlab = filterInfo.removed_empty_voxel_indices_matlab(:);
    out.removed_isolated_voxel_indices_matlab = filterInfo.removed_isolated_voxel_indices_matlab(:);
    out.filter_info = filterInfo;

    fprintf("Saving cleaned file: %s\n", outputFile);

    % 使用 -v7.3 保存，兼容当前大体积 DTI 矩阵和原始数据格式。
    save(outputFile, "-struct", "out", "-v7.3");

    one = struct( ...
        "n_original", nVox, ...
        "n_after_grey_matter", filterInfo.n_after_grey_matter, ...
        "n_final", numel(validIdx), ...
        "n_removed_empty", numel(filterInfo.removed_empty_voxel_indices_matlab), ...
        "n_removed_isolated", numel(filterInfo.removed_isolated_voxel_indices_matlab), ...
        "iterations", numel(filterInfo.iterations));
end


function dti = prepare_dti_for_filtering(dti, removeDiagonal)
    % 准备 DTI 矩阵：按需去掉自连接，并检查剩余连接权重是否合法。

    if removeDiagonal
        nVox = size(dti, 1);
        dti(1:nVox + 1:end) = 0;
    end

    if any(~isfinite(dti(:)))
        nanCount = nnz(isnan(dti));
        infCount = nnz(isinf(dti));
        error("dti_net_full contains NaN or Inf. nan_count=%d, inf_count=%d", nanCount, infCount);
    end

    if any(dti(:) < 0)
        negCount = nnz(dti < 0);
        error("dti_net_full contains negative values. neg_count=%d", negCount);
    end
end


function [validIdx, info] = get_valid_voxel_indices_matlab(dti, blockSize, removeDiagonal, requireCol)
    % 计算最终保留的原始体素索引。
    % validIdx 是 MATLAB 的 1-based 原始体素索引；保存时会额外给出 0-based 版本。

    if ndims(dti) ~= 2 || size(dti, 1) ~= size(dti, 2)
        error("dti must be a square matrix. Got size [%s]", num2str(size(dti)));
    end

    nVox = size(dti, 1);
    blockSize = double(blockSize(:));

    if numel(blockSize) ~= nVox
        error("blockSize length does not match dti size.");
    end

    if any(~isfinite(blockSize))
        nanCount = nnz(isnan(blockSize));
        infCount = nnz(isinf(blockSize));
        error("blockSize contains NaN or Inf. nan_count=%d, inf_count=%d", nanCount, infCount);
    end

    allIdx = (1:nVox).';
    dtiDiagonal = dti(1:nVox + 1:end).';

    % 第一步：删除灰质体积非正的空体素。
    validGreyMatter = blockSize > 0;
    validIdx = allIdx(validGreyMatter);

    info = struct();
    info.n_original = nVox;
    info.remove_diagonal = removeDiagonal;
    info.require_col = requireCol;
    info.removed_empty_voxel_indices_matlab = allIdx(~validGreyMatter);
    info.removed_empty_voxel_indices_zero_based = info.removed_empty_voxel_indices_matlab - 1;
    info.removed_isolated_voxel_indices_matlab = zeros(0, 1);
    info.removed_isolated_voxel_indices_zero_based = zeros(0, 1);
    info.n_after_grey_matter = numel(validIdx);

    fprintf("After grey matter filtering: %d / %d\n", numel(validIdx), nVox);

    if isempty(validIdx)
        error("No valid voxels remain after grey matter filtering.");
    end

    iteration = 0;
    iterations = struct( ...
        "current_voxels", {}, ...
        "invalid_voxels", {}, ...
        "min_row_sum", {}, ...
        "max_row_sum", {}, ...
        "removed_voxel_indices_matlab", {}, ...
        "removed_voxel_indices_zero_based", {});

    while true
        iteration = iteration + 1;

        % 用 0/1 活动体素向量计算“指向当前剩余子网络”的行和。
        % 这等价于 Python 中 sub_dti = dti[np.ix_(nonzero_all, nonzero_all)]，
        % 但不需要每轮复制一个完整子矩阵，内存压力更小。
        activeWeights = zeros(nVox, 1, "like", dti);
        activeWeights(validIdx) = 1;

        rowSumAll = dti * activeWeights;
        rowSum = rowSumAll(validIdx);

        % 如果调用者传入未清零的 DTI，这里仍会显式扣除自连接贡献。
        if removeDiagonal
            rowSum = rowSum - dtiDiagonal(validIdx);
        end

        % 默认孤立体素定义：当前剩余子网络中的出连接行和为 0。
        valid = isfinite(rowSum) & rowSum > 0;

        if requireCol
            % 可选项：同时要求入连接列和为正。当前默认关闭以匹配 Python 逻辑。
            colSumAll = activeWeights.' * dti;
            colSum = colSumAll(validIdx).';
            if removeDiagonal
                colSum = colSum - dtiDiagonal(validIdx);
            end
            valid = valid & isfinite(colSum) & colSum > 0;
        end

        removedNow = validIdx(~valid);
        invalidCount = numel(removedNow);

        fprintf( ...
            "DTI filtering iteration %d: current voxels=%d, invalid voxels=%d, min row_sum=%g, max row_sum=%g\n", ...
            iteration, numel(validIdx), invalidCount, min(rowSum), max(rowSum));

        iterations(iteration).current_voxels = numel(validIdx);
        iterations(iteration).invalid_voxels = invalidCount;
        iterations(iteration).min_row_sum = min(rowSum);
        iterations(iteration).max_row_sum = max(rowSum);
        iterations(iteration).removed_voxel_indices_matlab = removedNow(:);
        iterations(iteration).removed_voxel_indices_zero_based = removedNow(:) - 1;

        if all(valid)
            break;
        end

        % 将本轮孤立体素从原始索引列表中删除，然后继续下一轮。
        fprintf("Removing isolated MATLAB voxel indices first 50:");
        fprintf(" %d", removedNow(1:min(50, numel(removedNow))));
        fprintf("\n");

        info.removed_isolated_voxel_indices_matlab = [info.removed_isolated_voxel_indices_matlab; removedNow(:)];
        info.removed_isolated_voxel_indices_zero_based = info.removed_isolated_voxel_indices_matlab - 1;

        validIdx = validIdx(valid);

        if isempty(validIdx)
            error("No valid voxels remain after DTI isolated voxel filtering.");
        end
    end

    info.iterations = iterations;
    info.n_final = numel(validIdx);

    fprintf("Final valid voxel count: %d / %d\n", numel(validIdx), nVox);
    fprintf("Final valid MATLAB voxel indices first 100:");
    fprintf(" %d", validIdx(1:min(100, numel(validIdx))));
    fprintf("\n");
end


function y = filter_voxel_vector(x, validIdx, nVox, name)
    % 筛选一维体素变量，并尽量保持原变量的行/列方向。

    if isvector(x) && numel(x) == nVox
        if isrow(x)
            y = x(1, validIdx);
        else
            y = x(validIdx, 1);
        end
        return;
    end

    error("Variable %s is not a voxel vector of length %d. Got size [%s]", ...
        name, nVox, num2str(size(x)));
end


function y = filter_voxel_matrix(x, validIdx, nVox, name)
    % 筛选二维体素相关矩阵，自动判断体素维度在行还是列。

    if size(x, 2) == nVox
        y = x(:, validIdx);
        return;
    end

    if size(x, 1) == nVox
        y = x(validIdx, :);
        return;
    end

    error("Variable %s has no voxel dimension of length %d. Got size [%s]", ...
        name, nVox, num2str(size(x)));
end
