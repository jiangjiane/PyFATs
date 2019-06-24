# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

import re
import os
import nibabel as nib

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id'


# tck_name = ['lvis1_density_map_MNI152_mp.nii.gz', 'lvis2_density_map_MNI152_mp.nii.gz',
#             'lvis3_density_map_MNI152_mp.nii.gz', 'lvis4_density_map_MNI152_mp.nii.gz']
tck_name = ['rvis1_density_map_MNI152_mp.nii.gz', 'rvis2_density_map_MNI152_mp.nii.gz',
            'rvis3_density_map_MNI152_mp.nii.gz', 'rvis4_density_map_MNI152_mp.nii.gz']

template = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/subjects/standard/MNI152_T1_1mm_brain.nii.gz'

results_dir = 'Diffusion/tractography/Det/new_results'
out_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
          'response_dhollander/subjects/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

img = nib.load(template)
img_zero = np.zeros((img.shape[0], img.shape[1], img.shape[2], 4))
for i in range(len(tck_name)):
    path = os.path.join(out_dir, tck_name[i])
    data = nib.load(path).get_data()
    img_zero[:, :, :, i] = data

    # img_zero = np.zeros(img.shape)
    # # sub_count = 0.0
    # print tck
    # for subject in sessid:
    #     print subject
    #
    #     fib_path = os.path.join(subjects_dir, subject, results_dir, tck)
    #     if not os.path.exists(fib_path):
    #         continue
    #     data = nib.load(fib_path).get_data()
    #     data[data > 0] = 1.0
    #     # sub_count += 1.0
    #     img_zero += data
    # # img_zero /= sub_count
    # img_zero /= 30.0
    # print img_zero.min()
    # print img_zero.max()
out_path = os.path.join(out_dir, 'rvis_density_map_MNI152_mp.nii.gz')
save_nifti(img_zero, img.affine, out_path)
