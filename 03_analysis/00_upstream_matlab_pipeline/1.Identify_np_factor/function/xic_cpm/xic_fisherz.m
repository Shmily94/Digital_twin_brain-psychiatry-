function z = xic_fisherz(r)

%==========================================================================
% This function is used to perform fisher's r-to-z transformation.
%
%
% Syntax: function z = gretna_fishertrans(r)
%
% Input: 
%       r:
%         The correlation coefficients.
%
% Output: 
%       z:
%         The resultant zscores.
%
%==========================================================================



f=@(x) 0.5*log((1+x)./(1-x));
z =  arrayfun(f,r);

return