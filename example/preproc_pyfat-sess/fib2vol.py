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
tck_name = ['Diffusion/tractography/Det/results/l_vis4.tck',
            'Diffusion/tractography/Det/results/r_vis4.tck']

vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'

results_dir = 'Diffusion/tractography/Det/results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

for subject in sessid:
    print subject
    img = nib.load(os.path.join(subjects_dir, subject, vol_name))
    for tck in tck_name:
        img_zero = np.zeros((img.shape[0], img.shape[1], img.shape[2], 4))
        temppath, hemi = os.path.split(tck)
        fib_path = os.path.join(subjects_dir, subject, tck)
        fas = Fasciculus(fib_path)
        fibs = fas.get_data()
        ids = fas.get_header()['fasciculus_id']
        for index in set(ids):
            fib = fibs[ids == index]
            vol = fib_density_map(img, fib)
            img_zero[:, :, :, index-1] = vol
        out_path = os.path.join(subjects_dir, subject, results_dir, '{hemi}_vis4_vol.nii.gz'.format(hemi=hemi[0]))
        save_nifti(img_zero, img.affine, out_path)





