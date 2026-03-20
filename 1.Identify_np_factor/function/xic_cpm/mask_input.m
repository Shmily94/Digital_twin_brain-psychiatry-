

function pos_mask_final = mask_input(mask_pos_all,size2,size1,nan_mask)


  pos_mask = vertcat(mask_pos_all{:});
  pos_mask = tabulate(pos_mask);
  pos_mask(pos_mask(:,2)==0,:)=[];
  
  pos_mask_index = pos_mask(:,1);
  pos_mask_edge = pos_mask(:,2)/(size(mask_pos_all,1)*size(mask_pos_all,2));
  
  mask  = zeros(1,size2);
  mask(pos_mask_index) = pos_mask_edge;
  
  mask_pos_all = zeros(1,size1);
  mask_pos_all(nan_mask~=0) = mask;
  
  mask_pos_all = reshape(mask_pos_all,sqrt(size1),sqrt(size1));
  
  mask_final = mask_pos_all;
  mask_final_b = rot90(rot90(rot90(flipud(mask_final))));
  
  pos_mask_final = mask_final+mask_final_b;
    
end

