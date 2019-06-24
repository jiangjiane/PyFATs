# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np
import numpy.linalg as npl
from nibabel.affines import apply_affine

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_ids'

vis_name = ['Diffusion/tractography/Det/results/l_vis4_terminalpoint_posterior_vol.nii.gz',
            'Diffusion/tractography/Det/results/r_vis4_terminalpoint_posterior_vol.nii.gz']

fa_name = 'Diffusion/metrics/fa.nii.gz'

results_dir = 'Diffusion/tractography/Det/results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]


for subject in sessid:
    for vis in vis_name:
        _, hemi = os.path.split(vis)
        img = nib.load(os.path.join(subjects_dir, subject, vis))
        vis_data = img.get_data()
        fa_zero = np.zeros((img.shape[0], img.shape[1], img.shape[2], 4))
        for i in range(4):
            img0 = nib.load(os.path.join(subjects_dir, subject, fa_name))
            fa_data = img0.get_data()
            fa_data[vis_data[:, :, :, i] == 0] = 0
            fa_zero[:, :, :, i] = fa_data

        out_path = os.path.join(subjects_dir, subject, results_dir, '{hemi}_vis4_fa.nii.gz'.format(hemi=hemi[0]))
        save_nifti(fa_zero, img.affine, out_path)

