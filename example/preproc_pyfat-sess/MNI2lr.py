# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

files_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/standard/'
results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/standard/'

files = ['MNI152_cytoMPM_thr25_1mm_hOc1.nii.gz', 'MNI152_cytoMPM_thr25_1mm_hOc2.nii.gz',
         'MNI152_cytoMPM_thr25_1mm_hOc3d.nii.gz', 'MNI152_cytoMPM_thr25_1mm_hOc3v.nii.gz']


for file_name in files:
    img_path = os.path.join(files_dir, file_name)
    img = nib.load(img_path)
    data = img.get_data()
    datal = np.zeros(img.shape)
    datar = np.zeros(img.shape)
    datal[:img.shape[0]/2, :, :] = data[:img.shape[0]/2, :, :]
    datar[img.shape[0]/2:, :, :] = data[img.shape[0]/2:, :, :]
    out_path_l = os.path.join(results_dir, 'r_' + file_name)
    out_path_r = os.path.join(results_dir, 'l_' + file_name)
    save_nifti(datal, img.affine, out_path_l)
    save_nifti(datar, img.affine, out_path_r)
