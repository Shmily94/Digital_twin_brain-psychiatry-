function [EFT_neutral,EFT_angry,sub_eft_subject] = xic_eft_data_BL(files)


EFT_neutral = zeros(268,268,length(files));
EFT_angry = zeros(268,268,length(files));
% EFT_happy = zeros(268,268,length(files));
% EFT_control = zeros(268,268,length(files));

for j=1:length(files)

    try
disp(['Subject::   ',num2str(j,'%04d')])
    
files_mat = dir(fullfile(files(j).folder,files(j).name,'res*'));

names = importdata(fullfile(files(j).folder,files(j).name,'_list_conditions.txt'));

clear angry_number  neutral_number happy_number

for i=1:length(names)

    name = string(names{i});
    angry_number(i) = contains(name,'faces_a');
    neutral_number(i) = contains(name,'faces_n');

%     happy_number(i) = strcmp(emotion,'h'); 
end



% % control
% number = find(control_number~=0);
% 
% clear control
% for i=1:length(number)
%     data = load(fullfile(files_mat(number(i)).folder,files_mat(number(i)).name));
%     control(:,:,i) = data.Z(:,1:268);
%    
% end
% 
% EFT_control(:,:,j) = mean(control,3);
% 
% subject = files(j).name;subject = str2double(subject(6:end));
% control_subject(j) = subject; 


% neutral
number = find(neutral_number~=0);

clear neutral
for i=1:length(number)
    data = load(fullfile(files_mat(number(i)).folder,files_mat(number(i)).name));
    neutral(:,:,i) = data.Z(:,1:268);
   
end

EFT_neutral(:,:,j) = mean(neutral,3);

subject = files(j).name;subject =str2double(subject(10:end));
neutral_subject(j) = subject; 

% angry
number = find(angry_number~=0);

clear angry

for i=1:length(number)
    data = load(fullfile(files_mat(number(i)).folder,files_mat(number(i)).name));
    angry(:,:,i) = data.Z(:,1:268);
   
end


EFT_angry(:,:,j) = mean(angry,3);

subject = files(j).name;subject =str2double(subject(10:end));
angry_subject(j) = subject; 



% happy
% 
% clear happy
% number = find(happy_number~=0);
% 
% for i=1:length(number)
%     data = load(fullfile(files_mat(number(i)).folder,files_mat(number(i)).name));
%     happy(:,:,i) = data.Z(:,1:268);
%    
% end
% 
% EFT_happy(:,:,j) = mean(happy,3);
% 
% subject = files(j).name;subject =str2double(subject(6:end));
% happy_subject(j) = subject; 
% 
% catch
%    wrong_subject(j) = j; 
% end

    end

end

EFT_angry(:,:,angry_subject==0)=[];
angry_subject(angry_subject==0)=[];

EFT_neutral(:,:,neutral_subject==0)=[];
neutral_subject(neutral_subject==0)=[];

% EFT_happy(:,:,happy_subject==0)=[];  
% happy_subject(happy_subject==0)=[];

[sub_eft_subject,ind1,ind2] = intersect(angry_subject,neutral_subject);
EFT_angry = EFT_angry(:,:,ind1);
EFT_neutral = EFT_neutral(:,:,ind2);


