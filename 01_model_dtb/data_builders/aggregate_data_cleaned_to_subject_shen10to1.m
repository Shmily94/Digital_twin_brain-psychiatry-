% Aggregate data_cleaned voxel-level files to subject-specific Shen268
% parent-boundary constrained spatial 10:1 coarse-grained nodes.
%
% Original variable names are preserved in the output where possible so that
% downstream code can load coarse files through the same interface:
%   voxel_label       -> node labels 1..K
%   atlas_region      -> node Shen268 parent parcel
%   grey_matter_size  -> node GMV sum
%   dti_net_full      -> node-to-node DTI sum
%   *_bold            -> original time dimension x node dimension
%
% Inputs:
%   data_cleaned/sub-*_voxel_data_cleaned.mat
%   coarse_grained_shen_cleaned10to1/mappings/sub-*_cleaned10to1_mapping.mat
%
% Outputs:
%   coarse_grained_shen_cleaned10to1/data_cleaned_shen10to1/sub-*_shen10to1_coarse.mat
%   coarse_grained_shen_cleaned10to1/data_cleaned_shen10to1/coarse_graining_summary.csv
%   coarse_grained_shen_cleaned10to1/data_cleaned_shen10to1/coarse_graining_summary.mat

clear;
clc;

thisDir = fileparts(mfilename('fullpath'));
if isempty(thisDir)
    thisDir = pwd;
end

inputDir = fullfile(thisDir, 'data_cleaned');
mappingDir = fullfile(thisDir, 'coarse_grained_shen_cleaned10to1', 'mappings');
outputDir = fullfile(thisDir, 'coarse_grained_shen_cleaned10to1', 'data_cleaned_shen10to1');
if ~isfolder(outputDir)
    mkdir(outputDir);
end

if ~isfolder(mappingDir)
    error('Missing mapping directory: %s. Run make_subject_cleaned_shen10to1_nodes.py first.', mappingDir);
end

files = dir(fullfile(inputDir, 'sub-*_voxel_data_cleaned.mat'));
if isempty(files)
    error('No cleaned files found in %s', inputDir);
end

summary = repmat(struct( ...
    'subject_id', '', ...
    'input_voxels', 0, ...
    'n_nodes', 0, ...
    'mean_node_size', 0, ...
    'min_node_size', 0, ...
    'median_node_size', 0, ...
    'max_node_size', 0, ...
    'dti_nnz_sum', 0, ...
    'output_file', ''), numel(files), 1);

for f = 1:numel(files)
    inputFile = fullfile(files(f).folder, files(f).name);
    subjectId = get_subject_id(files(f).name);
    mappingFile = fullfile(mappingDir, sprintf('%s_cleaned10to1_mapping.mat', subjectId));
    outputFile = fullfile(outputDir, sprintf('%s_shen10to1_coarse.mat', subjectId));

    fprintf('\n[%d/%d] %s\n', f, numel(files), subjectId);
    tStart = tic;

    if ~isfile(mappingFile)
        error('Missing mapping file for %s: %s', subjectId, mappingFile);
    end

    data = load(inputFile);
    mapping = load(mappingFile);

    requiredDataFields = {'voxel_label', 'dti_net_full', 'grey_matter_size'};
    for r = 1:numel(requiredDataFields)
        if ~isfield(data, requiredDataFields{r})
            error('%s must contain %s.', inputFile, requiredDataFields{r});
        end
    end

    requiredMappingFields = { ...
        'cleaned_voxel_label', 'cleaned_voxel_to_node', ...
        'node_id', 'node_shen_parent', 'node_component_id', 'node_size', ...
        'node_centroid_ijk', 'node_min_voxel_label', 'node_max_voxel_label'};
    for r = 1:numel(requiredMappingFields)
        if ~isfield(mapping, requiredMappingFields{r})
            error('%s must contain %s.', mappingFile, requiredMappingFields{r});
        end
    end

    voxelLabel = double(data.voxel_label(:));
    mappedVoxelLabel = double(mapping.cleaned_voxel_label(:));
    if ~isequal(voxelLabel, mappedVoxelLabel)
        error('%s voxel_label order does not match its subject-specific mapping.', subjectId);
    end

    nodeCode = double(mapping.cleaned_voxel_to_node(:));
    node_id = double(mapping.node_id(:));
    node_shen_parent = double(mapping.node_shen_parent(:));
    node_component_id = double(mapping.node_component_id(:));
    node_size = double(mapping.node_size(:));
    node_centroid_ijk = double(mapping.node_centroid_ijk);
    node_min_voxel_label = double(mapping.node_min_voxel_label(:));
    node_max_voxel_label = double(mapping.node_max_voxel_label(:));
    nNodes = numel(node_id);

    if any(nodeCode < 1 | nodeCode > nNodes | nodeCode ~= round(nodeCode))
        error('%s has invalid cleaned_voxel_to_node values.', subjectId);
    end
    if numel(nodeCode) ~= numel(voxelLabel)
        error('%s mapping length does not match voxel_label length.', subjectId);
    end

    if isfield(data, 'atlas_region')
        atlasRegion = round(double(data.atlas_region(:)));
        mappedParent = node_shen_parent(nodeCode);
        mismatch = mappedParent ~= atlasRegion;
        if any(mismatch)
            bad = find(mismatch, 1, 'first');
            error('%s atlas_region mismatch at voxel %d.', subjectId, bad);
        end
    end

    nVox = numel(voxelLabel);
    if size(data.dti_net_full, 1) ~= nVox || size(data.dti_net_full, 2) ~= nVox
        error('%s dti_net_full size does not match voxel_label length.', subjectId);
    end

    M = sparse((1:nVox).', nodeCode(:), 1, nVox, nNodes);
    node_voxel_count = full(sum(M, 1)).';
    if any(node_voxel_count == 0)
        error('%s subject-specific mapping generated empty nodes.', subjectId);
    end
    if any(node_voxel_count ~= node_size)
        error('%s node_size in mapping does not match aggregation matrix counts.', subjectId);
    end

    greyMatter = double(data.grey_matter_size(:));
    grey_matter_sum = full(M.' * greyMatter);
    grey_matter_mean = safe_divide(grey_matter_sum, node_voxel_count);
    grey_matter_size = grey_matter_sum; %#ok<NASGU> compatibility: sum aggregation

    fprintf('  Aggregating DTI (%d voxels -> %d nodes)...\n', nVox, nNodes);
    dtiSparse = sparse(double(data.dti_net_full));
    dti_net_full_sum = full(M.' * dtiSparse * M);
    clear dtiSparse;

    dtiDenom = node_voxel_count * node_voxel_count.';
    dti_net_full_mean = safe_divide(dti_net_full_sum, dtiDenom);
    dti_net_full = dti_net_full_sum; %#ok<NASGU> compatibility: sum aggregation

    rest_state_bold = [];
    MID_task_bold = [];
    SST_task_bold = [];
    EFT_task_bold = [];
    boldFields = {'rest_state_bold', 'MID_task_bold', 'SST_task_bold', 'EFT_task_bold'};
    for b = 1:numel(boldFields)
        name = boldFields{b};
        if isfield(data, name)
            fprintf('  Aggregating %s...\n', name);
            boldNode = aggregate_bold_like_input(data.(name), M, node_voxel_count, nVox, name);
            switch name
                case 'rest_state_bold'
                    rest_state_bold = boldNode; %#ok<NASGU>
                case 'MID_task_bold'
                    MID_task_bold = boldNode; %#ok<NASGU>
                case 'SST_task_bold'
                    SST_task_bold = boldNode; %#ok<NASGU>
                case 'EFT_task_bold'
                    EFT_task_bold = boldNode; %#ok<NASGU>
            end
        end
    end

    voxel_label = node_id; %#ok<NASGU>
    atlas_region = node_shen_parent; %#ok<NASGU>
    if isfield(data, 'uni_region')
        uni_region = double(data.uni_region(:)); %#ok<NASGU>
        missingRegions = setdiff(unique(atlas_region), uni_region);
        if ~isempty(missingRegions)
            error('%s node atlas_region contains regions absent from source uni_region.', subjectId);
        end
    else
        uni_region = unique(atlas_region); %#ok<NASGU>
    end
    if isfield(data, 'is_cortex') && isfield(data, 'uni_region') && numel(data.is_cortex) == numel(data.uni_region)
        is_cortex = logical(data.is_cortex(:)); %#ok<NASGU>
    else
        is_cortex = true(numel(uni_region), 1); %#ok<NASGU>
    end

    valid_voxel_indices_matlab = node_id; %#ok<NASGU>
    valid_voxel_indices_zero_based = node_id - 1; %#ok<NASGU>
    removed_empty_voxel_indices_matlab = zeros(0, 1); %#ok<NASGU>
    removed_isolated_voxel_indices_matlab = zeros(0, 1); %#ok<NASGU>
    removed_voxel_indices_matlab = zeros(0, 1); %#ok<NASGU>
    removed_voxel_indices_zero_based = zeros(0, 1); %#ok<NASGU>

    cleaned_voxel_label = voxelLabel; %#ok<NASGU>
    cleaned_voxel_to_node = nodeCode; %#ok<NASGU>

    coarse_info = struct();
    coarse_info.source_file = inputFile;
    coarse_info.mapping_file = mappingFile;
    coarse_info.node_count = nNodes;
    coarse_info.target_ratio = 10;
    coarse_info.node_definition = 'Subject-specific cleaned-voxel Shen268 parent-boundary constrained spatial-only 10:1 Ward nodes';
    coarse_info.cross_subject_note = 'Node IDs are subject-specific, not a fixed cross-subject atlas. Use node_shen_parent and node_centroid_ijk for anatomical interpretation.';
    coarse_info.dti_net_full = 'sum aggregation: M'' * voxel_DTI * M';
    coarse_info.dti_net_full_mean = 'dti_net_full_sum divided by subject node voxel count outer product';
    coarse_info.bold = 'node-wise voxel mean after cleaned voxel filtering; output preserves the input BOLD orientation with voxel dimension replaced by node dimension';
    coarse_info.gmv = 'grey_matter_size is node GMV sum; grey_matter_mean stores node GMV mean';
    coarse_info.interface_note = 'Original data_cleaned variable names are preserved as node-level variables; voxel_label and valid_voxel_indices now index coarse nodes.';

    if isfield(data, 'filter_info')
        filter_info = data.filter_info; %#ok<NASGU>
    else
        filter_info = struct(); %#ok<NASGU>
    end
    filter_info.coarse_graining = coarse_info; %#ok<STRNU,NASGU>

    varsToSave = { ...
        'subjectId', 'filter_info', 'coarse_info', ...
        'voxel_label', 'atlas_region', 'uni_region', 'is_cortex', ...
        'valid_voxel_indices_matlab', 'valid_voxel_indices_zero_based', ...
        'removed_empty_voxel_indices_matlab', 'removed_isolated_voxel_indices_matlab', ...
        'removed_voxel_indices_matlab', 'removed_voxel_indices_zero_based', ...
        'cleaned_voxel_label', 'cleaned_voxel_to_node', ...
        'node_id', 'node_shen_parent', 'node_component_id', ...
        'node_size', 'node_centroid_ijk', 'node_min_voxel_label', 'node_max_voxel_label', ...
        'node_voxel_count', ...
        'grey_matter_size', 'grey_matter_sum', 'grey_matter_mean', ...
        'dti_net_full', 'dti_net_full_sum', 'dti_net_full_mean'};
    if ~isempty(rest_state_bold); varsToSave{end + 1} = 'rest_state_bold'; end %#ok<AGROW>
    if ~isempty(MID_task_bold); varsToSave{end + 1} = 'MID_task_bold'; end %#ok<AGROW>
    if ~isempty(SST_task_bold); varsToSave{end + 1} = 'SST_task_bold'; end %#ok<AGROW>
    if ~isempty(EFT_task_bold); varsToSave{end + 1} = 'EFT_task_bold'; end %#ok<AGROW>

    save(outputFile, varsToSave{:}, '-v7.3');

    summary(f).subject_id = subjectId;
    summary(f).input_voxels = nVox;
    summary(f).n_nodes = nNodes;
    summary(f).mean_node_size = mean(node_voxel_count);
    summary(f).min_node_size = min(node_voxel_count);
    summary(f).median_node_size = median(node_voxel_count);
    summary(f).max_node_size = max(node_voxel_count);
    summary(f).dti_nnz_sum = nnz(dti_net_full_sum);
    summary(f).output_file = outputFile;

    fprintf('  Nodes: %d, mean node size %.3f, DTI nnz %d, elapsed %.1fs\n', ...
        nNodes, summary(f).mean_node_size, summary(f).dti_nnz_sum, toc(tStart));

    clear data mapping M dti_net_full dti_net_full_sum dti_net_full_mean ...
        rest_state_bold MID_task_bold SST_task_bold EFT_task_bold;
end

summaryTable = struct2table(summary);
writetable(summaryTable, fullfile(outputDir, 'coarse_graining_summary.csv'));
save(fullfile(outputDir, 'coarse_graining_summary.mat'), 'summary', 'summaryTable', '-v7.3');

fprintf('\nSaved subject-specific 10:1 coarse-grained files to %s\n', outputDir);


function subjectId = get_subject_id(fileName)
    token = regexp(fileName, '(sub-\d+)', 'match', 'once');
    if isempty(token)
        error('Cannot parse subject id from %s', fileName);
    end
    subjectId = token;
end


function boldNode = aggregate_bold_like_input(rawBold, M, node_voxel_count, nVox, name)
    if size(rawBold, 2) == nVox
        boldNode = double(rawBold) * M;
        boldNode = safe_divide(boldNode, node_voxel_count.');
    elseif size(rawBold, 1) == nVox
        boldNode = M.' * double(rawBold);
        boldNode = safe_divide(boldNode, node_voxel_count);
    else
        error('%s has no voxel dimension of length %d. Actual size [%s].', ...
            name, nVox, num2str(size(rawBold)));
    end
end


function out = safe_divide(numer, denom)
    out = zeros(size(numer));
    if isvector(denom) && size(numer, 1) == numel(denom)
        denom = denom(:);
        valid = denom > 0;
        out(valid, :) = bsxfun(@rdivide, numer(valid, :), denom(valid));
    elseif isvector(denom) && size(numer, 2) == numel(denom)
        denom = denom(:).';
        valid = denom > 0;
        out(:, valid) = bsxfun(@rdivide, numer(:, valid), denom(valid));
    else
        valid = denom > 0;
        out(valid) = numer(valid) ./ denom(valid);
    end
end
