clear;clc

sub=dir('sub*');

% extract func bold signal
maskfile=('MNI152_T1_3mm_gmwmi_shen268_label.nii');
mask=load_nii(maskfile);
img=mask.img;
for i=1:17392
idx(1,i)=find(img==i); %change the order
end

Func_bold_all=cell(4,4);
for i=1:4
 filepath=sub(i).name;  
  for j=1:4
    task=task_id{j};
    Fun_file=dir(fullfile(filepath,['*',task,'*nii','*']));
    Fun_indi_file=load_nii([Fun_file.folder,'/',Fun_file.name]);
    Fun_indi_vol = Fun_indi_file.img;
    Func_bold_indi=zeros(size(Fun_indi_vol,4),17392);
      for n=1:size(Fun_indi_vol,4)
       A=Fun_indi_vol(:,:,:,n);
       mask_ts=A(idx); % zilin order  
       Func_bold_indi(n,:)=mask_ts;
      end
    Func_bold_all{i,j}=Func_bold_indi;
  end
end
filename = [sub(i).name, '_bold.mat'];   
Func_bold = Func_bold_all(i,:);          
save(filename, 'Func_bold');        

% extract gmv

for i=1:4
  filepath=sub(i).name;  
  gmv_file=dir(fullfile(filepath,['sm0wrp','*']));
  new_gmv_file=fullfile(gmv_file.folder,['reslice_',gmv_file.name]); % resliece gmv file
  reslice_nii(fullfile(gmv_file.folder,gmv_file.name), new_gmv_file, [3,3,3], 'nearest')
end

maskfile=('MNI152_T1_3mm_gmwmi_shen268_label.nii');
mask=load_nii(maskfile);
img=mask.img;
for i=1:4
 filepath=sub(i).name;  
 gmv_file=dir(fullfile(filepath,['reslice','*']));
 gmv_data=load_nii(fullfile(gmv_file.folder,gmv_file.name));
 gm_vol = gmv_data.img;
   for j=1:17392
    gmv_indi(1,j)=gm_vol(img==j);
   end
 save([filepath,'_gmv.mat'],'gmv_indi')
end

