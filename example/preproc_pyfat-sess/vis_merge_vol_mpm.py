# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

files_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/new_results'
results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/new_results'

l_files = ['l_vis1_terminus_MNI152_mp.nii.gz', 'l_vis2_terminus_MNI152_mp.nii.gz',
           'l_vis3_terminus_MNI152_mp.nii.gz', 'l_vis4_terminus_MNI152_mp.nii.gz']
r_files = ['r_vis1_terminus_MNI152_mp.nii.gz', 'r_vis2_terminus_MNI152_mp.nii.gz',
           'r_vis3_terminus_MNI152_mp.nii.gz', 'r_vis4_terminus_MNI152_mp.nii.gz']

img_path = os.path.join(files_dir, l_files[0])
img = nib.load(img_path)
shape = img.shape

img_zero = np.zeros((shape[0], shape[1], shape[2], 4))
for i in range(len(l_files)):
    img_zero[:, :, :, i] = nib.load(os.path.join(files_dir, l_files[i])).get_data()

pm_temp = np.empty((img_zero.shape[0], img_zero.shape[1], img_zero.shape[2], img_zero.shape[3]+1))
pm_temp[..., range(1, img_zero.shape[3]+1)] = img_zero
l_mpm = np.argmax(pm_temp, axis=3)

# l_mpm = np.zeros(shape) - 1
# l_mpm += np.argmax(img_zero, axis=3) + 2

out_path = os.path.join(results_dir, 'l_vis_terminus_MNI152_mpm_new.nii.gz')
save_nifti(l_mpm, img.affine, out_path)


img_path = os.path.join(files_dir, r_files[0])
img = nib.load(img_path)
shape = img.shape

img_zero = np.zeros((shape[0], shape[1], shape[2], 4))
for i in range(len(r_files)):
    img_zero[:, :, :, i] = nib.load(os.path.join(files_dir, r_files[i])).get_data()


pm_temp = np.empty((img_zero.shape[0], img_zero.shape[1], img_zero.shape[2], img_zero.shape[3]+1))
pm_temp[..., range(1, img_zero.shape[3]+1)] = img_zero
r_mpm = np.argmax(pm_temp, axis=3)

# r_mpm = np.zeros(shape) - 1
# r_mpm += np.argmax(img_zero, axis=3) + 2

out_path = os.path.join(results_dir, 'r_vis_terminus_MNI152_mpm_new.nii.gz')
save_nifti(r_mpm, img.affine, out_path)
