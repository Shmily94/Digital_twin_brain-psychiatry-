

function all_mats = cpm_reshape(all_mats)

nan_mask = all_mats(:,:,1);
nan_mask = reshape(tril(nan_mask,-1),[],1);

size1 = length(nan_mask);

no_sub = size(all_mats,3);


nfold =10;

all_mats = reshape(all_mats,[],size(all_mats,3))';
all_mats(:,nan_mask==0)=[];