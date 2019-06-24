# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np

with open('/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id', 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

print sessid

# extract
pre_roi_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                 'response_dhollander/subjects/{subjects_id}/ROI'
rois_name = ['cytoMPM_thr25_2mm_hOc1.nii.gz', 'cytoMPM_thr25_2mm_hOc2.nii.gz',
             'cytoMPM_thr25_2mm_hOc3d.nii.gz', 'cytoMPM_thr25_2mm_hOc3v.nii.gz']
output_name = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
              'response_dhollander/subjects/{subjects_id}/ROI/cytoMPM_thr25_2mm_vis.nii.gz'
value = [85, 86, 87, 88]
for subjects_id in sessid:
    print subjects_id
    img = nib.load(os.path.join(pre_roi_path, rois_name[0]).format(subjects_id=subjects_id))
    affine = img.affine
    data = img.get_data()
    output_data = np.zeros(data.shape)
    for index in range(len(rois_name)):
        roi_data = nib.load(os.path.join(pre_roi_path, rois_name[index]).format(subjects_id=subjects_id)).get_data()
        output_data[roi_data > 0] = value[index]

    dm_img = nib.Nifti1Image(output_data.astype("float32"), affine)
    dm_img.to_filename(output_name.format(subjects_id=subjects_id))


################################
# path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/
# response_dhollander/subjects/standard/MNI152_cytoMPM_thr25_2mm.nii.gz'
# output_name = '/home/brain/workingdir/data/dwi/hcp/preprocessed/
# response_dhollander/subjects/standard/MNI152_cytoMPM_thr25_2mm_{}.nii.gz'
# img = nib.load(path)
# affine = img.affine
# data = img.get_data()
# data1 = np.zeros(data.shape)
# data2 = np.zeros(data.shape)
# data3 = np.zeros(data.shape)
# data4 = np.zeros(data.shape)
# data1[data == 85] = 85
# data2[data == 86] = 86
# data3[data == 87] = 87
# data4[data == 88] = 88
# data1_img = nib.Nifti1Image(data1.astype("float32"), affine)
# data2_img = nib.Nifti1Image(data2.astype("float32"), affine)
# data3_img = nib.Nifti1Image(data3.astype("float32"), affine)
# data4_img = nib.Nifti1Image(data4.astype("float32"), affine)
# data1_img.to_filename(output_name.format('hOc1'))
# data2_img.to_filename(output_name.format('hOc2'))
# data3_img.to_filename(output_name.format('hOc3d'))
# data4_img.to_filename(output_name.format('hOc3v'))
#
######################################
# with open('/home/brain/workingdir/pyfat/bin/subjects_id', 'r') as f:
#     sessid = f.readlines()
#     sessid = [_.strip() for _ in sessid]
#
# print sessid
# #extract
#
# pro_atlas_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#                  'response_dhollander/subjects/{subjects_id}/ROI/JHU_tract_prob.nii.gz'
# output_name = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#               'response_dhollander/subjects/{subjects_id}/ROI/FP_prob.nii.gz'
#
# for subjects_id in sessid:
#     proatlas = nib.load(pro_atlas_path.format(subjects_id=subjects_id))
#     affine = proatlas.affine
#
#     proatlas_data = proatlas.get_data()
#     print proatlas_data[0, 0, 0, 8]
#     coordinate_shape = proatlas_data.shape[:3]
#     extract_atlas = np.zeros(coordinate_shape)
#     extract_atlas[proatlas_data[:, :, :, 8] > 0] = 1
#     dm_img = nib.Nifti1Image(extract_atlas.astype("float32"), affine)
#     dm_img.to_filename(output_name.format(subjects_id=subjects_id))
