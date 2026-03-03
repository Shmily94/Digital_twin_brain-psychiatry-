network_fu3=zeros(11,11);
for i=1:length(FC_ind_fu3)
[m,n]=find(mask_all==FC_ind_fu3(i));
net_label1=network_idx(m);
net_label2=network_idx(n);
network_fu3(net_label1,net_label2)=network_fu3(net_label1,net_label2)+1;
end
filename='net_fu3.txt';
save(filename, 'network_fu3', '-ascii');

sum(sum(network_fu3));