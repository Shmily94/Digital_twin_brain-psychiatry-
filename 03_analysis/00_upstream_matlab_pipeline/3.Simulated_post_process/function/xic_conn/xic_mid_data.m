function [sub_antici_hit,sub_feed_hit,sub_feed_miss,sub_mid_subject] = xic_mid_data(files)


sub_antici_hit = zeros(268,268,length(files));
sub_feed_hit = zeros(268,268,length(files));
sub_feed_miss = zeros(268,268,length(files));


for i=1:length(files)
   try
   
    disp(['Subject',num2str(i,'%05d')]);

    sub_files = dir(fullfile(files(i).folder,files(i).name,'res*'));
    names = importdata(fullfile(files(i).folder,files(i).name,'_list_conditions.txt'));

    clear feed_large_win feed_small_win feed_no_win ...
          feed_miss_large_win feed_miss_small_win feed_miss_no_win ...
          anticip_large_win anticip_small_win anticip_no_win
      
    for j=1:length(names)

        name = names{j};
        name = split(name);name = name{3};
        % feedback
        feed_large_win(j) = strcmp(name,'Feedback_Hit_BIG_WIN');
        feed_small_win(j) = strcmp(name,'Feedback_Hit_SMALL_WIN');
        feed_no_win(j) = strcmp(name,'Feedback_Hit_NO_WIN');
        
        % feedback miss
        feed_miss_large_win(j) = strcmp(name,'Feedback_Miss_BIG_WIN');
        feed_miss_small_win(j) = strcmp(name,'Feedback_Miss_SMALL_WIN');
        feed_miss_no_win(j) = strcmp(name,'Feedback_Miss_NO_WIN');
        
        % anticip hit
        anticip_large_win(j) = strcmp(name,'Anti_Hit_BIG_WIN');
        anticip_small_win(j) = strcmp(name,'Anti_Hit_SMALL_WIN');
        anticip_no_win(j) = strcmp(name,'Anti_Hit_NO_WIN');
    end
    
    
    %% antici hit
try
if sum(anticip_large_win)~=0
    number = find(anticip_large_win~=0);
    data = load(fullfile(sub_files(number).folder,sub_files(number).name));
    antici_hit_large = data.Z(:,1:268);
end

if sum(anticip_small_win)~=0
    number = find(anticip_small_win~=0);
    data = load(fullfile(sub_files(number).folder,sub_files(number).name));
    antici_hit_small = data.Z(:,1:268);
end

if sum(anticip_no_win)~=0
    number = find(anticip_no_win~=0);
    data = load(fullfile(sub_files(number).folder,sub_files(number).name));
    antici_hit_no = data.Z(:,1:268);
end

    antici_hit = mean(cat(3,antici_hit_large,antici_hit_small,antici_hit_no),3);
    sub_antici_hit(:,:,i) = antici_hit;
    subject = files(i).name;    
    subject =str2double(subject(11:end));
    antici_hit_subject(i) = subject;     
 
catch
     wrong_antici_subject(i) = i;
end
    
    %%  feedback hit
try
if sum(feed_large_win)~=0
    number = find(feed_large_win~=0);
    data = load(fullfile(sub_files(number).folder,sub_files(number).name));
    feedback_hit_large = data.Z(:,1:268);
end

if sum(feed_small_win)~=0
    number = find(feed_small_win~=0);
    data = load(fullfile(sub_files(number).folder,sub_files(number).name));
    feedback_hit_small = data.Z(:,1:268);
end

if sum(feed_no_win)~=0
    number = find(feed_no_win~=0);
    data = load(fullfile(sub_files(number).folder,sub_files(number).name));
    feedback_hit_no = data.Z(:,1:268);
end

    feed_hit = mean(cat(3,feedback_hit_large,feedback_hit_small,feedback_hit_no),3);
    sub_feed_hit(:,:,i) = feed_hit;
    subject = files(i).name;    
    subject = str2double(subject(11:end));
    feed_hit_subject(i) = subject;
    
catch
    wrong_feed_hit_subject(i) = i;
end       


    %%  feedback miss

 try
if sum(feed_miss_large_win)~=0
    number = find(feed_miss_large_win~=0);
    data = load(fullfile(sub_files(number).folder,sub_files(number).name));
    feed_miss_large = data.Z(:,1:268);
end

if sum(feed_miss_small_win)~=0
    number = find(feed_miss_small_win~=0);
    data = load(fullfile(sub_files(number).folder,sub_files(number).name));
    feed_miss_small = data.Z(:,1:268);
end

if sum(feed_miss_no_win)~=0
    number = find(feed_miss_no_win~=0);
    data = load(fullfile(sub_files(number).folder,sub_files(number).name));
    feed_miss_no = data.Z(:,1:268);
end

    feed_miss = mean(cat(3,feed_miss_large,feed_miss_small,feed_miss_no),3);
    sub_feed_miss(:,:,i) = feed_miss;
    
    subject = files(i).name;    
    subject =str2double(subject(11:end));
    feed_miss_subject(i) = subject;
    
 catch
    wrong_feed_miss_subject(i) = i;
 end 
   end

  save(num2str(subject), 'antici_hit', 'feed_hit', 'feed_miss') 

end

sub_antici_hit(:,:,antici_hit_subject==0)=[];
antici_hit_subject(antici_hit_subject==0)=[];

sub_feed_hit(:,:,feed_hit_subject==0)=[];
feed_hit_subject(feed_hit_subject==0)=[];

sub_feed_miss(:,:,feed_miss_subject==0)=[];
feed_miss_subject(feed_miss_subject==0)=[];

[sub_mid_subject,ind1,ind2,ind3] = xic_intersect(antici_hit_subject,feed_hit_subject,feed_miss_subject);
sub_antici_hit = sub_antici_hit(:,:,ind1);
sub_feed_hit = sub_feed_hit(:,:,ind2);
sub_feed_miss = sub_feed_miss(:,:,ind3);

