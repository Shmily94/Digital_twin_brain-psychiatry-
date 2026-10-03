
function [a,b] = polyfit_xic(x,y)

    [a,b] = polyfit(x{:}',y{:}',1);
    
end
