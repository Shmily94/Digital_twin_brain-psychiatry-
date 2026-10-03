####Start fiber tracking
for name in $(ls /data_path/DTI/Preprocessed)
do
mkdir -p /data_path/DTI/fiber_tracking/${name}
cd /data_path/DTI/fiber_tracking/${name}

#1. FOD construction
mrconvert /data_path/DTI/Preprocessed/${name}/preprocessed_dwi.nii.gz -fslgrad /data_path/DTI/Preprocessed/${name}/eddy_rotated_bvecs.bvec /data_path/DTI/Preprocessed/${name}/dwi.bval Preprocessed_DWI.mif -force
dwiextract Preprocessed_DWI.mif - -bzero | mrmath - mean meanb0.nii.gz -axis 3 -force
bet meanb0 meanb0_brain -f 0.3 -m
dwi2response tournier Preprocessed_DWI.mif RF_WM.txt -voxels RF_voxels.mif -mask meanb0_brain_mask.nii.gz -force -nthreads 10
dwi2fod csd Preprocessed_DWI.mif RF_WM.txt WM_FODs.mif -mask meanb0_brain_mask.nii.gz -force -nthreads 10

#2. fiber tracking
#T12DWI
cp /data_path/Func_Prep/fmriprep/sub-${name}/anat/sub-${name}_desc-brain_mask.nii.gz T1_brain_mask.nii.gz
cp /data_path/Func_Prep/fmriprep/sub-${name}/anat/sub-${name}_desc-preproc_T1w.nii.gz T1.nii.gz
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
flirt -ref /data_path/Code/MNI152_T1_3mm_brain.nii.gz -in T12DWI.nii.gz -omat T12MNI_affine.mat
fnirt --ref=/data_path/Code/MNI152_T1_3mm_brain.nii.gz --in=T12DWI.nii.gz --aff=T12MNI_affine.mat --cout=warps_T12MNI
invwarp --ref=T12DWI.nii.gz --warp=warps_T12MNI --out=warps_MNI2T1
#tcktransform from DWI to MNI
warpinit /data_path/Code/MNI152_T1_3mm_brain.nii.gz inv_identity_warp_no.nii -force
applywarp --ref=T12DWI.nii.gz --in=inv_identity_warp_no.nii --warp=warps_MNI2T1.nii.gz --out=mrtrix_warp_MNI2DWI.nii.gz
mrtransform /data_path/Code/MNI152_T1_3mm_brain.nii.gz -warp mrtrix_warp_MNI2DWI.nii.gz MNI2DWI.nii.gz -nthreads 10 -force
tcktransform ACT_50M.tck mrtrix_warp_MNI2DWI.nii.gz tck2MNI.tck -force -nthreads 10
#check registration
tckmap tck2MNI.tck tck2MNI.nii -template /data_path/Code/MNI152_T1_3mm_brain.nii.gz -force -nthreads 10

#4. connectome of construction
tck2connectome tck2MNI.tck /data_path/Code/MNI152_T1_3mm_gmwmi_shen268_label.nii.gz voxel_connectome.csv -force -nthreads 10

#5. copy results
cp voxel_connectome.csv /data_path/DTI/connectome/${name}_voxel_connectome.csv
done

#data_description
/data_path/Code/MNI152_T1_3mm_gmwmi_shen268_label.nii.gz -- A mask comprising voxels located at the gray–white matter boundary of the MNI152 template and also included in the Shen268 functional parcellation
/data_path/DTI/fiber_tracking -- processing folder
/data_path/DTI/connectome/${name}_voxel_connectome.csv -- the resulting voxel-wise structure connectome
/data_path/DTI/connectome/000000112288_voxel_connectome.csv -- demo
