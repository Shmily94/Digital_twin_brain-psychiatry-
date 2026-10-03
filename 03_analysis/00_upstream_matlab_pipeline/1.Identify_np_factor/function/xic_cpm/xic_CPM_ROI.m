

%% edges

function [ROI_square,ROI_degree] = xic_CPM_ROI(all_mats,behav,mask)

   
   if max(mask(:))~=1
    mask = mask/5;
   end
   
   if size(mask,2)<1000
       mask = reshape(mask,[],size(mask,3));
   end
    mask(mask<0.95) =0;mask(mask>0) =1;
        
    
node = sqrt(size(mask,1));        
condi = size(all_mats,3);

y   = behav;   

parfor i=1:node
   
    roi_mats1_all =[];
    ROI_all =[];
    
   for j=1:condi
    mask_tem = mask(:,j);
    all_mats_tem = all_mats(:,:,j);
    
    disp(['ROI---',num2str(i,'%03d'),'--Con--',num2str(j,'%03d')])
    mask_sigle = zeros(node,node);mask_sigle(:,i) = 1; 
    mask_sigle = reshape(mask_sigle,[],1);mask_wight1 = mask_sigle.*mask_tem;
  
    roi_mats1 = all_mats_tem(mask_wight1==1,:);
    roi_mats1_all = [roi_mats1_all;roi_mats1];
   
   end
    
    if size(roi_mats1_all,1)>0
      X = roi_mats1_all';
      lm = fitlm(X,y);  
      [r p] = corr(X,y); r_z = xic_fisherz(r);
       
      if sum(r_z)<0      
          ROI_square(i,1) = lm.Rsquared.Adjusted*(-1);
          ROI_degree(i,1) = size(X,2)*(-1);
      else
          ROI_square(i,1) = lm.Rsquared.Adjusted*(1);
          ROI_degree(i,1) = size(X,2)*(1);
      end
      
    else
      ROI_square(i,1) = 0;  
      ROI_degree(i,1) = 0;
    end
    
   
    
end
   

end
