
function [go_wrong, stop_suces, stop_failure, sub_sst_subject] = xic_sst_data2(files)

go_wrong = zeros(217,217,length(files));
stop_suces = zeros(217,217,length(files));
stop_failure = zeros(217,217,length(files));



for j=1:length(files) 

try
  
disp(['Subject::   ',num2str(j,'%04d')])   
files_mat = dir(fullfile(files(j).folder,files(j).name,'res*'));
names = importdata(fullfile(files(j).folder,files(j).name,'_list_conditions.txt'));
    for i=1:length(names)
    name = names{i};
    name = split(name);name = name{3};
    go_wrong_number(i) = strcmp(name,'GO_SUCCESS');
    stop_suces_number(i) = strcmp(name,'STOP_SUCCESS');
    stop_failure_number(i) = strcmp(name,'STOP_FAILURE');
    end
catch
end

% go wrong
try
    if sum(go_wrong_number)~=0
    number = find(go_wrong_number~=0);
    data = load(fullfile(files_mat(number).folder,files_mat(number).name));
    go_wrong_indi=data.Z(:,1:217);
    go_wrong(:,:,j) = go_wrong_indi;  

    subject = files(j).name;
    % subject =str2double(subject(34:35));
    go_wrong_subject{j} = subject; 
    end
catch
       wrong_go_wrong_subject(j) = j; 
end


% stop_suces
try
if sum(stop_suces_number)~=0
    number = find(stop_suces_number~=0);
    data = load(fullfile(files_mat(number).folder,files_mat(number).name));
    stop_suces_indi=data.Z(:,1:217);
    stop_suces(:,:,j) = stop_suces_indi;   

    subject = files(j).name;
    % subject =str2double(subject(34:35));
    stop_suces_subject{j} = subject; 
end
 catch
       wrong_stop_suces_subject(j) = j; 
 end

% stop_failure_
try
if sum(stop_failure_number)~=0
   number = find(stop_failure_number~=0);
   data = load(fullfile(files_mat(number).folder,files_mat(number).name));
   stop_failure_indi=data.Z(:,1:217);
   stop_failure(:,:,j) = stop_failure_indi;   

   subject = files(j).name;
   % subject =str2double(subject(34:35));
   stop_failure_subject{j} = subject; 
end
    catch
       wrong_stop_fail_subject(j) = j; 
end
% save(num2str(subject),'stop_failure_indi','stop_suces_indi','go_wrong_indi')
end

% go_wrong(:,:,go_wrong_subject==0)=[];
% go_wrong_subject(go_wrong_subject==0)=[];
% 
% stop_suces(:,:,stop_suces_subject==0)=[];
% stop_suces_subject(stop_suces_subject==0)=[];
% 
% stop_failure(:,:,stop_failure_subject==0)=[];
% stop_failure_subject(stop_failure_subject==0)=[];
 sub_sst_subject = go_wrong_subject;
% [sub_sst_subject,ind1,ind2,ind3] = xic_intersect(go_wrong_subject,stop_suces_subject,stop_failure_subject);
% 
% go_wrong = go_wrong(:,:,ind1);
% stop_suces = stop_suces(:,:,ind2);
% stop_failure = stop_failure(:,:,ind3);


                   
                
   