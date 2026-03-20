

function EV_result = EV_test(R,DF, Lower_Bound, Upper_Bound)


  Z = xic_fisherz(R); %Z transformed R
  LB_Z =xic_fisherz(Lower_Bound);
  UB_Z = xic_fisherz(Upper_Bound);
  SD = 1/sqrt(DF-3);
 
  D_Lower = Z-LB_Z;  % Cohen's D for Lower_Bound
  D_Upper = UB_Z-Z ; % Cohen's D for Upper_Bound
  
  P_Lower = 1-cdf('Normal',D_Lower/SD,0,1);%#P-value for the lower boundary, must be significant to claim an equivalence
  P_Upper = 1-cdf('Normal',D_Upper/SD,0,1);% #P-value for the upper boundary, must be significant to claim an equivalence
  
  EV_result = [P_Lower,P_Upper];
  
end