

function pos_mask_final = weight_input(mask_both_r,mask_all_all,size2,size1,nan_mask)

 mask_all  = zeros(1,size1);
 mask_all_to  = zeros(1,size1);
 
 mask_nan  = zeros(1,size2);
  for j = 1:1000
      disp(j)
      for i=1:10
          
        mask = cell2mat(mask_all_all(j,i));        
        r = cell2mat(mask_both_r(j,i));     
     
        mask_nan(mask) = r;
        mask_all(nan_mask~=0) = mask_nan;
        
        mask_all_to = mask_all+ mask_all_to;
          
      end
  end
  pos_mask = mask_all_to/10000; 
  pos_mask = reshape(pos_mask,sqrt(size1),sqrt(size1));
  
  mask_final_b = rot90(rot90(rot90(flipud(pos_mask))));
  
  pos_mask_final = pos_mask+mask_final_b;
end