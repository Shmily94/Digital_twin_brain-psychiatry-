function conn_beta_r(path_folder,subject_conn)

path = path_folder;
subject = ['conn_',subject_conn];

beta_file = 'BETA_Subject001_Condition';
se_file = 'se_Subject001_Condition';

for j = 1:14

file = dir(fullfile(path,subject,[beta_file,num2str(j,'%03d'),'_*']));
efile = dir(fullfile(path,subject,[se_file,num2str(j,'%03d'),'.nii*']));
e_data = y_ReadAll(fullfile(efile.folder,efile.name));

tic

clear subject_condition_z z_file_name
parfor i=1:length(file)
    disp(['beta to z:::',num2str(i)])
    
    beta_subfile = fullfile(file(i).folder,file(i).name);
    data = y_ReadAll(beta_subfile);
    t_data = data./e_data;
    df = 191;
    direction = t_data./abs(t_data);
    k = t_data./sqrt(df);
    r2 = k.^2/1+k.^2;
    r = sqrt(r2).*direction;
    fisher_z = xic_fisherz(r);
    subject_condition_z(:,:,:,i) = fisher_z;
end
toc

z_file = file(1).name; z_file_name = ['MAT_Condition_',num2str(j,'%03d'),'Source01_14.mat'];
z_file_name_path = fullfile(path_folder,subject,z_file_name);

save(z_file_name_path,'subject_condition_z');
end

