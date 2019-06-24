# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_ids'
vol_name = ['Diffusion/tractography/Det/new_results/l_terminus_MNI152.nii.gz',
            'Diffusion/tractography/Det/new_results/r_terminus_MNI152.nii.gz']


results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

# left or right
shape = nib.load(os.path.join(subjects_dir, sessid[0], vol_name[1])).shape[:3]
for i in range(4):
    # img_zero_prob = np.zeros(shape)
    img_zero_sum = np.zeros(shape)
    print i
    for subject in sessid:
        img = nib.load(os.path.join(subjects_dir, subject, vol_name[1]))
        # temp_data = np.zeros(img.shape[:3])
        data = img.get_data()[:, :, :, i]
        data[data > 0] = 1.0
        # temp_data[data > 0] = 1
        # img_zero_prob += data
        img_zero_sum += data
    # img_zero_prob /= len(sessid)
    img_zero_sum /= len(sessid)
    _, hemi = os.path.split(vol_name[1])
    # out_path_prob = os.path.join(results_dir, '{hemi}_vis{vis_id}_fa_merge_mean24.nii.gz'.format(hemi=hemi[0], vis_id=i+1))
    # save_nifti(img_zero_prob, img.affine, out_path_prob)
    out_path_sum = os.path.join(results_dir, '{hemi}_vis{vis_id}_terminus_MNI152_mp.nii.gz'.format(hemi=hemi[0], vis_id=i+1))
    save_nifti(img_zero_sum, img.affine, out_path_sum)


