

function [mask_nan,mask_clean] = cpm_ev_test_exin(subj,subjects,matrix,phenos,ext_pos_clean)

[~,a,b] = intersect(subj,subjects);
matrix_ph = matrix(a,:);
ph = phenos(b);

mask = reshape(ext_pos_clean,[],1);
[m,n]  =  find(mask>0);

matrix_phed = matrix_ph(:,mask>0);

[r_phed,p_phed] = corr(matrix_phed,ph);

[ev_result]=  EV_test(r_phed,length(ph),-0.1,0.1);

ev_mask = sum(ev_result>0.01,2);

numb = m(ev_mask>0);

% clean

mask_clean = zeros(268,268);

mask_clean(numb) = mask(numb);

% keep

mask(numb)=0;
mask_nan = reshape(mask,268,268);

end