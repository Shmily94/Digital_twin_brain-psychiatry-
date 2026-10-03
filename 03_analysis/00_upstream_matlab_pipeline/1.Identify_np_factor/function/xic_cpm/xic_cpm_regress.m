
function [Residual]= xic_cpm_regress(Data,Cov)

PM = eye(size(Cov,1)) - Cov*(inv(Cov'*Cov))*Cov';

Residual = PM*Data;

end