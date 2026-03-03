
idx=find(x(:,1)==0);
idx2=find(x(:,1)~=0);

non_np_region=x(idx,2:end);
np_region=x(idx2,2:end);


p = zeros(1,39);
t = zeros(1,39);

for i = 1:39
    [~, p(i), ~, stats] = ttest2(non_np_region(:,i), np_region(:,i), 'Vartype','unequal');
    t(i) = stats.tstat;
end

q = mafdr(p, 'BHFDR', true);
alpha=0.05;
h_fdr=q<alpha;
find(h_fdr==1)+2;

d = zeros(1,39);
for i = 1:39
    m1 = mean(non_np_region(:,i));
    m2 = mean(np_region(:,i));
    s1 = var(non_np_region(:,i));
    s2 = var(np_region(:,i));
    
    sp = sqrt((s1 + s2)/2);   % 非严格 pooled，但在 Welch 框架下可接受
    d(i) = (m1 - m2) / sp;
end