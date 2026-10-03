

function [network_num,network_size] = xic_cpm_matrix(data)

load('/share/home1/xic_fdu/project/IMAGEN_Develop_diagnostic/shen_net.mat')
load('/share/home1/xic_fdu/project/IMAGEN_Develop_diagnostic/Matrix_plot/Cog_MyColormaps.mat')
load('/share/home1/xic_fdu/project/IMAGEN_Develop_diagnostic/Matrix_plot/MyColormaps.mat')
close all 

figure(1)
set(0,'DefaultFigureVisible', 'on');
imagesc(data,[1 7]);


number = 0;
colormap(mymap_cog)

for j =1:13
        hold on;
    number = sum(shen_net_num==j)+number;    
       
    plot([0,length(shen_net_num)],[number+0.5,number+0.5],'w','LineWidth',0.8)
    plot([number+0.5,number+0.5],[0,length(shen_net_num)],'w','LineWidth',0.8)
  
end

xticklabels([])
yticklabels([])


%% data

clear network_num
for j =1:13
      for i =1:13
          
          network1 = (shen_net_num==j);
          network2 = (shen_net_num==i);
         
       
          network_data = data(network1,network2);
           
          if i==j
          network_size(i,j) = (size(network_data,1)*size(network_data,2)-size(network_data,2))/2;
          network_num(i,j) = sum(network_data(:))/2;
          else
          network_size(i,j) = size(network_data,1)*size(network_data,2);
          network_num(i,j) = sum(network_data(:)); 
          end
      end
end


figure(2)

% set(0,'DefaultFigureVisible', 'off');
imagesc(network_num);

number = 0;
colormap(mycmap);
colorbar

for j =1:13
        hold on;
       number = j+0.5;
       
    plot([0,14],[number,number],'color',[180 180 180]/255,'LineWidth',0.8)
    plot([number,number],[0,14],'color',[180 180 180]/255,'LineWidth',0.8)
  
end
xticklabels([])
yticklabels([])

% 
% 
figure(3)
imagesc(sum(network_num));
% 
number = 0;
colormap(mycmap);
colorbar

for j =1:13
        hold on;
       number = j+0.5;
       
%     plot([0,14],[number,number],'color',[180 180 180]/255,'LineWidth',0.8)
    plot([number,number],[0,14],'color',[180 180 180]/255,'LineWidth',0.8)
  
end
xticklabels([])
yticklabels([])
end