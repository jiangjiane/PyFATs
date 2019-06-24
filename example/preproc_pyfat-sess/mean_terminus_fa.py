# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib

from pyfat.io.save import save_nifti


prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/'
terminus_fa_path = 'Diffusion/tractography/Det/results'
terminus_fa_name = ['lvis_terminus_fa_MNI152.nii.gz', 'rvis_terminus_fa_MNI152.nii.gz']

vol_name = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/subjects/standard/MNI152_T1_1mm_brain.nii.gz'

subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_ids'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

img = nib.load(vol_name)
for fas_name in terminus_fa_name:
    img_new = np.zeros((img.shape[0], img.shape[1], img.shape[2], 4))
    sb_count = 0.0
    for sb_id in sessid:
        fa_name = os.path.join(prepath, str(sb_id), terminus_fa_path, fas_name)
        if not os.path.exists(fa_name):
            continue
        sb_count += 1
        img_new += nib.load(fa_name).get_data()
    img_new /= sb_count
    out_path = os.path.join(prepath, 'results', 'mean_' + fas_name)
    save_nifti(img_new, img.affine, out_path)
