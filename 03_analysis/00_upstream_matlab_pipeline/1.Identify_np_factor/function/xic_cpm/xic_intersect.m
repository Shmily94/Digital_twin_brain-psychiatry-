


function [all,ind1,ind2,ind3] = xic_intersect(a,b,c)

    [all] = intersect(a,intersect(b,c));
    [~,ind1] = intersect(a,all);
    [~,ind2] = intersect(b,all);
    [~,ind3] = intersect(c,all);
    

end