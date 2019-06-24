import nibabel as nib
import numpy as np
#extract special fiber probability atlas from standard atlas,JHU-ICBM-tracts-prob-2mm.nii.gz.

#extract

def extract_volume(proatlas_data,volume,threshold=0):

    coordinate_shape = proatlas_data.shape[:3]
    extract_atlas = np.zeros(coordinate_shape)

    for i in range(proatlas_data.shape[0]):
        for j in range(proatlas_data.shape[1]):
            for k in range(proatlas_data.shape[2]):
                if proatlas_data[i][j][k][volume] > threshold :
                    extract_atlas[i][j][k] = proatlas_data[i][j][k][volume]

    return extract_atlas


#extract special fiber probability atlas from standard atlas,JHU-ICBM-tracts-prob-2mm.nii.gz.

#extract
pro_atlas_path = '/nfs/s2/userhome/quyukun/workingdir/fiberdata/subjects/100206/prob_atlas/100206_JHU_tract_prob.nii.gz'
output_name = '/nfs/s2/userhome/quyukun/workingdir/fiberdata//subjects/100206/prob_atlas/100206_FP_prob.nii.gz'

proatlas = nib.load(pro_atlas_path)
affine = proatlas.affine

proatlas_data = proatlas.get_data()
extract_atlas = extract_volume(proatlas_data,8)

#save as Nifti
dm_img = nib.Nifti1Image(extract_atlas,affine)
dm_img.to_filename(output_name)




