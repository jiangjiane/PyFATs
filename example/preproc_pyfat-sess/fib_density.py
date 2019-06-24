# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
# subjects_dirs = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest'

# subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_qyk'
# tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck',
#             'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

# tck_name = ['lvis1_template_centroids.tck', 'lvis2_template_centroids.tck',
#             'lvis3_template_centroids.tck', 'lvis4_template_centroids.tck']

tck_name = ['rvis1_template_centroids.tck', 'rvis2_template_centroids.tck',
            'rvis3_template_centroids.tck', 'rvis4_template_centroids.tck']

vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'

results_dir = 'Diffusion/tractography/Det/new_results'

# with open(subjects_id, 'r') as f:
#     sessid = f.readlines()
#     sessid = [_.strip() for _ in sessid]

# sessid = ['101309']
sessid = ['101915']

for subject in sessid:
    print subject
    img = nib.load(os.path.join(subjects_dir, subject, vol_name))

    for tck in tck_name:

        fib_path = os.path.join(subjects_dir, subject, results_dir, tck)
        if not os.path.exists(fib_path):
            continue
        fas = Fasciculus(fib_path)
        fib = fas.get_data()
        img_zero = fib_density_map(img, fib)
        out_path = os.path.join(subjects_dir, subject, results_dir,
                                '{tck}_density_map.nii.gz'.format(tck=tck.split('.')[0]))
        save_nifti(img_zero, img.affine, out_path)
