function g = buildGroup(x,dataset,mask)
N =size(x,3);
subjects(1,N) = subject(N);
for i=1:N
    subjects(i) = subject(x(:,:,i,:),i,dataset,mask);
end
g = group(subjects);
end
