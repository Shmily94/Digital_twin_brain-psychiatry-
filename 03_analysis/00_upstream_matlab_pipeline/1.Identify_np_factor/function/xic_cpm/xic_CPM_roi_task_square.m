


%% edges

function [ROI_square] = xic_CPM_roi_square(data_all,behav,mask)

    
 
  
parfor i=1:sqrt(size(all_mats_all,2))
    
    disp(['ROI',num2str(i,'%03d')])
    
    mask_sigle = zeros(sqrt(size(all_mats_all,2)),sqrt(size(all_mats_all,2)));
    mask_sigle(:,i) = 1; mask_wight1 = mask_sigle.*mask_template_use1;
    mask_wight1 = reshape(mask_wight1,[],1);
  
    mask_sigle = zeros(sqrt(size(all_mats_all,2)),sqrt(size(all_mats_all,2)));
    mask_sigle(:,i) = 1; mask_wight2 = mask_sigle.*mask_template_use2;
    mask_wight2 = reshape(mask_wight2,[],1);
  
    mask_sigle = zeros(sqrt(size(all_mats_all,2)),sqrt(size(all_mats_all,2)));
    mask_sigle(:,i) = 1; mask_wight3 = mask_sigle.*mask_template_use3;
    mask_wight3 = reshape(mask_wight3,[],1);
  
    roi_mats1 = all_mats_all(:,mask_wight1==1,1); 
    roi_mats2 = all_mats_all(:,mask_wight2==1,2);
    roi_mats3 = all_mats_all(:,mask_wight3==1,3);
    %% roi
          
    X   = [roi_mats1,roi_mats2,roi_mats3];
    y   = all_behav;

    lm = fitlm(X,y);

    ROI_square(i,1) = lm.Rsquared.Adjusted;

end

end

