####Start fiber tracking
for name in $(ls /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/Preprocessed)
###这里可以把$(ls /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/Preprocessed)替换成需要跑的被试名单，空格间隔
do
mkdir -p /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/fiber_tracking/${name}
cd /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/fiber_tracking/${name}

#1. FOD construction
mrconvert /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/Preprocessed/${name}/preprocessed_dwi.nii.gz -fslgrad /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/Preprocessed/${name}/eddy_rotated_bvecs.bvec /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/Preprocessed/${name}/dwi.bval Preprocessed_DWI.mif -force
dwiextract Preprocessed_DWI.mif - -bzero | mrmath - mean meanb0.nii.gz -axis 3 -force
bet meanb0 meanb0_brain -f 0.3 -m
dwi2response tournier Preprocessed_DWI.mif RF_WM.txt -voxels RF_voxels.mif -mask meanb0_brain_mask.nii.gz -force -nthreads 10
dwi2fod csd Preprocessed_DWI.mif RF_WM.txt WM_FODs.mif -mask meanb0_brain_mask.nii.gz -force -nthreads 10

#2. fiber tracking
#T12DWI
cp /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/Func_Prep/fmriprep/sub-${name}/anat/sub-${name}_desc-brain_mask.nii.gz T1_brain_mask.nii.gz
cp /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/Func_Prep/fmriprep/sub-${name}/anat/sub-${name}_desc-preproc_T1w.nii.gz T1.nii.gz
fslmaths T1.nii.gz -mul T1_brain_mask.nii.gz T1_brain.nii.gz
flirt -ref meanb0_brain.nii.gz -in T1_brain.nii.gz -omat T12DWI_affine.mat -o T12DWI.nii.gz -noresample
#5ttgen
5ttgen fsl T12DWI.nii.gz 5tt2DWI.nii.gz -sgm_amyg_hipp -premasked -nocrop -force -nthreads 10
5tt2gmwmi 5tt2DWI.nii.gz gmwmi.nii.gz -force
#tckgen
mrinfo Preprocessed_DWI.mif -export_grad_fsl DWI.bvec DWI.bval -force
tckgen WM_FODs.mif ACT_50M.tck -algorithm iFOD2 -fslgrad DWI.bvec DWI.bval -minlength 3 -maxlength 250 -angle 45 -step 0.2 -cutoff 0.05 -seed_gmwmi gmwmi.nii.gz -act 5tt2DWI.nii.gz -backtrack -crop_at_gmwmi -force -select 50M -nthreads 10


#3. tracks transform from DWI to MNI space
#warps from DWI to MNI
flirt -ref /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/Code/MNI152_T1_3mm_brain.nii.gz -in T12DWI.nii.gz -omat T12MNI_affine.mat
fnirt --ref=/share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/Code/MNI152_T1_3mm_brain.nii.gz --in=T12DWI.nii.gz --aff=T12MNI_affine.mat --cout=warps_T12MNI
invwarp --ref=T12DWI.nii.gz --warp=warps_T12MNI --out=warps_MNI2T1
#tcktransform from DWI to MNI
warpinit /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/Code/MNI152_T1_3mm_brain.nii.gz inv_identity_warp_no.nii -force
applywarp --ref=T12DWI.nii.gz --in=inv_identity_warp_no.nii --warp=warps_MNI2T1.nii.gz --out=mrtrix_warp_MNI2DWI.nii.gz
mrtransform /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/Code/MNI152_T1_3mm_brain.nii.gz -warp mrtrix_warp_MNI2DWI.nii.gz MNI2DWI.nii.gz -nthreads 10 -force
tcktransform ACT_50M.tck mrtrix_warp_MNI2DWI.nii.gz tck2MNI.tck -force -nthreads 10
#check registration
tckmap tck2MNI.tck tck2MNI.nii -template /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/Code/MNI152_T1_3mm_brain.nii.gz -force -nthreads 10

#4. connectome of AAL construction
tck2connectome tck2MNI.tck /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/Code/MNI3mm_gmwmi_bin_AAL_label.nii.gz AAL_voxel_connectome.csv -force -nthreads 10

#5. copy results
cp AAL_voxel_connectome.csv /share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/AAL_connectome/${name}_AAL_voxel_connectome.csv
done





#文件说明
/share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/Code/MNI3mm_gmwmi_bin_AAL_label.nii.gz -- MNI brain的灰白质交界*AAL，对每个体素标记后的模板
/share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/AAL_connectome/${name}_AAL_voxel_connectome.csv -- 基于体素标记模板构建纤维追踪得到的条数矩阵
/share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/fiber_tracking -- 每个被试的纤维追踪中间生成的数据存储于此
/share/inspurStorage/home1/ISTBI_data/IMAGEN_FU3/DTI/AAL_connectome/000000112288_AAL_voxel_connectome.csv -- 示例
