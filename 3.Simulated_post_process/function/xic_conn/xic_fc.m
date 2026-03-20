
function ts = xic_fc(rest_dat,template)
    
    rois = unique(template);
    rois(rois==0)=[];
    rest_data = reshape(rest_dat,[],size(rest_dat,4));
    
    for i=1:length(rois)
       ts(:,i) = mean(rest_data(template==rois(i),:))';
    end
end